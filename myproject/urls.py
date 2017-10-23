"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import url,include
from django.contrib.auth.views import login
from poster import urls as poster_urls
from approver import urls as approver_ulrs
import django.contrib.auth.views
from poster.views import post_tweet,thankyou


admin.autodiscover()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^poster/thankyou',thankyou),
    url(r'^poster/$',post_tweet),
    url(r'^poster/create/',post_tweet),
    url(r'^approver/',include(approver_ulrs)),
    url(r'^login',login,name='login'),
    url(r'^logout',django.contrib.auth.views.logout),
]
