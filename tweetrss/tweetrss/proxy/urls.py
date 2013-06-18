from django.conf.urls import patterns, include, url

urlpatterns = patterns('tweetrss.proxy',
    url(r'(.+)$', "views.timeline", name="timeline"),
)
