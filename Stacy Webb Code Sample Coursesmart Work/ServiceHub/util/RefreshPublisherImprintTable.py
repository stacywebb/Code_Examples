__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'


import sys
import os
import re
import MySQLdb
import urllib
from lxml import etree

BOOKS_PER_PAGE = 50
        
URL_TEMPLATE   = 'http://localhost:8000/xmlapi/?search=BOOK&&md=1&page=%s&spp=' + str(BOOKS_PER_PAGE) + '&'

sys.path.insert(0, "..")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

ANY_DIGIT_PATTERN = pat=re.compile('.*^\d+.*$')

from django.core.management import execute_manager

try:
    import settings # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

from core.models import *

    
def createUrl(page):
    result = URL_TEMPLATE % (str(page))
    return result

def fetchPage(url):
    root = None
    content = urllib.urlopen(url).read()
    try:
        #print content
        root = etree.fromstring(content)
    except:
        print "<!-- PARSE Error -->"
    return root

def getXPathAttribute(node, attrName):
    result = None
    attrs = node.xpath('@'+attrName)
    if attrs != None and len(attrs) > 0:
        result = attrs[0]
    return result
    
def getXPathContent(node, tag):
    result = None
    if getXPathNode(node, tag) != None:
        result = getXPathNode(node, tag).text
    return result

def getXPathNode(node, tag):
    result = None
    subnode = node.xpath(tag)
    if subnode != None and len(subnode) > 0:
        result = subnode[0]
    return result

def string_to_slug(s):    
    raw_data = s
    # normalze string as proposed on http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/251871
    # by Aaron Bentley, 2006/01/02
    try:
        import unicodedata        
        raw_data = unicodedata.normalize('NFKD', raw_data.decode('utf-8', 'replace')).encode('ascii', 'ignore')
    except:
        pass
    return re.sub(r'[^a-z0-9-]+', '_', raw_data.lower()).strip('_')
    

if __name__ == '__main__':
    try:
        database = MySQLdb.connect(
                host="127.0.0.1", 
                port=3307,
                db="ACIS", 
                user="root", 
                passwd="root")
    except:
        print "ERROR: Ensure that setupTunnels has been run"    
        sys.exit()

    Imprint.objects.all().delete()
    EResource.objects.all().delete()
    
    cursor = database.cursor()
    cursor.execute("""
        select imprintName, publisher from View_Imprint;
    """)
    rowTuples = cursor.fetchall()
    for rowTuple in rowTuples:
        imprintName = rowTuple[0]
        imprintKey = string_to_slug(imprintName)
        publisher = rowTuple[1]
        imprint = Imprint(imprintKey=imprintKey, imprint=imprintName, publisher=publisher)
        imprint.save()
        #print imprintKey,imprintName,publisher
        
    # Traverse metadata database
    totalPages = 1000000
    page = 0
    while page < totalPages:
        url = createUrl(page)

        pageNode = fetchPage(url)
        if page == 0:
            # once-only -- get pagecount
            pageCountStr = pageNode.xpath('/coursesmart/@pages')[0]
            totalPages = int(pageCountStr)
            print 'Total pages:', totalPages
        print 'Page:',page
        page += 1
        
        books = pageNode.xpath('book')
        for book in books:
            fpId = book.xpath('@id')[0]
            imprintName = book.xpath('publisher/imprintname')[0].text
            imprintKey = string_to_slug(imprintName)
            try:
                imprint = Imprint.objects.get(imprintKey=imprintKey)
                eResource = EResource(fpId=fpId, imprint=imprint)
            except Imprint.DoesNotExist:
                print "WARNING: invalid imprint",imprintName,"for fpId:",fpId
                eResource = EResource(fpId=fpId)
            eResource.save()
