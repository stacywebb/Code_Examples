__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'


from core.models import SiteUser

class BaseUserIdentity(object):

    def __init__(self):
        pass
    
    def getUserId(self):
        pass

