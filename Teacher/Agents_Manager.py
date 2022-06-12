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
        self.quit = False
        self.user_name = {}
        self.accept_agent = False

    #main to thread
    def run(self):
        x = threading.Thread(target=self.main_loop, args=())
        x.start()

    # listen to clients' connection
    def connect(self):
        self.ser_socket.bind(('0.0.0.0', self.port))
        print("Waiting for client")
        self.ser_socket.listen(5)

    #read the file and send to client
    def send_file(self, get_file):
        file = open(get_file, 'rb')
        # reading the file into message
        message = file.read()

        # getting the length of the file (bytes)
        length = str(len(message))
        # getting the length of the length, and zero-filling him
        length_of_length = str(len(length)).zfill(3)
        #lengths = length_of_length + length
        print(length)
        print(length_of_length)
        print(length)
        # sending the file itself
        self.send_file_all(message)

    #send the message to the socket
    @staticmethod
    def protocol_message(message, is_text, curr_socket):
        length_msg = len(message)
        length_msg_str = str(length_msg)

        length_length = len(length_msg_str)
        length_length_str = str(length_length).zfill(3)

        curr_socket.send(length_length_str.encode())
        print("length_length_str " + length_length_str)

        curr_socket.send(length_msg_str.encode())
        print("length_msg_str " + length_msg_str)

        print("message " + str(message))
        if is_text:
            curr_socket.send(message.encode())
        else:
            curr_socket.send(message)

    #send the message to every client that connected
    def message_everyone(self, message):
        for current_socket in self.open_client_sockets:
            self.protocol_message(message, True, current_socket)

    #get the read file and send to all clients
    def send_file_all(self, message):
        for current_socket in self.open_client_sockets:
            self.protocol_message(message, False, current_socket)

    #read the file - users
    def read_file_names(self):
        users = open('Users.txt', 'r')

        name_code = {}
        line = list(users.readlines())
        for counter in range(len(line)):
            line[counter] = line[counter].split('\n')[0]

        for counter in range(len(line)):
            name_code.update({line[counter].split()[0]: line[counter].split()[-1]})

        return name_code

    #check if the name and password are in the file Users
    def check_pass(self, user, password):
        name_code = self.read_file_names()
        if str(name_code.get(user)) == password:
            print("yes")
            self.accept_agent = True
        else:
            print("no")
            self.accept_agent = False

    #recive the message from the client and translate the message
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

    #wait for clients and when a client is trying to join he check if he can join
    def main_loop(self):
        while True:
            if self.quit:
                break
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
                    self.protocol_message("close socket", True, new_socket)
                    self.open_client_sockets.remove(new_socket)


        print("finish")
        self.open_client_sockets.clear()
