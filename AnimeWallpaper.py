import multiprocessing as mp
from ext.BackgroundHandle import Manager
from ext import TrayIcon as Tray
import socket


def server_exists() -> bool:
    # Send TCP Socket and wait for answer
    try:
        client_socket = socket.socket()  # instantiate
        client_socket.connect(('localhost', 7331))  # connect to the server

        client_socket.send(str("hi").encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        client_socket.close()  # close the connection
        if data == "hi":
            return True
        return False
    except Exception as e:
        print(e)
        return False


def host_server():
    manager = Manager()
    manager.start(manager, boot_only_guy=server_exists())


if __name__ == '__main__':
    p1 = mp.Process(target=host_server)
    p2 = mp.Process(target=Tray.start_tray_icon)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
