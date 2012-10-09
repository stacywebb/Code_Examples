#!/usr/bin/env python2.5

# diffs the files in two directories
# for each file in the source directory
# complain if it doesn't exist in the target directory
# or if there is a diff between source and target

import sys
import os
import difflib

def usage():
    print "usage: diffTextDirectories.py sourceDir targetDir"



def main(sourceDir, targetDir):

    # verify existence of source directory
    if os.path.exists(sourceDir) == False:
        print "sourceDir doesn't exist: %s" % sourceDir
        sys.exit(1)

    if os.path.isdir(sourceDir) == False:
        print "sourceDir not a directory: %s" % sourceDir
        sys.exit(1)

    # verify existence of target directory
    if os.path.exists(targetDir) == False:
        print "targetDir doesn't exist: %s" % targetDir
        sys.exit(1)

    if os.path.isdir(targetDir) == False:
        print "targetDir not a directory: %s" % targetDir
        sys.exit(1)

    # walk the sourceDirectory...
    for root, dirs, files in os.walk(sourceDir):

        # ignore svn directories
        if root.count('.svn') > 0:
            continue
        
        subDir = root.replace(sourceDir,'')
        targetSubDir = targetDir + subDir

        # check to see if targetSubDir exists
        if os.path.exists(targetSubDir) == False or os.path.isdir(targetSubDir) == False:
            print
            print "sourceDir %s not found at %s" % (root, targetSubDir)
            continue
       
        # verify that each file in root exists in targetSubDir
        count = 0
        for sourceFile in files:

            # skip symbolic links
            if os.path.islink(root + '/' + sourceFile):
                continue
           
            targetFile = targetSubDir + '/' + sourceFile
            if os.path.exists(targetFile) == False:

                # print header if this is the first missing file
                count = count + 1
                if count == 1:
                    print
                    print "Files in %s missing from %s" % (root, targetSubDir)

                print "\t%s" % (sourceFile)

        # verify that each file in root is indeed a file in targetSubDir
        count = 0
        for sourceFile in files:

            # skip symbolic links
            if os.path.islink(root + '/' + sourceFile):
                continue
           
            targetFile = targetSubDir + '/' + sourceFile
            if os.path.exists(targetFile) == True and os.path.isfile(targetFile) == False:

                # print header if this is the first missing file
                count = count + 1
                if count == 1:
                    print
                    print "Files in %s not valid files in %s" % (root, targetSubDir)

                print "\t%s" % (sourceFile)

        # now diff the source and target files
        count = 0
        for sourceFile in files:

            # skip symbolic links
            if os.path.islink(root + '/' + sourceFile):
                continue
           
            targetFile = targetSubDir + '/' + sourceFile
            if os.path.exists(targetFile) == True and os.path.isfile(targetFile) == True:
                sourceText = open(root + '/' + sourceFile, "r").readlines()
                targetText = open(targetFile, "r").readlines()
                result = difflib.unified_diff(sourceText, targetText)
                resultStr = ''.join(list(result))
                # for extraSpacing
                #resultStr = '\n'.join(list(result))
                if len(resultStr) > 0:
                    count = count + 1
                    if count == 1:
                        print
                        print "Diff for %s and %s" % (root, targetSubDir)

                    print
                    print "********************************"
                    print "\t%s" % (sourceFile)
                    print "********************************"
                    print resultStr
                    print "********************************"
                    print "********************************"


   
if __name__=='__main__':


    main('/var/simplesamlphp/config-templates', '/var/simplesamlphp/config')
    main('/var/simplesamlphp/metadata-templates', '/var/simplesamlphp/metadata')
