__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'

from django.template import RequestContext 
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.core.cache import cache

import settings

from tenant.wgu.Service import Service
from tenant.wgu.Service import emitErrorResponse

from security.DatabaseUserIdentity import DatabaseUserIdentity
from security.models import UserIdentity
from django.contrib.auth.models import User
from core.models import *
from tenant.wgu.models import *

from tenant.wgu.LrcLookupService import LrcLookupService

UNIDENTIFIED_TENANT_ERROR = "Tenant can't be identified"
UNIDENTIFIED_USER_ERROR = "User can't be identified"
USER_CANT_BE_AUTHENTICATED = "User %(userId)s can't be authenticated"

identityService = None

def index(req):
    return render_to_response('index.html', {}, 
                              context_instance = RequestContext(req)) 
    
def log(msg):
    settings.logger.info(msg)
    
def createRedirectAddress(host, request):
    scheme = 'http'
    path = request.get_full_path()
    url = scheme + '://' + host + path
    log(url)
    return url

def getUserField(request, aliases):
    result = None
    for alias in aliases:
        value = request.GET.get(alias)
        if value != None:
            result = value
            break
    return result

def getUserInfoTest(request, kwargs):
    userId = DatabaseUserIdentity().getUserId()
    try:
        userIdentity = DatabaseUserIdentity().getUserIdentity(userId)
        kwargs['userId'] = userId
        kwargs['firstname'] = userIdentity.firstName
        kwargs['lastname'] = userIdentity.lastName
        kwargs['emailAddress'] = userIdentity.emailAddress
        kwargs['role'] = userIdentity.role
    except UserIdentity.DoesNotExist:
        userId = None
        kwargs['userId'] = userId
    
def getUserInfo(request, kwargs):
    redirectResponse = None    
    ssoSource = kwargs['sso']  
    attributeDict = dict()
    userId = None
    authMemCookieKey = request.COOKIES.get('AuthMemCookie')
    if authMemCookieKey != None:
        attrBuf = cache.get(authMemCookieKey)
        if attrBuf != None:
            attributes = attrBuf.split('\r\n')
            for attributePair in attributes:
                tokens = attributePair.split('=')
                if len(tokens) == 2:
                    name = tokens[0]
                    value = tokens[1]
                    log(name + '=' + value)
                    attributeDict[name] = value
            userId = attributeDict.get('ATTR_UserId')
    if userId != None:  
        kwargs['userId'] = userId
        kwargs['firstname'] = attributeDict.get('ATTR_FirstName')
        kwargs['lastname'] = attributeDict.get('ATTR_LastName')
        kwargs['emailAddress'] = attributeDict.get('ATTR_EmailAddress')
        kwargs['role'] = 'student'
        log('OpenSSO authenticated ' + userId)
    elif ssoSource == None or ssoSource.endswith('andDB'):
        getUserInfoTest(request, kwargs)
        log('TestAuthenticator authenticated ' + kwargs['userId'])
    else:
        redirectResponse = emitErrorResponse(kwargs, UNIDENTIFIED_USER_ERROR, kwargs['isHtmlView'])
    return redirectResponse

def authenticatedService(request, **kwargs):
    operation = kwargs['operation']
    isHtmlView = kwargs['isHtmlView']
    redirectResponse = getUserInfo(request, kwargs)
    if redirectResponse != None:
        return redirectResponse
    userId = kwargs['userId']
    tenantKey = kwargs['tenant']
    tenant = Tenant.objects.get(tenantKey=tenantKey)
    if tenant == None:
        return emitErrorResponse(kwargs, UNIDENTIFIED_TENANT_ERROR, isHtmlView)
    try:
        tenantUser = SiteUser.objects.get(userId=userId, tenant=tenant)
    except SiteUser.DoesNotExist:
        tenantUser = None
    
    # see adapter in security package for custom behavior
    user = auth.authenticate(**kwargs)
    if user != None and user.is_authenticated:
        auth.login(request, user) 
        try:
            service = Service(user, tenant, tenantUser)
            result = service.doOperation(operation, request, kwargs)
        except:
            auth.logout(request)
            raise
        auth.logout(request)
    else:
        return emitErrorResponse(kwargs, USER_CANT_BE_AUTHENTICATED % (kwargs), isHtmlView)
    return result

def lookupLrc(request, **kwargs):
    resourceId = kwargs['resourceId']
    lrcLookupService = LrcLookupService(settings.LRC_LOOKUP_SERVICE_URL)
    result = lrcLookupService.lookup(resourceId)
    return HttpResponse(result)
    
def testSSO(request, **kwargs):
    output = "<html><body><table>"
    output += "<h3>SSO attributes</h3>"
    for keyname in request.POST.keys():
        #if keyname.startswith('MCAC_'):
            value = request.POST.get(keyname)
            output += "<tr><td>" + keyname + "</td><td>" + value + "</td></tr>" 
    output += "</table></body></html>"
    return HttpResponse(output)
