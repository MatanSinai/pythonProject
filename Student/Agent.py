import socket
import App_Handler as app
import Agent_Ui
import tempfile

def main():
    port = open('Get_Ip-Port.txt', 'r')
    get = port.readlines()[-1]
    my_socket = Client_Socket(int(get), socket.socket(socket.AF_INET, socket.SOCK_STREAM), 2)
    agent_name = Agent_Ui.master_ui()
    agent_name.set_agent(my_socket)
    agent_name.main_loop()
    my_socket.connect()
    my_socket.main_loop()


class Client_Socket:
    def __init__(self, port, my_socket, pre_len):
        self.port = port
        self.my_socket = my_socket
        self.pre_len = pre_len
        self.name = ''

    #read the ip from the file Get_Ip-port and try to connect to him
    def connect(self):
        Ip = open('Get_Ip-Port.txt', 'r')
        get = Ip.readlines()[0]
        print(get)
        get = get.split('\n')[0]
        self.my_socket.connect((get, self.port))
        print("Connection established")

    #get text and boolean(if true do an encode else he is not doing an encode) and send to the manager
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

    #get the command(data) and handle the command
    def handle_app(self, data):
        if data == "excel":
            app.App_Handler().open_excel()
        elif data == "word":
            app.App_Handler().open_word()
        elif data == "power point":
            app.App_Handler().open_power_point()
        elif data == "close word":
            app.App_Handler().close_word()
        elif data == "close excel":
            app.App_Handler().close_excel()
        elif data == "close power point":
            app.App_Handler().close_power_point()
        elif data == "close all":
            app.App_Handler().close_power_point()
            app.App_Handler().close_word()
            app.App_Handler().close_excel()
        elif data == 'close program':
            app.App_Handler().close_power_point()
            app.App_Handler().close_word()
            app.App_Handler().close_excel()

    #decode the massage the has been sent from manager
    def recv_message(self):
        length_length_str = self.my_socket.recv(3)
        if length_length_str == "":
            pass
        length_length_str = length_length_str.decode()
        length_length = int(length_length_str)

        msg_length_str = self.my_socket.recv(length_length).decode()
        msg_length = int(msg_length_str)

        message = self.my_socket.recv(msg_length)
        while len(message) < int(msg_length):
            message += self.my_socket.recv(int(msg_length) - len(message))
        return message.decode()

    def recv_file_message(self):
        length_length_str = self.my_socket.recv(3)
        if length_length_str == "":
            pass
        length_length_str = length_length_str.decode()
        length_length = int(length_length_str)

        msg_length_str = self.my_socket.recv(length_length).decode()
        msg_length = int(msg_length_str)

        message = self.my_socket.recv(msg_length)
        while len(message) < int(msg_length):
            message += self.my_socket.recv(int(msg_length) - len(message))
        return message

    #recive the file and save him on the computer disk
    def recv_file(self, file):
        # getting the length of the file
        length = self.my_socket.recv(3).decode()
        print(length)
        # getting the length of the file. reciving with length
        message_length = int(self.my_socket.recv(int(length)).decode())
        print(message_length)
        file_data = b"" + self.my_socket.recv(message_length)

        #save the received file to local disk
        if file == 'docx':
            file_name = tempfile.gettempdir() + r'\\tempTeacherFile.docx'
        elif file == 'xlsx':
            file_name = tempfile.gettempdir() + r'\\tempTeacherFile.xlsx'
        elif file == 'pptx':
            file_name = tempfile.gettempdir() + r'\\tempTeacherFile.pptx'
        text_file = open(file_name, "wb")
        n = text_file.write(file_data)
        text_file.close()
        return file_name

    # responsible for the running client and call the function
    def main_loop(self):
        self.protocol_message(self.name.split(',')[0], True)
        self.protocol_message(self.name.split(',')[-1], True)
        while True:
            data = self.recv_message()
            if data == 'file':
                # Check the type of the file to run
                file = self.recv_file_message()

                #get the file from the server
                file_name = self.recv_file(file)
                print("file name is:" + file_name)
                app.App_Handler().open_file(file_name)
            elif data == 'close program':
                self.handle_app(data)
                break

            elif data == 'close socket':
                break
            else:
                self.handle_app(data)

            if data is None or data == "":
                print("none")
                break
            if "^" in data[0]:
                if 'exit' in data:
                    print("exit")
                    break
        print("Connection severed")
        self.my_socket.close()


if __name__ == '__main__':
    main()
