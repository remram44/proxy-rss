from django.http import HttpResponse
from django.shortcuts import render
import email.utils
import time
import tweepy

from tweetrss import settings


def format_date(d):
    return email.utils.formatdate(time.mktime(d.timetuple()))


class Status(object):
    def __init__(self, text, link, date):
        self.text = text
        self.link = link
        self.date = date


def timeline(request, screen_name):
    include_retweets = request.GET.get('retweets', '1') != '0'

    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(*settings.ACCESS_TOKEN)

    api = tweepy.API(auth)

    try:
        tw_statuses = api.user_timeline(screen_name=screen_name)
    except tweepy.TweepError:
        return HttpResponse("tweepy error", status=503, content_type="text/plain")
    statuses = []
    for status in tw_statuses:
        if hasattr(status, 'retweeted_status'):
            if not include_retweets:
                continue
            status = status.retweeted_status
            statuses.append(Status(
                    u'RT @%s: %s' % (status.author.screen_name, status.text),
                    'https://twitter.com/{screen_name}/status/{id}'.format(
                            screen_name=status.author.screen_name,
                            id=status.id),
                    format_date(status.created_at)))
        else:
            statuses.append(Status(
                    status.text,
                    'https://twitter.com/{screen_name}/status/{id}'.format(
                            screen_name=screen_name,
                            id=status.id),
                    format_date(status.created_at)))

    return render(
            request,
            'proxy/timeline.rss',
            {
                    'screen_name': screen_name,
                    'account_link': 'https://twitter.com/{screen_name}'.format(
                            screen_name=screen_name),
                    'statuses': statuses,
                },
            content_type='application/rss+xml')
