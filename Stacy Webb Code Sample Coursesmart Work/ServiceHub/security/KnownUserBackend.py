__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'

import os.path
import glob
import tenant

from settings import logger

from django.contrib.auth.models import User

def get_subpackages(module):
    dir = os.path.dirname(module.__file__)
    def is_package(d):
        d = os.path.join(dir, d)
        return os.path.isdir(d) and glob.glob(os.path.join(d, '__init__.py*'))
    return filter(is_package, os.listdir(dir))


class KnownUserBackend(object):
    def __init__(self):
        pass
    
    def get_user(self, user_id):
        result = None
        try:
            result = User.objects.get(username=user_id)
        except:
            pass
        return result
        
    def authenticate(self, **kwargs):
        result = None
        tenantKey = kwargs.get('tenant')
        userId = kwargs.get('userId')
        if tenantKey != None and userId != None:
            tenantPackages = get_subpackages(tenant)
            logger.warn(str(tenantPackages))
            if tenantKey in tenantPackages:
                result = self.get_user(userId)
                logger.warn(str(tenantKey))
                if result == None:
                    if 'emailAddress'in kwargs.keys():
                        # 'Long' call has been issued
                        userId = kwargs['userId']
                        emailAddress = kwargs['emailAddress']
                        firstname = kwargs['firstname']
                        lastname = kwargs['lastname']
                        role = kwargs['role']
                        raw_password = userId[::-1]
                        user = User(username=userId, email=emailAddress, first_name=firstname,
                                    last_name=lastname)
                        user.set_password(raw_password)
                        user.save()
                        result = user
        return result
        
        