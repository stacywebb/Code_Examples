
from django.template import RequestContext 
from django.http import HttpResponse
from django.shortcuts import render_to_response

from security.oauth import OAuthUtil

import settings

def exceptionResponse(exceptionName, message):
    settings.logger.error(exceptionName +' ' + message)
    return HttpResponse('<h4>%s</hr><p>%s' % (exceptionName, message))

def index(req):
    return render_to_response('index.html', {}, 
                              context_instance = RequestContext(req)) 
     
def log(msg):
    settings.logger.info(msg)

def ltiService(req):
    paramDict = OAuthUtil.validateSignedRequest("12345", "secret", req)
    return HttpResponse('hello')
