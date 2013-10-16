from functools import wraps

import re

from exceptions import NoMatchFound


def match(regex):
    regex = re.compile(regex)
    def decorator(f):
        @wraps(f)
        def decorated_function(msg):
            match = regex.match(msg)
            if match is None:
                raise NoMatchFound("No match found for message: {msg}".format(msg=msg))
            return f(**match.groupdict())
        return decorated_function
    return decorator
