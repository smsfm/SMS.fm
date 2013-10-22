import sys

if 'threading' in sys.modules:
    del sys.modules['threading']

import gevent.monkey
gevent.monkey.patch_all()
