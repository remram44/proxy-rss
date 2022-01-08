import logging

from proxy_rss.wsgi import application


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    application.run(debug=True)
