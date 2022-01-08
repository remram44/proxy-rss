import calendar
import email.utils
from flask import Flask, render_template, request
import logging
import os
import tweepy

from proxy_rss import settings


logging.basicConfig(level=logging.WARNING)

app = Flask(
    'proxy_rss',
    template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
)


def format_date(d):
    return (
        email.utils.formatdate(calendar.timegm(d.timetuple()))
        .replace("-0000", "+0000")
    )


class Status(object):
    def __init__(
        self, status,
        text=None, datetime=None, id_=None, author=None, link=None,
    ):
        if text is None:
            text = status.text
        if datetime is None:
            datetime = status.created_at
        if id_ is None:
            id_ = status.id
        if author is None:
            author = status.author
        if link is None:
            link = status
        self.text = (text.encode('ascii', 'xmlcharrefreplace')
                         .decode('ascii'))
        self.datetime = datetime
        self.id = id_
        self.screen_name = author.screen_name
        self.full_name = (author.name.encode('ascii', 'xmlcharrefreplace')
                                     .decode('ascii'))
        self.link = 'https://twitter.com/{screen_name}/status/{id}'.format(
            screen_name=link.author.screen_name,
            id=link.id,
        )
        if hasattr(status, 'extended_entities'):
            self.images = [
                me['media_url']
                for me in status.extended_entities['media']
                if me['type'] == 'photo'
            ]
        else:
            self.images = []

    @property
    def readable_date(self):
        return self.datetime.strftime("%B %d, %Y")

    @property
    def date(self):
        return format_date(self.datetime)


def get_twitter():
    auth = tweepy.OAuthHandler(
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET,
    )
    auth.set_access_token(*settings.TWITTER_ACCESS_TOKEN)

    return tweepy.API(auth)


@app.route('/p/<screen_name>')
def timeline(screen_name):
    include_retweets = request.args.get('retweets', '1') != '0'

    api = get_twitter()

    try:
        tw_statuses = api.user_timeline(screen_name=screen_name)
    except tweepy.TweepError:
        import traceback
        return (
            "tweepy error\n" + traceback.format_exc(),
            503,
            {'Content-Type': 'text/plain'},
        )
    statuses = []
    for status in tw_statuses:
        if hasattr(status, 'retweeted_status'):
            if not include_retweets:
                continue
            old, status = status, status.retweeted_status
            statuses.append(Status(
                status,
                text=u'RT @%s: %s' % (status.author.screen_name, status.text),
                datetime=old.created_at,
                link=old,
            ))
        else:
            statuses.append(Status(status))

    return (
        render_template(
            'timeline.rss', screen_name=screen_name, statuses=statuses,
            account_link='https://twitter.com/{0}'.format(screen_name),
        ),
        {'Content-Type': 'application/rss+xml'},
    )


@app.route('/s/<query>')
def search(query):
    api = get_twitter()

    try:
        tw_statuses = api.search(query)
    except tweepy.TweepError:
        import traceback
        return (
            "tweepy error\n" + traceback.format_exc(),
            503,
            {'Content-Type': 'text/plain'},
        )
    statuses = []
    for status in tw_statuses:
        if hasattr(status, 'retweeted_status'):
            continue
        statuses.append(Status(status))

    return (
        render_template('search.rss', statuses=statuses),
        {'Content-Type': 'application/rss+xml'},
    )
