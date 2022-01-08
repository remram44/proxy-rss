import logging

from proxy_rss.proxy import app


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    app.run(debug=True)
