import ctypes
import shutil
import webview
import socket
import win32gui
from ext.Anine import Anime, Anime2
from ext.DesktopManager import Handle
from screeninfo import get_monitors
import requests as rq


manager = Handle()


def find_window(name: str):
    return win32gui.FindWindow(None, name)


def get_anime(name: str = None, typ: str = None) -> tuple:
    anime = None
    if name is None:
        name: str = input("Enter the name of the anime: ")
    if typ is None:
        print("Enter 'Poster' or 'cover' to get the cover of the anime. To get a Random Scene, enter 'random' or "
              "'scene'.")
        typ: str = input("Do you want a Poster/Cover Image or a Scene Image? (poster/cover, scene/random): ").lower()
    typ = typ.lower()
    if typ == "poster" or typ == "cover":
        anime = Anime(name)
    elif typ == "scene" or typ == "random":
        anime = Anime2(name)
    else:
        print("Invalid input. Please try again with correct syntax.")
        raise SystemExit(0)

    url: str = anime.get_thumbnail()

    if url is None or url.strip() == "":
        print("Can't find a image for this anime")
        # Create small Error Dialog with tkinter messagebox
        ctypes.windll.user32.MessageBoxW(0, "Can't find a image for this anime!", "Error - Can't find anime", 0)

    try:
        extension: str = url.split(".")[-1]
        res = rq.get(url, stream=True)
        shutil.copyfileobj(res.raw, open(f"wallpaper.{extension}", "wb"))
        return f"wallpaper.{extension}", anime
    except TypeError:
        print("Can't find a image for this anime")
        ctypes.windll.user32.MessageBoxW(0, "Can't find a image for this anime!", "Error - Can't find anime", 0)


class Api:

    def __init__(self, man) -> None:
        self.man = man

    def set_bg(self, anime_name: str, typ: str) -> None:
        res: tuple = get_anime(anime_name, typ)
        if res is None:
            return
        self.man.reload_paper(res[0])


class Manager:

    def __init__(self) -> None:
        self.ui = None
        self.instances: list = []
        self.__api = None

    def get_monitor_count(self) -> int:
        return len(get_monitors())

    def mover(self):
        i = 1
        nextmove = 0
        for m in get_monitors():
            try:
                target = find_window('AnimeWallpaperWindow' + str(i))
                # Move Window to current Monitor
                win32gui.MoveWindow(target, nextmove, 0, m.width, m.height, True)
                manager.send_behind(target)
                nextmove += m.width
                i += 1
            except Exception:
                pass

    def callback(self):
        self.ui.events.shown -= self.callback
        server_socket = socket.socket()
        server_socket.bind(('localhost', 7331))
        server_socket.listen(5)
        while True:
            conn, address = server_socket.accept()
            old_data = conn.recv(1024)
            data: str = str(old_data.decode("utf-8"))
            if not data:
                break

            if data == "close" or old_data == b"close":
                for win in self.instances:
                    win.destroy()
                self.ui.destroy()
                server_socket.close()
                break
            elif data == "open-ui":
                try:
                    self.ui.show()
                except KeyError:
                    self.ui = webview.create_window("AnimeWallpaper's", url="src/index.html", width=1200, height=700,
                                                    resizable=True, js_api=self.__api)
                    return
                # Why we answer every time? To Proof that the server is still running. First i build a UPD Server.
                # On UPD this Step is necessary. Now on TCP not but i use it anyway.
            conn.send(b"hi")
            conn.close()

    def get_code(self, image_src: str) -> str:
        # Can't use f String, because CSS uses the "{}" syntax.
        return """
            <html>
                <head>
                    <title>AnimeWallpapers - by Fido_de07#9227</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <!-- Now we use the Style Tag to maximize the image -->
                    <style>
                        body {
                          margin: 0;
                          padding: 0;
                        }
                        
                        img {
                            width: 100%;
                            height: 100%;
                            position: fixed;
                            left: 0;
                            right: 0;
                            top: 0;
                            bottom: 0;
                            margin: auto;
                        }
                    </style>
                </head>
                <body>
                    <img src='../""" + str(image_src) + """'/>
                </body>
            </html>
        """

    def set_code(self) -> None:
        i = 1
        for m in get_monitors():
            print(win32gui.GetWindowText(find_window('AnimeWallpaperWindow' + str(i))))
            win = webview.create_window('AnimeWallpaperWindow' + str(i), url="src/wallpaper.html", width=m.width,
                                        height=m.height, resizable=True, fullscreen=True)
            win.events.shown += self.mover
            win.events.closed += manager.repair()
            self.instances.append(win)
            i += 1

    def reload_paper(self, image_src: str) -> None:
        code: str = self.get_code(image_src)
        with open("src/wallpaper.html", "w", encoding="utf-8") as f:
            f.write(code)
        for win in self.instances:
            win.load_url("src/wait.html")
            win.load_url("src/wallpaper.html")

    def start(self, man, boot_only_guy: bool = False) -> None:
        if not boot_only_guy:
            self.set_code()

        self.__api = Api(man)

        self.ui = webview.create_window("AnimeWallpaper's", url="src/index.html", width=1200, height=700,
                                        resizable=True, js_api=self.__api)
        self.ui.events.shown += self.callback
        webview.start()
