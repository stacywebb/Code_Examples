from django.conf.urls.defaults import *
from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('core.views',
    (r'^$', 'index'),
)