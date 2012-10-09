__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'


from lxml import etree
import urllib2, cookielib
from urlparse import urlsplit, parse_qsl, urlparse
from syslog import syslog
from HttpsClientAuthHandler import HttpsClientAuthHandler

from KLib.logger import LoggerFactory

import logging
import syslog

logger = LoggerFactory.getDefaultLogger()
logger.setLevel(logging.WARNING)

def getSingleValue(dict, name):
    result = None
    values = dict.get(name)
    if values != None:
        result = values[0]
    return result

def log(string):
    #logger.warn(string)
    syslog.syslog(str(string))
    
def logCommand(command, string):
    log('%s: %s' % (command,string))
    
def parseAttributes(content):
    result = {}
    lines = content.split('\n')
    for line in lines:
        #print line
        equalPos = line.find('=')
        if equalPos >= 0:
            key = line[0:equalPos]
            property = line[equalPos+1:]
            if key == 'userdetails.attribute.name':
                name = property
                values = []
                result[name] = values
            elif key == 'userdetails.attribute.value':
                values.append(property)
    return result    

def parseNameValuePairs(content):
    result = {}
    lines = content.split('\n')
    for line in lines:
        #print line
        equalPos = line.find('=')
        if equalPos >= 0:
            name = line[0:equalPos]
            value = line[equalPos+1:]
            result[name] = value
    return result
    
class IdentityServices(object):
    '''
    Executes a synchronous request.
    '''

    def __init__(self, portalUrl, keyfile=None, certfile=None):
        self.portalUrl = portalUrl
        cookies = cookielib.CookieJar()
        parseResult = urlparse(self.portalUrl)
        if parseResult.scheme == 'https':
            self.urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), \
                                HttpsClientAuthHandler(keyfile, certfile))
        else:
            self.urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
        content = self.doPostService('/identity/getCookieNameForToken', {})
        resultDict = parseNameValuePairs(content)
        self.cookieName = resultDict['string']
        
    def createQueryString(self, paramDict):
        result = ''
        for paramKey in paramDict.keys():
            paramValue = paramDict.get(paramKey)
            result += paramKey + '=' + paramValue + '&'
        return result
        
    def doPostService(self, method, paramDict):
        url = self.portalUrl + '/opensso' + method + '?'
        data = self.createQueryString(paramDict)
        log(url + ' ' + data)
        try:
            content = self.fetchContent(url, data)
        except Exception as exception:
            log(exception)
            content = None
        return content
        
    # if data == NONE-->GET; else POST
    def fetchContent(self, url, data):
        root = None
        response = self.urlOpener.open(url, data)
        content = response.read()
        return content
        
    # if data == NONE-->GET; else POST
    def fetchPage(self, url, data):
        root = None
        content = self.fetchContent(url, data)
        root = etree.fromstring(content)
        return root

    def authenticate(self, username, password, uri=None):
        paramDict = {}
        paramDict['username'] = username
        paramDict['password'] = password
        if uri != None:
            paramDict['url'] = uri
        content = self.doPostService('/identity/authenticate', paramDict)
        resultDict = parseNameValuePairs(content)
        return resultDict.get('token.id')
    
    def getAttributes(self, token):
        result = None
        paramDict = {self.cookieName: token}
        content = self.doPostService('/identity/attributes', paramDict)
        if content != None:
            result = parseAttributes(content)
        return result
        
    def getCookieName(self):
        return self.cookieName
    
    def getUserId(self, token):
        attributeDict = self.getAttributes(token)
        userId = getSingleValue(attributeDict, 'uid')
        return userId
    
    def isAuthenticated(self, token):
        result = False
        paramDict = {"tokenid": token}
        try:
            content = self.doPostService('/identity/isTokenValid', paramDict)
            dict = parseNameValuePairs(content)
            value = dict.get('boolean')
            result = value == 'true'
        except:
            pass
        return result