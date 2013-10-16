#!/usr/bin/env python

from gevent import monkey
monkey.patch_all()

import gevent

from flask import Flask, request

import twilio.twiml

from smsfm.worker import Worker, notifications


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
def hello_monkey():
    """
    Respond to incoming calls with a simple text message.
    """

    # TODO
    # Figure out what's being requested
    # Request it
    # Render the response

    print "request.values", repr(request.values)
    print "request.values['Body']", request.values['Body']

    resp = twilio.twiml.Response()
    resp.message("Right you are, squire")
    return str(resp)


@app.route("/item", methods=['GET', 'POST'])
def item():
    return str(app.item)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5252, debug=True)
