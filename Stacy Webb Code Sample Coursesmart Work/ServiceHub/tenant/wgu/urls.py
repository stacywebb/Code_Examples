__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'

from django.conf.urls.defaults import *
from django.conf import settings
from django.conf.urls.defaults import *

def tenantContext(operation, isHtmlView=False):
    dict = {'operation': operation, 'isHtmlView': isHtmlView}
    dict['tenant'] = 'wgu'
    return dict
    
allParams = '(?P<userId>\w+)/(?P<emailAddress>.*)/(?P<firstname>.*)/(?P<lastname>.*)/(?P<role>\w+)/$'

urlpatterns = patterns('tenant.wgu.views',
    (r'^SetUser/(?P<userId>\w+)/(?P<emailAddress>.*)/(?P<firstname>.*)/(?P<lastname>.*)/(?P<role>\w+)/$', 'authenticatedService', tenantContext('setuser')),
    
    (r'^GetBookshelfLink/$', 'authenticatedService', tenantContext('getbookshelflink')),
    
    (r'^GetEBookLink/(?P<isbn>\w+)/(?P<page>\d*)/$', 'authenticatedService', tenantContext('getebooklink')),
    (r'^GetEBookLink/(?P<isbn>\w+)/$', 'authenticatedService', tenantContext('getebooklink')),
   
    (r'^ViewBookshelf/$', 'authenticatedService', tenantContext('viewbookshelf', True)),
    
    (r'^ViewEBook/(?P<isbn>\w+)/(?P<page>\d*)/$', 'authenticatedService', tenantContext('viewebook', True)),
    (r'^ViewEBook/(?P<isbn>\w+)/$', 'authenticatedService', tenantContext('viewebook', True)),
    
    (r'^ClearHubData/(?P<emailAddress>.*)', 'authenticatedService', tenantContext('clearhubdata', False)),
    
    (r'^TestSSO/$', 'testSSO'),
    
    (r'^LookupLrc/(?P<resourceId>.*)', 'lookupLrc'),
)