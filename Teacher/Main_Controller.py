import Agents_Manager
import Teacher_Ui

def main():
    # Create the server socket listener for all clients
    manager_clients = Agents_Manager.Server_Socket()
    manager_clients.connect()
    # Run the main thread listener loop
    manager_clients.run()

    # create and run UI
    master_ui = Teacher_Ui.master_ui()
    # to connect between ManagerClients to oopText
    master_ui.set_master_socket(manager_clients)
    master_ui.run()

if __name__ == '__main__':
    main()
