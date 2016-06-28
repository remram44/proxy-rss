from django.http import HttpResponse
from django.shortcuts import render
import calendar
import email.utils
import tweepy

from tweetrss import settings


def format_date(d):
    return email.utils.formatdate(calendar.timegm(d.timetuple())).replace("-0000", "+0000")


class Status(object):
    def __init__(self, status,
                 text=None, datetime=None, id_=None, author=None):
        if text is None:
            text = status.text
        if datetime is None:
            datetime = status.created_at
        if id_ is None:
            id_ = status.id
        if author is None:
            author = status.author
        self.text = (text.encode('ascii', 'xmlcharrefreplace')
                         .decode('ascii'))
        self.datetime = datetime
        self.id = id_
        self.screen_name = author.screen_name
        self.full_name = (author.name.encode('ascii', 'xmlcharrefreplace')
                                     .decode('ascii'))

    @property
    def readable_date(self):
        return self.datetime.strftime("%B %d, %Y")

    @property
    def date(self):
        return format_date(self.datetime)

    @property
    def link(self):
        return 'https://twitter.com/{screen_name}/status/{id}'.format(
                screen_name=self.screen_name,
                id=self.id)


def get_twitter():
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(*settings.ACCESS_TOKEN)

    return tweepy.API(auth)


def timeline(request, screen_name):
    include_retweets = request.GET.get('retweets', '1') != '0'

    api = get_twitter()

    try:
        tw_statuses = api.user_timeline(screen_name=screen_name)
    except tweepy.TweepError:
        return HttpResponse("tweepy error", status=503, content_type="text/plain")
    statuses = []
    for status in tw_statuses:
        date = status.created_at
        if hasattr(status, 'retweeted_status'):
            if not include_retweets:
                continue
            status = status.retweeted_status
            statuses.append(Status(
                    status,
                    text=u'RT @%s: %s' % (status.author.screen_name, status.text),
                    datetime=date))
        else:
            statuses.append(Status(status))

    return render(
            request,
            'proxy/timeline.rss',
            {
                    'screen_name': screen_name,
                    'account_link': 'https://twitter.com/{screen_name}'.format(
                            screen_name=screen_name),
                    'statuses': statuses,
            },
            content_type='application/rss+xml; charset=utf-8')


def search(request, query):
    api = get_twitter()

    try:
        tw_statuses = api.search(query)
    except tweepy.TweepError:
        import traceback
        return HttpResponse("tweepy error" + traceback.format_exc(), status=503, content_type="text/plain")
    statuses = []
    for status in tw_statuses:
        if hasattr(status, 'retweeted_status'):
            continue
        statuses.append(Status(status))

    return render(
            request,
            'proxy/search.rss',
            {
                    'statuses': statuses,
            },
            content_type='application/rss+xml; charset=utf-8')
