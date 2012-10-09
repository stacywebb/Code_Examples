__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'

from util.CSService import CSService
from core.models import SiteUser
from tenant.coursesmart.models import *

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from util import XmlEmitter
    
def emitErrorResponse(contextDict, message, isHtmlView):
    if isHtmlView:
        result = HttpResponse('<h4>%s</hr><p>%s' % ('Error', message))
    else:
        result = HttpResponse(XmlEmitter.emitXmlContent(contextDict['operation'], False, None, message))
    return result
    
def emitResponse(contextDict, content, isHtmlView):
    if isHtmlView:
        result = HttpResponseRedirect(content)
    else:
        result = HttpResponse(XmlEmitter.emitXmlContent(contextDict['operation'], True, content, None))
    return result

class Service(object):

    def __init__(self, tenant):
        self.tenant = tenant
        self.urlPrefix = 'http://'+tenant.csUrlPrefix
        self.csService = CSService(self.urlPrefix)

    def doOperation(self, operation, request, kwargs):
        self.isHtmlView = kwargs['isHtmlView']
        method = getattr(self, operation)
        return method(request, kwargs)
    
    def redirector(self, request, kwargs):
        try:
            templateName = kwargs['templateName']
            redirectorTemplate = RedirectorTemplate.objects.get(pk=1)
        except:
            return emitErrorResponse(kwargs, "No redirector object fournd for " + templateName, self.isHtmlView)
        templateName = redirectorTemplate.templateName
        template = redirectorTemplate.template
                
        countSubstTokens = template.count("%s")
        
        tuples = ()
        if countSubstTokens >= 1:
            tuples = (kwargs.get('arg1'),)
        elif countSubstTokens >= 2:     
            tuples += (kwargs.get('arg2'),)
        elif countSubstTokens >= 3:
            tuples += (kwargs.get('arg3'),)
        else:
            return emitErrorResponse(kwargs, 'Too many substitutions defined in redirectorTemplate', self.isHtmlView)
        
        redirectString = template % tuples
        return emitResponse(kwargs, redirectString, self.isHtmlView)
            
            