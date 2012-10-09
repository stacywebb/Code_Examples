__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'

from security.models import *

class DatabaseUserIdentity(object):

    def __init__(self):
        pass
    
    def getUserId(self):
        userIdentities = UserIdentity.objects.filter(isCurrentUser=True)
        if len(userIdentities) == 0:
            result = None
        else:
            result = userIdentities[0].userId
        return result

    def getUserIdentity(self, userId):
        if userId != None:
            try:
                userIdentity = UserIdentity.objects.get(userId=userId)
            except:
                userIdentity = None
        return userIdentity
    
    def clearCurrentUser(self):
        userIdentities = UserIdentity.objects.filter(isCurrentUser=True)
        for userIdentity in userIdentities:
            userIdentity.isCurrentUser = False
            userIdentity.save()
            
    def setCurrentUser(self, userId):
        self.clearCurrentUser()
        userIdentities = UserIdentity.objects.filter(userId=userId)
        for userIdentity in userIdentities:
            userIdentity.isCurrentUser = True
            userIdentity.save()


        
    
        