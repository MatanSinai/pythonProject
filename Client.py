import socket
import ms_example as ms

def main():
    my_socket = ClientSocket(1727, socket.socket(socket.AF_INET, socket.SOCK_STREAM), 2)
    my_socket.connect()
    my_socket.main_loop()


class ClientSocket:
    def __init__(self, port, my_socket, pre_len):
        self.port = port
        self.my_socket = my_socket
        self.pre_len = pre_len

    def connect(self):
        self.my_socket.connect(('127.0.0.1', self.port))
        print("Connection established")

    def protocol_message(self, message, is_text):
        length_msg = len(message)
        length_msg_str = str(length_msg)

        length_length = len(length_msg_str)
        length_length_str = str(length_length).zfill(2)

        self.my_socket.send(length_length_str.encode())

        self.my_socket.send(length_msg_str.encode())

        if is_text:
            self.my_socket.send(message.encode())
        else:
            self.my_socket.send(message)

    def recv_message(self):
        length_length_str = self.my_socket.recv(2)
        if length_length_str == "":
            pass
        length_length_str = length_length_str.decode()
        length_length = int(length_length_str)

        msg_length_str = self.my_socket.recv(length_length).decode()
        msg_length = int(msg_length_str)

        message = self.my_socket.recv(int(msg_length))
        while len(message) < int(msg_length):
            message += self.my_socket.recv(int(message) - len(message))
        return message.decode()

    def open_app(self, data):

        if data == "excel":
            ms.ms_example().open_excel()
        elif data == "word":
            ms.ms_example().open_word()
        elif data == "powerpoint":
            ms.ms_example().open_pp()

    def main_loop(self):
        while True:
            data = self.recv_message()
            if data is None or data == "":
                print("none")
                break
            if "^" in data[0]:
                if 'exit' in data:
                    print("exit")
                    break
            else:
                self.open_app(data)
                self.protocol_message("Received" + data + " and done", True)

        print("Connection severed")
        self.my_socket.close()


if __name__ == '__main__':
    main()