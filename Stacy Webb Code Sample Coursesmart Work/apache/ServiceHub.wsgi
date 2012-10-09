 # Django settings for Recommender project.

import os
import os.path

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__)+'/../ServiceHub')
    
import sys

sys.path.insert(0, PROJECT_PATH)

import settings

import django.core.management
django.core.management.setup_environ(settings)
utility = django.core.management.ManagementUtility()
command = utility.fetch_command('runserver')

command.validate()

import django.conf
import django.utils

django.utils.translation.activate(django.conf.settings.LANGUAGE_CODE)

import django.core.handlers.wsgi

_application = django.core.handlers.wsgi.WSGIHandler()
def application(environ, start_response):
	environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
	environ['SCRIPT_NAME'] = ''
	return _application(environ, start_response)