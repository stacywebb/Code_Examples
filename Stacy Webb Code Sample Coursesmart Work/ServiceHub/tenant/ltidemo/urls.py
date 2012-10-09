from django.conf.urls.defaults import *
from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('tenant.ltidemo.views',
    (r'^ltiservice/$', 'ltiService'),
)