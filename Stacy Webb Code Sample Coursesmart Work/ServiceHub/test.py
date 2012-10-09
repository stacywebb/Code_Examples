__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'


import hashlib
from util.CyclingMessageDigest import CyclingMessageDigest

userId = '30886'
acctId = '122869'
loginCycleLength = 1000000

searchIndex = 800000
searchToken = ''

anchors = [acctId, userId]

mdGenerator = CyclingMessageDigest(loginCycleLength)
for i in range(0,loginCycleLength):
    token = mdGenerator.generateMessageDigest(anchors, i)
    if i == searchIndex:
        searchToken = token
        print i,":",searchToken
    
print token

print "Searching for token at",searchIndex

print mdGenerator.indexOfCycleWithinSeries(anchors, searchToken)
    
