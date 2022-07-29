import random
from bs4 import BeautifulSoup as Bs
import json
import requests as rq


class Anime:

    def __init__(self, name: str, __json_response=None) -> None:
        self.__name = name
        if __json_response is None:
            self.__json_response = json.loads(rq.get(f"https://kitsu.io/api/edge/anime?filter[text]={name}").text)
        else:
            self.__json_response = __json_response

    def get_thumbnail(self) -> str:
        # Check if this anime has a cover image
        if len(self.__json_response["data"][0]["attributes"]["coverImage"]) == 0:
            return None
        return self.__json_response["data"][0]["attributes"]["coverImage"]["original"]


class Anime2:

    def __init__(self, name: str):
        name = name.replace(" ", "%20")
        self.__src = Bs(rq.get(f"https://www.anime2you.de/?s={name}").text, "html.parser")
        self.__container = self.__src.find("div", {"class": "td-main-content"})
        self.__cards = self.__container.find_all("div", {"class": "td-module-thumb"})

    def get_thumbnail(self):
        if len(self.__cards) == 0:
            return None
        target = self.__cards[random.randint(0, len(self.__cards)-1)]
        soup = Bs(rq.get(target.find("a")["href"]).text, "html.parser")
        container = soup.find("div", class_="td-post-featured-image")
        return container.find("img")["src"]
