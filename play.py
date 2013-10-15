#!/usr/bin/env python

import requests

import settings


class Play(requests.Session):
    def __init__(self, *args, **kwargs):
        """
        Initialize a new Play session.
        """
        self.host = kwargs.pop("host")
        self.port = kwargs.pop("port")
        self.login = kwargs.pop("login")
        self.token = kwargs.pop("token")

        super(Play, self).__init__(*args, **kwargs)

        self.params = dict(login=self.login, token=self.token)

    def request(self, method, url, *args, **kwargs):
        url = "http://{host}:{port}/api/{path}".format(host=self.host,
                                                       port=self.port, path=url)

        return super(Play, self).request(method, url, *args, **kwargs)

    def get(self, url, *args, **kwargs):
        return self.request("get", url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        return self.request("post", url, *args, **kwargs)

    def play(self):
        return self.post("play")

    def pause(self):
        return self.post("pause")

    def next(self):
        return self.post("next")

    def add(self, **kwargs):
        return self.post("queue/add", data=kwargs)


# Play instance, configured from settings
play = Play(host=settings.PLAY_HOST, port=settings.PLAY_PORT,
            login=settings.PLAY_LOGIN, token=settings.PLAY_TOKEN)


if __name__ == "__main__":
    print play.pause()
    print play.play()
    print play.add(type="song", artist_name="Radiohead", song_name="Creep")
    print play.next()
