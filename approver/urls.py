from django.conf.urls import url ,include
import approver.views
urlpatterns = [
    url(r'^$',approver.views.list_tweets),
    url(r'^review/(?P<tweet_id>\d+)$',approver.views.review_tweet),
]

