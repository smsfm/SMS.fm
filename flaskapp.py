#!/usr/bin/env python

from gevent import monkey
monkey.patch_all()

import logging

import gevent

from flask import Flask, render_template, request

import twilio.twiml

from sms.fm.commands import commands
from sms.fm.exceptions import NoMatchFound
from sms.fm.worker import Worker, notifications
from sms.fm import utils

indecipherable = logging.getLogger("indecipherable")


class App(Flask):
    requests = []
    greenlets = []
    item = None
    request = None

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
        """
        Consumes now playing notifications.

        Alerts the initiator when their request is being played.
        """
        while True:

            # Get the now playing item
            self.item = notifications.get()
            print " * Got", repr(self.item), repr(self.requests)

            # Are there any requests to match against
            if self.request is None:
                try:
                    self.request = self.requests.pop(0)

                except IndexError:
                    # Nothing to match against, ignore
                    continue

            # If item matches request, then alert the initiator of the request
            # that their request is not playing
            lft = self.item["now_playing"]
            rgt = self.request["requested"]["songs"][0]

            # Matches
            # We allow artists to be matched alone, but a title or album must be paired with the artist
            artist_match = lft["artist_name"] == rgt["artist_name"]
            title_match = artist_match and lft["title"] == rgt["title"]
            album_match = artist_match and lft["album_name"] == rgt["album_name"]

            if artist_match or title_match or album_match:
                # Send an alert!
                message = utils.render_template("now_playing.txt", ok=True, data=self.item)
                utils.sms(self.request["request"]["From"], message)

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

            if resp.ok:
                # Parse the response
                data = resp.json()

                # Save this request / reply
                if command.__name__.startswith("play_"):
                    app.requests.append(dict(requested=resp.json(), request=request.values))

            else:
                # No response
                data = None

            # Render the reply
            template_name = "".join((command.__name__.replace("_command", ""), ".txt"))
            reply = render_template(template_name, ok=resp.ok, data=data)

            break

        except NoMatchFound:
            continue

        except StopIteration:
            # Couldn't decipher this one, log it
            indecipherable.info(message)

            # Reply with misunderstood message
            reply = "Sorry, no comprende :("

            break

    resp = twilio.twiml.Response()
    resp.message(reply)
    return str(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5252, debug=True)
