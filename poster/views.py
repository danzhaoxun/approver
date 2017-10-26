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
from poster.models import Tweet,Comment
# Create your views here.


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ('text','author_email')
        widgets = {
            'text':forms.Textarea(attrs={'cols':50,'rows':3})
        }

"""
get_object_or_404的介绍： 我们原来调用django 的get方法，如果查询的对象不存在的话，会抛出一个DoesNotExist的
异常， 现在我们调用django get_object_or_404方法，它会默认的调用django 的get方法， 如果查询的对象不存在的话，
会抛出一个Http404的异常，我感觉这样对用户比较友好， 如果用户查询某个产品不存在的话，我们就显示404的页面给用户，
比直接显示异常好。
"""

def post_tweet(request,tweet_id=None):                  #这个tweet_id这个名称可以换成其他的  在这里调用的两次都为None
    tweet = None
    logging.debug('post tweet')
    logging.info('tweet_id:%s',tweet_id)
    if tweet_id:
        tweet = get_object_or_404(Tweet,id=tweet_id)    #在这个方法中这句始终没有运行
    if request.method == 'POST':
        logging.debug('method post')
        form = TweetForm(request.POST,instance=tweet)   #缺少request.POST, 页面将不能够跳转  request.POST中有提交的数据
        if form.is_valid():
            logging.debug('is valid')
            new_tweet = form.save(commit=False)
            new_tweet.state = 'pending'
            new_tweet.save()
            #send_review_email()
            return HttpResponseRedirect('/poster/thankyou')
    else:
        form = TweetForm(instance=tweet)
        pending_tweets = Tweet.objects.filter(state = 'pending').order_by('created_at')
        published_tweets = Tweet.objects.filter(state = 'published').order_by('-published_at')
        rejected_tweets = Tweet.objects.filter(state = 'rejected').order_by('-rejected_at')
    return render_to_response('post_tweet.html',{'form':form,'pending_tweets':pending_tweets,'published_tweets':published_tweets,'rejected_tweets':rejected_tweets},RequestContext(request))

def thankyou(request):
    #tweets_in_queue = Tweet.objects.filter(state = 'pending').aggregate(Count('id')).values()  错误语句
    #logging.error('thankyou')
    tweets_in_queue = Tweet.objects.all().filter(state = 'pending').aggregate(Count('id')).get('id__count')
    logging.debug('tweets_in_queue:%d',tweets_in_queue)
    return render_to_response('thank_you.html', {'tweets_in_queue': tweets_in_queue}, RequestContext(request))