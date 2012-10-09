__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'


import urllib2, cookielib
from urlparse import urlsplit, parse_qsl
from lxml import etree
from django.core.exceptions import PermissionDenied
from syslog import syslog

def fixname(name):
    result = name[0:1].upper() + name[1:].lower()
    return result

def log(string):
    #print string
    syslog(string)
    
def logCommand(command, string):
    log('%s: %s' % (command,string))
    
class CSService(object):
    '''
    Executes a synchronous CSService request.
    '''

    def __init__(self, portalUrl):
        self.portalUrl = portalUrl
        cookies = cookielib.CookieJar()
        self.urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    
    def chainedLoginUserIdAndOperation(self, accountId, userId, method, paramDict):
        url = self.portalUrl + "/adminapi?method=LoginUserId"  \
            + "&AccountId=" + accountId \
            + "&UserId=" + userId \
            + "&method=" + method \
            + "&" \
            + self.createQueryString(paramDict)
        log(url)
        resultXml = self.fetchPage(url, None)
        #print etree.tostring(resultXml, pretty_print=True)
        return resultXml
        
    def createQueryString(self, paramDict):
        result = ''
        for paramKey in paramDict.keys():
            paramValue = paramDict.get(paramKey)
            if paramValue != None:
                result += paramKey + '=' + paramValue + '&'
        return result
    
    def createStudentUserWithEmailAddr(self, emailAddr):
        logCommand('createStudentUser', 'emailAddr=%s' % (emailAddr))
        result = (None, None)
        tokens = emailAddr.split('@')
        name = tokens[0]
        domainname = tokens[1]
        tokens = name.split('.')
        if len(tokens) == 2:
            firstname = fixname(tokens[0])
            lastname = fixname(tokens[1])
        else:   # not enough info just grab whole token
            firstname = name
            lastname = name
        password = s = firstname[::-1].lower()  # whoa!
        paramDict = {
            'Email': emailAddr,
            'Password': password,
            'SecurityQuestionId': '2',
            'SecurityQuestionAnswer': 'SuMadre',
            'FirstName': firstname,
            'LastName': lastname,
            'Address': domainname,
            'City': 'Roanoke',
            'StateId': 'VA',
            'Zip': '24015',
            'CountryId': 'US'
            }
        result = self.createStudentUserWithParamDict(paramDict)
        return result
    
    # dict may include:
    # Email, Password, SecurityQuestionId, SecurityQuestionAnswer, FirstName, LastName
    # Address, City, StateId, Zip, CountryId, PortalID
    def createStudentUserWithParamDict(self, paramDict):
        logCommand('createStudentUser', str(paramDict))
        result = (None, None)
        if not 'SecurityQuestionId' in paramDict:
            paramDict['SecurityQuestionId'] = '2'
            paramDict['SecurityQuestionAnswer'] = ''
        resultXml = self.doPostAdminService('CSCreateStudentUser', paramDict)
        if not self.hasErrors(resultXml):
            resultNodes = resultXml.xpath('/CourseSmart/Results/CSCreateStudentUser/AccountId')
            if len(resultNodes) > 0:
                accountId = resultNodes[0].text
                userId = resultXml.xpath('/CourseSmart/Results/CSCreateStudentUser/UserId')[0].text
                result = (accountId, userId)
        return result
        
    # to reset test cases
    def deleteAccount(self, accountId):
        logCommand('deleteAccount', 'accountId=%s' % (accountId))
        paramDict = {'AccountId': accountId}
        resultXml = self.doGetAdminService('DeleteAccount', paramDict)
        return not self.hasErrors(resultXml)
        
    def doGetAdminService(self, method, paramDict):
        url = self.portalUrl + "/adminapi?method=" + method + "&" + self.createQueryString(paramDict)
        log(url)
        root = self.fetchPage(url, None)
        #print etree.tostring(root, pretty_print=True)
        return root
        
    def doPostAdminService(self, method, paramDict):
        url = self.portalUrl + "/adminapi"
        data = "method=" + method + "&" + self.createQueryString(paramDict)
        log(url + ' ' + str(paramDict))
        root = self.fetchPage(url, data)
        #print etree.tostring(root, pretty_print=True)
        return root
        
    def doSearchService(self, searchString):
        url = self.portalUrl + "/xmlapi?search=" + searchString
        log(url)
        root = self.fetchPage(url, None)
        return root
    
    # if data == NONE-->GET; else POST
    def fetchPage(self, url, data):
        root = None
        response = self.urlOpener.open(url, data)
        content = response.read()
        root = etree.fromstring(content)
        return root
    
    def getFpidForIsbn(self, isbn):
        logCommand('getFpidForIsbn', 'isbn=%s' % (isbn))
        result = None
        resultXml = self.doSearchService('ISBN='+isbn)
        if len(resultXml.xpath('/error')) == 0:
            bookNode = resultXml.xpath('/coursesmart/book')[0]
            result = str(bookNode.xpath('@id')[0])
        return result
    
    def getUserTitles(self, accountId, userId):
        logCommand('getUserTitles', 'accountId=%s userId=%s' % (accountId, userId))
        result = []
        resultXml = self.chainedLoginUserIdAndOperation(accountId, userId, 'GetUserAccountProducts', {})
        productNodes = resultXml.xpath('/CourseSmart/Context/User/Account/Products/Product')
        for productNode in productNodes:
            isbn = productNode.xpath('Isbn')[0].text
            result.append(isbn)
        #print etree.tostring(resultXml, pretty_print=True)
        return result
   
    def hasErrors(self, resultXml):
        errorNodes = resultXml.xpath('/CourseSmart/Context/Errors')
        return len(errorNodes) > 0
   
    def isBookOnUserShelf(self, accountId, userId, isbn):
        logCommand('isBookOnUserShelf', 'accountId=%s userId=%s isbn=%s' % (accountId, userId, isbn))
        isbns = self.getUserTitles(accountId, userId)
        return isbn in isbns
   
    def isUserExists(self, emailAddress):
        logCommand('isUserExists', 'emailAddr=%s' % (emailAddress))
        paramDict = {'Email': emailAddress}
        resultXml = self.doGetAdminService('UserExists', paramDict)
        return resultXml.xpath('/CourseSmart/Results/UserExists/Success')[0].text == 'true'
    
    def loginUser(self, username, password):
        logCommand('loginUser', 'username=%s password=<pswd>' % (username))
        paramDict = {'Login': username, 'Password': password}
        resultXml = self.doGetAdminService('LoginUser', paramDict)
        resultNodes = resultXml.xpath('/CourseSmart/Results/LoginUser/SessionKey')
        if len(resultNodes) > 0:
            sessionKey = resultNodes[0].text
            sessionId = resultXml.xpath('/CourseSmart/Results/LoginUser/SessionId')[0].text
            userId = resultXml.xpath('/CourseSmart/Context/User/Id')[0].text
            accountId = resultXml.xpath('/CourseSmart/Context/User/Account/Id')[0].text
            result = (sessionKey, sessionId, accountId, userId)
        else:
            result = (None, None, None, None)
        return result
    
    def loginUserId(self, accountId, userId):
        logCommand('loginUserId', 'accountId=%s userId=%s' % (accountId, userId))
        paramDict = {'UserId': userId, 'AccountId': accountId}
        resultXml = self.doGetAdminService('LoginUserId', paramDict)
        resultNodes = resultXml.xpath('/CourseSmart/Results/LoginUserId/SessionKey')
        if len(resultNodes) > 0:
            sessionKey = resultNodes[0].text
            sessionId = resultXml.xpath('/CourseSmart/Results/LoginUserId/SessionId')[0].text
            result = (sessionKey, sessionId)
        else:
            result = (None, None)
        return result
    
    def logoutUser(self, sessionKey):
        logCommand('logoutUser', 'sessionKey=%s' % (sessionKey))
        paramDict = {'SessionId': sessionKey}
        resultXml = self.doGetAdminService('LogoutUser', paramDict)
        return resultXml.xpath('/CourseSmart/Results/LogoutUser/Success')[0].text == 'true'
        
    def placeBookOnUserBookshelf(self, accountId, userId, redemptionId, isbn, redemptionFormat=1, portalName=None):
        logCommand('placeBookOnUserBookshelf', 
                   'accountId=%s userId=%s redemptionId=%s isbn=%s portal=%s' 
                            % (accountId, userId, redemptionId, isbn, portalName))
        result = False
        paramDict = {
                'Number': '1',
                'ProductList': isbn,
                'ProgramID': str(redemptionId)
            }
        resultXml = self.doGetAdminService('GenerateRedemptionCode', paramDict)
        if not self.hasErrors(resultXml):
            couponNodes = resultXml.xpath('/CourseSmart/Results/GenerateRedemptionCode/Coupons')
            if len(couponNodes) > 0:
                coupon = couponNodes[0].xpath('CouponCode')[0].text
                
                # put on shelf
                paramDict = {
                        'Code': coupon,
                        'RedemptionFormat': str(redemptionFormat)
                    }
                if portalName != None:
                    paramDict['Portal'] = portalName
                resultXml = self.chainedLoginUserIdAndOperation(accountId, userId, 'AddRedemptionCode', paramDict)
                if not self.hasErrors(resultXml):
                    result = True
                #else:
                    #raise PermissionDenied, "Could not add redeemed book to bookShelf"
        #print etree.tostring(resultXml, pretty_print=True)
        return result
    
    def requestFIAProductCode(self, school, firstname, lastname, emailAddr, 
                              productList, professorId,  
                              schoolId=None, department=None, schoolZip=None,
                              schoolState=None):
        logCommand('requestProductCode', 'professorId=%s, emailAddr=%s' % (professorId,emailAddr))
        campaignCode = "SAMPLE_EXAMCOPY"
        publisherId = "CSPUB"
        accountExtendedRole = "2"
        result = (None, None)
        tokens = emailAddr.split('@')
        name = tokens[0]
        domainname = tokens[1]
        paramDict = {
            'AccountExtendedRole': accountExtendedRole,
            'CampaignCode': campaignCode,
            'ProfessorId': professorId,
            'ProfessorEmail': emailAddr,
            'ProfessorFirstName': firstname,
            'ProfessorLastName': lastname,
            'ProfessorSchool': school,
            'ProfessorSchoolID': schoolId,
            'ProfessorDepartment': department,
            'ProfessorZIP': schoolZip,
            'ProfessorState': schoolState,
            'ProductList': productList,
            'PublisherId': publisherId,
            }
        result = self.requestFIAProductCodeWithParamDict(paramDict)
        return result
   
    def requestFIAProductCodeWithParamDict(self, paramDict):
        logCommand('requestProductCodeWithParamDict', str(paramDict))
        result = (None, None)
        resultXml = self.doPostAdminService('CSRequestProductCode', paramDict)
        if not self.hasErrors(resultXml):
            resultNodes = resultXml.xpath('/CourseSmart/Results/CSRequestProductCode/AccountId')
            if len(resultNodes) > 0:
                accountId = resultNodes[0].text
                userId = resultXml.xpath('/CourseSmart/Results/CSRequestProductCode/UserId')[0].text
                result = (accountId, userId)
        #print etree.tostring(resultXml, pretty_print=True)
        return result