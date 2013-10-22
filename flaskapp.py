#!/usr/bin/env python

from gevent import monkey
monkey.patch_all()

import logging

import gevent

from flask import Flask, request

import twilio.twiml

from sms.fm.commands import commands
from sms.fm.exceptions import NoMatchFound
from sms.fm.worker import Worker, notifications


indecipherable = logging.getLogger("indecipherable")

class App(Flask):
    greenlets = []
    item = None

    def __init__(self, name):
        # Spin up a worker
        self.worker = Worker()

        super(App, self).__init__(name)

    def run(self, host=None, port=None, debug=None, **options):
        # Start the worker
        self.greenlets.append(gevent.spawn(self.worker.start))

        # Start the consumer (consumes events from the worker)
        self.greenlets.append(gevent.spawn(self._consume))

        # Run the server
        super(App, self).run(host=host, port=port, debug=debug, **options)

        # Server is shutting down. Let's clean up...
        self._shutdown()

    def _consume(self):
        while True:
            self.item = notifications.get()
            print " * Got", repr(self.item)

    def _shutdown(self):
        print " * Shutting down"
        gevent.killall(self.greenlets)
        gevent.joinall(self.greenlets)

app = App(__name__)


@app.route("/", methods=['GET', 'POST'])
def smsfm():
    """
    Handles all smsfm requests.
    """
    message = request.values['Body']
    iterator = iter(commands)
    while True:
        try:
            # Figure out what's being requested
            command = iterator.next()
            req = command(message)

            # Request it
            resp = req()

            # TODO
            # Render the response
            template_name = command.__name__.replace("_command", "")

        except NoMatchFound:
            continue

        except StopIteration:
            # Couldn't decipher this one, log it
            indecipherable.info(message)

            # Reply with misunderstood message
            # TODO

    resp = twilio.twiml.Response()
    resp.message("Right you are, squire")
    return str(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5252, debug=True)
