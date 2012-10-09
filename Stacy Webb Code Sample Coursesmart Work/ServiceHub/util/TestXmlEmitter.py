__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'

import unittest

import XmlEmitter

class TestXmlEmitter(unittest.TestCase):


    def testSuccess(self):
        print '\n' + XmlEmitter.emitXmlContent("testSuccess", True, None, None)

    def testContent(self):
        print '\n' + XmlEmitter.emitXmlContent("testContent", True, "http://localhost:8000", None)

    def testError(self):
        print '\n' + XmlEmitter.emitXmlContent("testError", False, None, "Can't pass this case")

    def testSuccess2Args(self):
        print '\n' + XmlEmitter.emitXmlContent("testSuccess2Args", True, "http://localhost:8000", "Can't pass this case")

    def testError2Args(self):
        print '\n' + XmlEmitter.emitXmlContent("testError2Args", False, "http://localhost:8000", "Can't pass this case")

    def testMultiContent(self):
        print '\n' + XmlEmitter.emitXmlMultiple("testMultiContent", True, 
            {'DirectUrl': "http://localhost:8000", 'IndirectUrl': "http://stacywebb.com"},
             "Can't pass this case")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSuccess']
    unittest.main()