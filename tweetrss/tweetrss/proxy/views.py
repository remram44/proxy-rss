from django.shortcuts import render
import tweepy

from tweetrss import settings


class Status(object):
    def __init__(self, text, link):
        self.text = text
        self.link = link


def timeline(request, screen_name):
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(*settings.ACCESS_TOKEN)

    api = tweepy.API(auth)

    tw_statuses = api.user_timeline(screen_name=screen_name)
    statuses = []
    for status in tw_statuses:
        if hasattr(status, 'retweeted_status'):
            status = status.retweeted_status
            statuses.append(Status(
                    u'RT @%s: %s' % (status.author.screen_name, status.text),
                    'https://twitter.com/{screen_name}/status/{id}'.format(
                            screen_name=status.author.screen_name,
                            id=status.id)))
        else:
            statuses.append(Status(
                    status.text,
                    'https://twitter.com/{screen_name}/status/{id}'.format(
                            screen_name=screen_name,
                            id=status.id)))

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
