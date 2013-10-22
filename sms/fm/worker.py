#!/usr/bin/env python

from gevent import monkey
monkey.patch_all()

import gevent

from gevent import queue
notifications = queue.Queue()

import requests

from play import play


class Worker():
    now_playing = None

    def start(self):
        g = gevent.spawn(self._run)
        return g

    def _run(self):
        """
        Continuously poll play.now_playing, emit any changes.
        """
        while True:
            try:
                resp = play.now_playing()
                if resp.ok:
                    now_playing = resp.json()
                    if now_playing != self.now_playing:
                        self.now_playing = now_playing
                        notifications.put_nowait(self.now_playing)
            except requests.ConnectionError:
                pass
            gevent.sleep(5)


if __name__ == "__main__":
    try:
        worker = Worker()
        g = worker.start()
        while True:
            item = notifications.get()
            print "Got", repr(item)

    except KeyboardInterrupt:
        g.kill()
        g.join()
