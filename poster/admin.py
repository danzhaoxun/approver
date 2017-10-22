from django.contrib import admin
from poster.models import *
import logging
# Register your models here.
logging.debug('admin register')
admin.site.register([Tweet,Comment])
