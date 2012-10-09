__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'

import unittest
from tenant.wgu.LrcLookupService import LrcLookupService

class Test(unittest.TestCase):


    def setUp(self):
        import sys
        import os
        
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
        
        from django.core.management import execute_manager
        try:
            import settings # Assumed to be in the same directory.
        except ImportError:
            sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
            sys.exit(1)
        
        from settings import logger
        self.lrcLookupService = LrcLookupService('wgu.solutionstream.com:8080/lrcs/ws/provision/lookup/resourceId')


    def tearDown(self):
        pass


    def testLookup(self):
        self.assertTrue(self.lrcLookupService.lookup('00000COURSESMART29', 'twinte1'))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()