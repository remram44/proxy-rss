from django.shortcuts import redirect, render
import os
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
    missing = set()

    app_key = request.POST.get('fkey')
    if not app_key:
        missing.add('fkey')
    app_secret = request.POST.get('fsecret')
    if not app_secret:
        missing.add('fsecret')

    # These parameters are optional
    user_key = request.POST.get('futoken')
    user_secret = request.POST.get('fusecret')
    if user_key or user_secret:
        if not user_key:
            missing.add('futoken')
        if not user_secret:
            missing.add('fusecret')

    if missing:
        # Stuff is missing, ask again
        return render(
                request,
                'setup/appkey.html',
                {
                    'missing': missing,
                    'fkey': app_key or '',
                    'fsecret': app_secret or '',
                    'futoken': user_key or '',
                    'fusecret': user_secret or '',
                })
    else:
        # Try to rewrite the config ourselves
        try:
            filename = os.path.join(
                    os.path.dirname(__file__),
                    '../settings.py')
            with open(filename, 'r') as fp:
                lines = list(fp)
            for lineno in xrange(len(lines)):
                line = lines[lineno]
                if line.startswith('CONSUMER_KEY'):
                    lines[lineno] = 'CONSUMER_KEY = %r\n' % app_key
                elif line.startswith('CONSUMER_SECRET'):
                    lines[lineno] = 'CONSUMER_SECRET = %r\n' % app_secret
                elif user_key:
                    if line.startswith('ACCESS_TOKEN'):
                        closeparen = ')' in line
                        lines[lineno] = (
                                'ACCESS_TOKEN = (%r,\n'
                                '                %r)\n' % (
                                user_key, user_secret))
                        if not closeparen:
                            lineno += 1
                            while ')' not in lines[lineno]:
                                del lines[lineno]
                            del lines[lineno]
            with open(filename, 'w') as fp:
                for line in lines:
                    fp.write(line)
        except IOError:
            return redirect('tweetrss.setup.views.appkey_manual',
                    app_key=app_key,
                    app_secret=app_secret,
                    user_key=user_key,
                    user_secret=user_secret)
        else:
            # If we set the user auth, we are done
            if user_key:
                return redirect('tweetrss.setup.views.getstarted')
            # Else, take use to the OAuth dance
            else:
                return redirect('tweetrss.setup.views.userkey')


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
