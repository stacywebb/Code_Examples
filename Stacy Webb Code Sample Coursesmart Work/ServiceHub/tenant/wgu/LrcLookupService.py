__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'

import urllib2
import cookielib
import settings
from util import TokenUtil
from syslog import syslog

class LrcLookupService(object):

    def __init__(self, lrcUrlPrefix):
        self.urlPrefix = 'http://' + lrcUrlPrefix
        cookies = cookielib.CookieJar()
        self.urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
        
    def fetchPage(self, url):
        response = self.urlOpener.open(url)
        content = response.read()
        return content
    
    def lookup(self, resourceId, userId):
        result = True
        if settings.LRC_LOOKUP_SERVICE_URL != None: 
            token = TokenUtil.createToken(settings.LRC_DEFAULT_USERNAME, settings.LRC_SHARE_ID, settings.LRC_SHARED_SECRET)
            url = self.urlPrefix + "/" + resourceId + "/token/" + token + "/userName/" + userId
            syslog(url)
            content = self.fetchPage(url)
            syslog(content)
            if content.count('/lrcs/provision/') == 1:
                result = True
            else:
                result = False
        return result

    
