#!/usr/bin/env python

from gevent import monkey
monkey.patch_all()

import datetime

import gevent

from gevent import queue
notifications = queue.Queue()


class Worker():
    def start(self):
        g = gevent.spawn(self._run)
        return g

    def _run(self):
        while True:
            item = dict(when=datetime.datetime.utcnow())
            notifications.put_nowait(item)
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
