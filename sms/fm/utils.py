import os

from jinja2 import Environment, FileSystemLoader

from twilio.rest import TwilioRestClient

import settings

# Template environment
environ = Environment(loader=FileSystemLoader(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "templates"))))


def client(**kwargs):
    """
    Returns an instance of TwilioRestClient.
    """
    sid = kwargs.get("sid", settings.TWILIO_ACCOUNT_SID)
    tok = kwargs.get("tok", settings.TWILIO_AUTH_TOKEN)
    return TwilioRestClient(sid, tok)


def sms(to, message, **kwargs):
    """
    Sends an SMS message to the specified recipient using the Twilio client.
    """
    from_ = kwargs.get("from", settings.TWILIO_SMS_NUMBER)

    return client().messages.create(to=to, body=message, from_=from_)


def render_template(template, **kwargs):
    """
    Renders a template outside of the Flask context.
    """
    template = environ.get_template(template)
    return template.render(**kwargs)

