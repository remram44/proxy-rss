from django.conf.urls import patterns, include, url

urlpatterns = patterns('tweetrss',
    # Examples:
    #url(r'^$', 'home.views.index', name='index'),
    url(r'^p/', include('proxy.urls')),
)

handler404 = 'tweetrss.site.error_404'
handler500 = 'tweetrss.site.error_500'
