from flask import Flask
import logging
import os

from proxy_rss import twitter


logging.basicConfig(level=logging.WARNING)


application = Flask('proxy_rss')

application.register_blueprint(twitter.blueprint, url_prefix='/twitter')
