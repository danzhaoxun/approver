from django.conf.urls import url,include
from poster.views import post_tweet,thankyou
import poster.views
urlpatterns = [
    url(r'^$',post_tweet),
    url(r'^create/',post_tweet),
    url(r'^thankyou/',thankyou),
    url(r'^edit/(?P<tweet_id>d+)',poster.views.post_tweet),
]