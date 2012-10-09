__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'

import settings
from LrcLookupService import LrcLookupService

from util.CSService import CSService
from core.models import SiteUser

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from util import XmlEmitter
from util.BookData import BookData
from tenant.wgu.models import RedemptionProgram
    
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

    def __init__(self, siteUser, tenant, tenantUser):
        self.siteUser = siteUser
        self.tenant = tenant
        self.tenantUser = tenantUser
        self.urlPrefix = 'http://'+tenant.csUrlPrefix
        self.csService = CSService(self.urlPrefix)
        self.bookDataService = BookData(settings)
        if settings.LRC_LOOKUP_SERVICE_URL != None:
            self.lrcLookupService = LrcLookupService(settings.LRC_LOOKUP_SERVICE_URL)
        else:
            self.lrcLookupService = None
        
    def doOperation(self, operation, request, kwargs):
        self.isHtmlView = kwargs['isHtmlView']
        self.userId = kwargs['userId']
        method = getattr(self, operation)
        return method(request, kwargs)

    def createBookshelfUrl(self, kwargs):
        if self.tenantUser == None:
            (self.tenantUser, errorResponse) = self.createCSUser(kwargs)
            if errorResponse != None:
                return errorResponse
        
        (self.sessionKey, self.sessionId) = self.csService.loginUserId(self.tenantUser.csAccountId, self.tenantUser.csUserId) 
        if self.sessionKey == None:
            return emitErrorResponse(kwargs, 'Stored credentials are no longer valid'. self.isHtmlView)
            
        self.redirectUrl = self.urlPrefix + '/mycoursesmart' + \
            '?' + self.getPortalParameter(self.tenant) + 'key=' + self.sessionKey
        
        return emitResponse(kwargs, self.redirectUrl, self.isHtmlView)

    def createEBookUrl(self, kwargs):
        if self.tenantUser == None:
            (self.tenantUser, errorResponse) = self.createCSUser(kwargs)
            if errorResponse != None:
                return errorResponse
        
        self.userId = kwargs.get('userId')
        self.isbn = kwargs.get('isbn')
        self.page = kwargs.get('page')
        
        # Unconditionally check for availability in catalog
        if self.lrcLookupService != None:
            if not self.lrcLookupService.lookup(self.isbn, self.userId):
                return emitErrorResponse(kwargs, "Book is not available in the catalog", self.isHtmlView)

        if not self.csService.isBookOnUserShelf(self.tenantUser.csAccountId, self.tenantUser.csUserId, self.isbn):
            if not self.csService.placeBookOnUserBookshelf(self.tenantUser.csAccountId, self.tenantUser.csUserId, 
                            self.getRedemptionCode(self.isbn), self.isbn):
                return emitErrorResponse(kwargs, "Can't place book on shelf", self.isHtmlView)
        
        (self.sessionKey, self.sessionId) = self.csService.loginUserId(self.tenantUser.csAccountId, self.tenantUser.csUserId) 
        if self.sessionKey == None:
            return emitErrorResponse(kwargs, 'Stored credentials are no longer valid'. self.isHtmlView)

        if self.page == None:
            pageValue = ''
        else:
            pageValue = str(self.page)
            
        self.redirectUrl = self.urlPrefix + '/' + self.isbn + '/' + pageValue + \
            '?' + self.getPortalParameter(self.tenant) + 'key=' + self.sessionKey
        
        return emitResponse(kwargs, self.redirectUrl, self.isHtmlView)
  
    def createCSUser(self, kwargs):
        # Create a user instance
        siteUser = self.siteUser
        tenant = self.tenant
        tenantUser = self.tenantUser
        
        if not self.csService.isUserExists(siteUser.email):
                paramDict = {
                        'Email': siteUser.email,
                        'Password': siteUser.username[::-1],
                        'FirstName': siteUser.first_name,
                        'LastName': siteUser.last_name,
                        'Address': tenant.address,
                        'City': tenant.city,
                        'StateId': tenant.stateId,
                        'Zip': tenant.zip,
                        'CountryId': 'US',
                        'PortalId': str(tenant.portalId)
                    }
                (self.csAccountId, self.csUserId) = self.csService.createStudentUserWithParamDict(paramDict)
        else:
            if tenantUser == None:
                return (None, 
                    emitErrorResponse(kwargs, 
                        "There is a problem creating your CourseSmart membership.  Call Customer Support", 
                        self.isHtmlView))
            self.csUserId = tenantUser.csUserId
            self.csAccountId = tenantUser.csAccountId
                
        if self.csAccountId != None:
            # Insert or Update
            if self.tenantUser == None:
                self.tenantUser = SiteUser()
            
            self.tenantUser.tenant = self.tenant
            self.tenantUser.userId = self.userId
            self.tenantUser.role = kwargs['role']
            self.tenantUser.csUserId = self.csUserId
            self.tenantUser.csAccountId = self.csAccountId
            self.tenantUser.save()
            
            self.siteUser.first_name = kwargs['firstname']
            self.siteUser.last_name = kwargs['lastname']
            self.siteUser.email = kwargs['emailAddress']
            self.siteUser.save()
        else:
            return (None, emitErrorResponse(kwargs, 
                "Can't create student user", self.isHtmlView),)
        
        return (self.tenantUser, None,)
                
    def clearhubdata(self, request, kwargs):
        emailAddress = kwargs['emailAddress']
        try:
            self.tenantUser = SiteUser.objects.get(userId=self.userId, tenant=self.tenant)
            self.csService.deleteAccount(self.tenantUser.csAccountId)
            if self.tenantUser != None:
                self.tenantUser.delete()
            return emitResponse(kwargs, "Account successfully deleted", 
                self.isHtmlView)
        except SiteUser.DoesNotExist:
            if self.csService.isUserExists(emailAddress):
                return emitErrorResponse(kwargs, 
                    'CourseSmart Account for ' + emailAddress 
                    + ' must be manually deleted in BackOffice',
                    self.isHtmlView)
            return emitErrorResponse(kwargs, "Account successfully deleted", 
                self.isHtmlView)

    def setuser(self, request, kwargs):
        (self.tenantUser, errorResponse) = self.createCSUser(kwargs)
        if errorResponse != None:
            return errorResponse
        return emitResponse(kwargs, "User data set", self.isHtmlView)
  
    def getbookshelflink(self, request, kwargs):
        return self.createBookshelfUrl(kwargs)
    
    def getebooklink(self, request, kwargs):
        return self.createEBookUrl(kwargs)
    
    # temporary
    def getRedemptionCode(self, isbn):
        result = None
        fpId = self.csService.getFpidForIsbn(isbn)
        bookInfo = self.bookDataService(fpId)
        publisher = bookInfo.get('publisher')
        redemptionPrograms = RedemptionProgram.objects.all()
        for redemptionProgram in redemptionPrograms:
            if redemptionProgram.publisher == publisher:
                result = redemptionProgram.redemptionProgram
            elif redemptionProgram.publisher == "*":
                allOtherRedemptionPrograms = redemptionProgram.redemptionProgram
        if result == None:
            result = allOtherRedemptionPrograms
        return result
        
    def getPortalParameter(self, tenant):
        result = ''
        if tenant.portal != None:
            result = 'portal=' + tenant.portal + '&'
        return result
    
    def viewbookshelf(self, request, kwargs):
        return self.createBookshelfUrl(kwargs)
    
    def viewebook(self, request, kwargs):
        return self.createEBookUrl(kwargs)

    