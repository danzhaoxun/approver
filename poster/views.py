from django.shortcuts import render_to_response
from django import forms
from django.forms import ModelForm
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.views.generic import TemplateView
from myproject import settings
from poster.models import Tweet
import logging
# Create your views here.


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ('text','author_email')
        widgets = {
            'text':forms.Textarea(attrs={'cols':50,'rows':3})
        }


def post_tweet(request,tweet_id=None):
    tweet = None
    logging.debug('post tweet')
    logging.info('tweet_id:%s',tweet_id)
    if tweet_id:
        tweet = get_object_or_404(Tweet,id=tweet_id)
    if request.method == 'POST':
        logging.debug('method post')
        form = TweetForm(request.POST,instance=tweet)
        if form.is_valid():
            logging.debug('is valid')
            new_tweet = form.save(commit=False)
            new_tweet.state = 'pending'
            new_tweet.save()
            #send_review_email()
            return HttpResponseRedirect('/poster/thankyou')
    else:
        form = TweetForm(instance=tweet)
    return render_to_response('post_tweet.html',{'form':form},RequestContext(request))

def thankyou(request):
    tweets_in_queue = Tweet.objects.filter(state = 'pending').aggregate(Count('id')).values()
    return render_to_response('thank_you.html', {'tweet_in_queue': tweets_in_queue}, RequestContext(request))