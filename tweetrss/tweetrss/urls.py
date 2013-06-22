from django.conf.urls import patterns, include, url

urlpatterns = patterns('tweetrss',
    # Examples:
    #url(r'^$', 'home.views.index', name='index'),

    # Proxy
    url(r'^p/(.+)$', 'proxy.views.timeline', name='timeline'),
)

handler404 = 'tweetrss.site.error_404'
handler500 = 'tweetrss.site.error_500'
