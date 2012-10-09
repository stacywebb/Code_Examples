
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ImproperlyConfigured
from django.template import RequestContext 
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from core.models import *

from util.CSService import CSService

import cookielib
import json
import re

from syslog import syslog

CS_PORTAL = 'http://csrel.bvdep.com'
#REDEMPTION_PROGRAM_ID = '78' # correct program
REDEMPTION_PROGRAM_ID = '27'

def index(req):
    return render_to_response('index.html', {}, 
                              context_instance = RequestContext(req)) 
