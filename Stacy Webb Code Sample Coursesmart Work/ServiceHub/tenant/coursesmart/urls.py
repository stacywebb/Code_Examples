 from django.conf.urls.defaults import *
from django.conf import settings
from django.conf.urls.defaults import *

def tenantContext(operation, isHtmlView=True):
    dict = {'operation': operation, 'isHtmlView': isHtmlView}
    dict['tenant'] = 'coursesmart'
    return dict
    
urlpatterns = patterns('tenant.coursesmart.views',
    (r'^Redirector/(?P<templateName>\w+)/(?P<arg1>.*)/(?P<arg2>.*)/(?P<arg3>.*)/$', 'nonAuthenticatedService', tenantContext('redirector')),
    (r'^Redirector/(?P<templateName>\w+)/(?P<arg1>.*)/(?P<arg2>.*)/$', 'nonAuthenticatedService', tenantContext('redirector')),
    (r'^Redirector/(?P<templateName>\w+)/(?P<arg1>.*)/$', 'nonAuthenticatedService', tenantContext('redirector')),
)