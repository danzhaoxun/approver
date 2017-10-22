from django.db import models

# Create your models here.

# Create your models here.
class Tweet(models.Model):
    #推文内容
    text = models.CharField(max_length=140)
    #作者邮箱
    author_email = models.CharField(max_length=200)
    #推文创建时间（auto_now_add:表示create_at字段自动含有当前的日期和时间，同时表示无论什么时候创建推文并保存到数据库中）
    created_at = models.DateTimeField(auto_now_add=True)
    #推文审核时间(允许publish_at的字段为null)
    published_at = models.DateTimeField(null = True)
    #推文的三种状态
    STATE_CHOICES = (
        ('pending','pending'),
        ('published','published'),
        ('rejected','rejected'),
    )
    #推文状态
    state = models.CharField(max_length=15,choices=STATE_CHOICES)
    #告知django在管理的web站点中显示每个Tweet对象的text属性
    def __unicode__(self):
        return self.text
    #可以通过这个类通知Django对数据实体的其它要求
    class Meta:
        permissions = (
            ("can_approve_or_reject_tweet",
             "Can approve or reject tweets"),
        )

class Comment(models.Model):
    #ForengnKey该字段，它指向Tweet类，这个字段让Django数据库中的Tweet和comment对象之间创建一对多的关系
    tweet = models.ForeignKey(Tweet)
    #评论推特文本
    text = models.CharField(max_length=300)
    #评论时间
    create_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text
