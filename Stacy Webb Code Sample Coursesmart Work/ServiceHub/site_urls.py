__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'

import os.path

from django.conf.urls.defaults import *
from django.http import Http404
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^Test/', include('tenant.test.urls'), {'sso': 'IdP'}),
    (r'^tennant_Test/', include('tenant.test.urls'), {'sso': 'IdPandDB'}),
    
    (r'^coursesmart/', include('tenant.coursesmart.urls')),
    
    (r'^lti/', include('tenant.ltidemo.urls')),
    
    (r'^core/', include('core.urls')),
    (r'^%s' % settings.SITE_NAME, include('core.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve', 
         {'document_root': os.path.join(settings.PROJECT_PATH, '..', 'media')}),
    )


def no_view(req):
    raise Http404


url(r'ServiceHubMedia/$', no_view, name='static_root')
