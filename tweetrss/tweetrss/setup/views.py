from django.shortcuts import redirect, render
import tweepy

from tweetrss import settings


def index(request):
    """First page: how to add app to Twitter.
    """
    if (settings.CONSUMER_KEY != 'app consumer key' and
            settings.CONSUMER_SECRET != 'app secret'):
        if settings.ACCESS_TOKEN != ('user access key',
                                     'user acces secret'):
            return redirect('tweetrss.setup.views.getstarted')
        else:
            return redirect('tweetrss.setup.views.userkey')
    return render(
            request,
            'setup/index.html')

def appkey(request):
    """Enter the application key that Twitter generated.
    """
    return render(
            request,
            'setup/appkey.html')


def userkey(request):
    """Explain how to setup user auth token, choose whether to use callback.
    """


def userkey_callback(request):
    """If callback is used, user is redirected here after auth.
    """


def userkey_verif(request):
    """If callback is not used, user enters verification code here.
    """


def getstarted(request):
    """Once everything is setup, checks configuration and displays help.
    """
