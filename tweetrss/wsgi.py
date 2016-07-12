import logging

import tweetrss.proxy


logging.basicConfig(level=logging.WARNING)

# WSGI interface
application = tweetrss.proxy.app
