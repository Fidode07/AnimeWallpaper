from pystray import MenuItem as item
import pystray
from PIL import Image
import socket


global icon


def __send_msg(msg: str):
    client_socket = socket.socket()
    client_socket.connect(('localhost', 7331))

    client_socket.send(str(msg).encode())
    data = client_socket.recv(1024).decode()

    client_socket.close()


def quit_window():
    global icon
    __send_msg("close")
    icon.stop()


def show_window():
    __send_msg("open-ui")


def start_tray_icon():
    global icon
    image = Image.open("src/logo.ico")
    menu = (item('Open UI', show_window), item('Exit ...', quit_window))
    icon = pystray.Icon(name="AnimeWallpaper", icon=image, title="AnimeWallpaper", menu=menu)
    icon.run()
