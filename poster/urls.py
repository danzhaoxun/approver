from django.conf.urls import url,include
import poster.views
urlpatterns = [
    #url(r'^$',poster.views.post_tweet),
    #url(r'^create/',poster.views.post_tweet),
    url(r'^thankyou/',poster.views.thankyou),
    url(r'^edit/(?P<tweet_id>d+)',poster.views.post_tweet),
]