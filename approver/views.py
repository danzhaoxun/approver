from django.shortcuts import render_to_response
from datetime import datetime
from django import forms
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from myproject import settings
from poster.views import *
from poster.models import Tweet,Comment
from django.contrib.auth.decorators import permission_required


# Create your views here.
"""
用于检查用户是否具有特定权限的视图的装饰器
启用，如有必要，重定向到登录页。
如果raise_exception参数给出了permissiondenied例外
提高。

"""
@permission_required('poster.can_approve_or_reject_tweet',login_url='/login')

#列举推特数据
def list_tweets(request):
    pending_tweets = Tweet.objects.filter(state='pending').order_by('create_at')
    published_tweets = Tweet.objects.filter(state='published').order_by('-published_at')
    return render_to_response('list_tweets.html',{'pending_tweets':pending_tweets,'published_tweets':published_tweets})

#审视表单
class ReviewForm(forms.Form):
    new_comment = forms.CharField(max_length=300,widget=forms.Textarea(attrs={'cols':50,'rows':6}),required=False)
    APPROVAL_CHOICES = (
        ('approve','Approve this tweet and post it to Twitter'),
        ('reject','Reject this tweet and send ti back to the authoer with your comment'),
    )
    approval = forms.ChoiceField(choices=APPROVAL_CHOICES,widget=forms.RadioSelect)

@permission_required('poster.can_approve_or_reject_tweet',login_url='/login')

#重审推特
def review_tweet(request,tweet_id):
    reviewed_tweet = get_object_or_404(Tweet,id=tweet_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_comment = form.cleaned_data['new_comment']
            if form.cleaned_data['approval'] == 'approve':
                reviewed_tweet.published_at = datetime.now()
                reviewed_tweet.state = 'published'
            else:
                #link = request.build_absolute_uri(reverse(post_tweet,args=[reviewed_tweet.id]))
                reviewed_tweet.state = 'rejected'
            reviewed_tweet.save()
            if new_comment:
                c = Comment(tweet=reviewed_tweet,text=new_comment)
                c.save()
            return HttpResponseRedirect('/approve')
    else:
        form = ReviewForm()
    return render_to_response('review_tweet.html',{'form':form,'tweet':reviewed_tweet,'comments':reviewed_tweet.comment_set.all()},RequestContext(request))





