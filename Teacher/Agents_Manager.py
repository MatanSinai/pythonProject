import select
import socket
import os.path
import shutil
import glob
import threading


class Server_Socket:
    def __init__(self):
        self.port = 1727
        self.ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pre_len = 2
        self.messages_to_send = []
        self.open_client_sockets = []
        self.command = ''
        self.quit = False
        self.user_name = {}
        self.accept_agent = False

    def setQuit(self):
        self.quit = True

    def run(self):
        x = threading.Thread(target=self.main_loop, args=())
        x.start()

    def connect(self):
        self.ser_socket.bind(('0.0.0.0', self.port))
        print("Waiting for client")
        self.ser_socket.listen(5)

    def send_waiting_messages(self):
        for message in self.messages_to_send:
            (curr_socket, data) = message
            self.protocol_message(data, True, curr_socket)
            self.messages_to_send.remove(message)

    def send_file(self, get_file):
        file = open(get_file, 'rb')
        # reading the file into message
        message = file.read()
        # getting the length of the file (bytes)
        length = str(len(message))
        # getting the length of the length, and zero-filling him
        length_of_length = str(len(length)).zfill(3)
        lengths = length_of_length + length
        print(length)
        print(length_of_length)
        print(lengths)
        #self.message_everyone(lengths)
        # sending the file itself
        self.send_file_all(message)

    @staticmethod
    def protocol_message(message, is_text, curr_socket):
        length_msg = len(message)
        length_msg_str = str(length_msg)

        length_length = len(length_msg_str)
        length_length_str = str(length_length).zfill(2)

        curr_socket.send(length_length_str.encode())
        print("length_length_str " + length_length_str)

        curr_socket.send(length_msg_str.encode())
        print("length_msg_str " + length_msg_str)

        print("message " + str(message))
        if is_text:
            curr_socket.send(message.encode())
        else:
            curr_socket.send(message)

    def message_everyone(self, message):
        for current_socket in self.open_client_sockets:
            self.protocol_message(message, True, current_socket)

    def send_file_all(self, message):
        for current_socket in self.open_client_sockets:
            self.protocol_message(message, False, current_socket)

    def read_file(self):

        users = open('Users.txt', 'r')

        name_code = {}
        line = list(users.readlines())
        for counter in range(len(line)):
            line[counter] = line[counter].split('\n')[0]

        for counter in range(len(line)):
            name_code.update({line[counter].split()[0]: line[counter].split()[-1]})

        return name_code

    def check_pass(self, user, password):
        name_code = self.read_file()
        if str(name_code.get(user)) == password:
            print("yes")
            self.accept_agent = True
        else:
            print("no")
            self.accept_agent = False


    @staticmethod
    def recv_message(curr_socket):
        length_length_str = curr_socket.recv(2)
        if length_length_str == "":
            pass
        length_length_str = length_length_str.decode()
        length_length = int(length_length_str)

        msg_length_str = curr_socket.recv(length_length).decode()
        msg_length = int(msg_length_str)

        message = curr_socket.recv(msg_length)
        while len(message) < msg_length:
            message += curr_socket.recv(int(message) - len(message))
        print(message.decode())
        return message.decode()

    def main_loop(self):
        while True:
            rlist, wlist, xlist = select.select([self.ser_socket] + self.open_client_sockets, [], [])
            for current_socket in rlist:
                if current_socket is self.ser_socket:
                    (new_socket, address) = current_socket.accept()
                    self.open_client_sockets.append(new_socket)
                name = self.recv_message(new_socket)
                password = self.recv_message(new_socket)
                self.check_pass((name), password)
                if self.accept_agent:
                    self.user_name.update({new_socket: name})
                else:
                    self.open_client_sockets.remove(new_socket)
            self.send_waiting_messages()
            if self.quit:
                break

        print("finish")
        self.open_client_sockets.clear()