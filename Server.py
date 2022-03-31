import select
import socket
import os.path
import shutil
import glob
def main():
    cli_socket = ServerSocket(1727, socket.socket(socket.AF_INET, socket.SOCK_STREAM), 2)
    cli_socket.connect()
    cli_socket.main_loop()


class ServerSocket:
    def __init__(self, port, ser_socket, pre_len):
        self.port = port
        self.ser_socket = ser_socket
        self.pre_len = pre_len
        self.cli_socket = None
        self.messages_to_send = []
        self.open_client_sockets = []

    def connect(self):
        self.ser_socket.bind(('0.0.0.0', self.port))
        print("Waiting for client")
        self.ser_socket.listen(5)

    def send_waitint_messages(self):
        for message in self.messages_to_send:
            (curr_socket, data) = message
            self.protocol_message(data, True, curr_socket)
            self.messages_to_send.remove(message)

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

        print("message " + message)
        if is_text:
            curr_socket.send(message.encode())
        else:
            curr_socket.send(message)


    def message_everyone(self, message):
        for current_socket in self.open_client_sockets:
            self.protocol_message(message, True, current_socket)


    def message_personal(self, client_socket):
        self.protocol_message(message, True, client_socket)


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
        return message.decode().split()


    def open_app(self, data):
        if data == "excel":
            self.message_everyone("excel")
        elif data == "word":
            self.message_everyone("word")
        elif data == "powerpoint":
            self.message_everyone("powerpoint")

    def main_loop(self):
        while True:
            rlist, wlist, xlist = select.select([self.ser_socket] + self.open_client_sockets, [], [])
            for current_socket in rlist:
                if current_socket is self.ser_socket:
                    (new_socket, address) = current_socket.accept()
                    self.open_client_sockets.append(new_socket)
                    app = input("Which app do you want to open for the client")
                    self.open_app(app)
                self.send_waitint_messages()

if __name__ == '__main__':
    main()