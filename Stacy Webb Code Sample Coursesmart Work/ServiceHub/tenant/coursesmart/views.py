
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ImproperlyConfigured
from django.template import RequestContext 
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth

from tenant.coursesmart.Service import Service
from tenant.coursesmart.Service import emitErrorResponse

from util.CSService import CSService
from security.DatabaseUserIdentity import DatabaseUserIdentity
from core.models import *
from tenant.coursesmart.models import *

import settings

UNIDENTIFIED_TENANT_ERROR = "Tenant can't be identified"
UNIDENTIFIED_USER_ERROR = "User can't be identified"
USER_CANT_BE_AUTHENTICATED = "User %(userId)s can't be authenticated"

def index(req):
    return render_to_response('index.html', {}, 
                              context_instance = RequestContext(req)) 

def getUserId():
    return DatabaseUserIdentity().getUserId()

def nonAuthenticatedService(request, **kwargs):
    operation = kwargs['operation']
    isHtmlView = kwargs['isHtmlView']
    tenantKey = kwargs['tenant']
    tenant = Tenant.objects.get(tenantKey=tenantKey)
    if tenant == None:
        return emitErrorResponse(kwargs, UNIDENTIFIED_TENANT_ERROR, isHtmlView)

    # see adapter in security package for custom behavior
    service = Service(tenant)
    result = service.doOperation(operation, request, kwargs)

    return result
