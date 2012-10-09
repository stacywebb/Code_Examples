__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'

import MySQLdb
import sys

class BookData(object):

    def __init__(self, settings):
        self.bookdataDatabase = MySQLdb.connect(
            host=settings.DATABASE_HOST, 
            db='BookData', 
            user=settings.DATABASE_USER, 
            passwd=settings.DATABASE_PASSWORD)
        
    def getBookData(self, fpId):
        cursor = self.bookdataDatabase.cursor(MySQLdb.cursors.DictCursor)
        sqlCmd = """
            select * from core_book where fpId = "%s";
            """ % (fpId) 
        cursor.execute(sqlCmd)
        rowDictTuple = cursor.fetchone()
        return rowDictTuple

if __name__ == '__main__':
    
    from django.core.management import execute_manager
    try:
        import settings # Assumed to be in the same directory.
    except ImportError:
        sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
        sys.exit(1)
    
    bookData = BookData(settings)
    bookDict = bookData.getBookData('9780135074046')
    print bookDict
        