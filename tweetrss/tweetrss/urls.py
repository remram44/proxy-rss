from django.conf.urls import patterns, include, url

urlpatterns = patterns('tweetrss',
    # Setup
    url(r'^$', 'setup.views.index', name='index'),
    url(r'^appkey$', 'setup.views.appkey', name='appkey'),
    url(r'^userkey$', 'setup.views.userkey', name='userkey'),
    #url(r'^userkey_callback$', 'setup.views.userkey_callback', name='userkey_callback'),
    url(r'^userkey_verif$', 'setup.views.userkey_verif', name='userkey_verif'),
    url(r'^getstarted$', 'setup.views.getstarted', name='getstarted'),

    # Proxy
    url(r'^p/(.+)$', 'proxy.views.timeline', name='timeline'),
)

handler404 = 'tweetrss.setup.error_404'
handler500 = 'tweetrss.setup.error_500'
