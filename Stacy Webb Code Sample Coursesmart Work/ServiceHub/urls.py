from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('',
    (r'^%s/' % settings.SITE_NAME, include('site_urls')),
)