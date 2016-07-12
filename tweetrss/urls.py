from django.conf.urls import patterns, include, url

urlpatterns = patterns('tweetrss',
    # Examples:
    #url(r'^$', 'home.views.index', name='index'),

    # Timeline
    url(r'^p/(.+)$', 'proxy.views.timeline', name='timeline'),
    # Search
    url(r'^s/(.+)$', 'proxy.views.search', name='search'),
)

handler404 = 'tweetrss.site.error_404'
handler500 = 'tweetrss.site.error_500'
