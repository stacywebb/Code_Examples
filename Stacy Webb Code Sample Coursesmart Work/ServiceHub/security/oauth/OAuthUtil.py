__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'

import oauth2 as oauth
import urllib2
import urlparse
import json

def createServer():
    server=oauth.Server({})
    server.add_signature_method(oauth.SignatureMethod_PLAINTEXT())
    server.add_signature_method(oauth.SignatureMethod_HMAC_SHA1())
    return server

def createSignedRequest(keyId, sharedSecret, method, url, params):
    consumer = oauth.Consumer(key="12345", secret="secret")

    params['oauth_consumer_key'] = keyId
    
    params['oauth_timestamp'] = oauth.generate_timestamp()
    params['oauth_nonce'] = oauth.generate_nonce()

    #params['oauth_timestamp'] = "1280948289"
    #params['oauth_nonce'] = "99999999"
    
    # Create our request. Change method, etc. accordingly.
    req = oauth.Request(method=method, url=url, parameters=params)
    
    # Sign the request.
    signature_method = oauth.SignatureMethod_HMAC_SHA1()
    req.sign_request(signature_method, consumer, None)
    return req
    
def sendSignedRequest(signedRequest):
    urlParsed = urlparse.urlparse(signedRequest.url)
    baseUrl = urlParsed.scheme + "://" + urlParsed.netloc + urlParsed.path
    queryString = signedRequest.to_postdata()
    if signedRequest.method == "GET":
        fullUrl = baseUrl + "?" + queryString
        f = urllib2.urlopen(fullUrl)
    elif signedRequest.method == "POST":
        f = urllib2.urlopen(baseUrl, queryString)
    content = f.read()
    return json.loads(content)
    

def verifySignedRequestfromUrl(keyId, sharedSecret, method, signedUrl):
    urlTokens = signedUrl.split('?')
    urlPrefix = urlTokens[0]
    queryString = urlTokens[1]
    server=createServer()
    newreq = oauth.Request.from_request(method, urlPrefix, query_string=queryString)
    consumer=oauth.Consumer(keyId, sharedSecret)
    server.verify_request(newreq, consumer, None)
    return newreq.get_nonoauth_parameters()

def xvalidateSignedRequest(keyId, sharedSecret, httpRequest):
    method = httpRequest.method
    server = createServer()
    if method == "GET":
        path = httpRequest.path
        queryString = httpRequest.META.get('QUERY_STRING')
        
        pass
    elif method == "POST":
        path = "http://" + httpRequest.get_host() + httpRequest.path
        postdata = httpRequest.raw_post_data
        req = oauth.Request.from_request("POST", path, query_string=postdata)
        consumer=oauth.Consumer(keyId, sharedSecret)
        params = server.verify_request(req, consumer, None)
        pass
    return None

def validateSignedRequest(keyId, sharedSecret, httpRequest):
    method = httpRequest.method
    server = createServer()
    path = "http://" + httpRequest.get_host() + httpRequest.path
    if method == "GET":
        queryString = httpRequest.META.get('QUERY_STRING')
    elif method == "POST":
        queryString = httpRequest.raw_post_data
    req = oauth.Request.from_request(method, path, query_string=queryString)
    consumer=oauth.Consumer(keyId, sharedSecret)
    params = server.verify_request(req, consumer, None)
    return None
    
