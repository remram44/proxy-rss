import logging

import proxy_rss.proxy


logging.basicConfig(level=logging.WARNING)

# WSGI interface
application = proxy_rss.proxy.app
