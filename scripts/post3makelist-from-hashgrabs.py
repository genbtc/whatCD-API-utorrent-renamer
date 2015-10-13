#!/usr/bin/env python
# -*- coding: utf-8 -*

# Written under Python 2.7 for Windows, not tested on Python 3
#
# Code by genBTC. Created from scratch 10/6/2015.  Relies on other pre-requisite steps that I scripted also.
#   
# Version 0.1 - functional since 10/9/2015.
#
# Preliminary program to make a list of hashes and proper names to be used later.

import os
import json
import ntpath
import codecs

def main():

    directory_path = u"E:\\rename-project\\hash-grabs-as-filenames\\"    #needs a unicode symbol so os. commands work at all on paths with funny chars
    allfiles = [os.path.join(directory_path,fn) for fn in next(os.walk(directory_path))[2]]        #gives absolute paths + names

    writelistfile = codecs.open(u"E:\\rename-project\\propernames+hash.txt",'wb',"utf-8") # write-out a text file with one entry per line.
    for hashidfilename in allfiles:  #iterate through filenames of what.cd JSON data
        with open(hashidfilename,'r') as stringfile: #open them
            response = json.load(stringfile)
            torrentHash= response["torrent"]["infoHash"]     #grab the hash To compare.            
            writelistfile.write(hashidfilename[hashidfilename.rfind("\\")+1:] + " / " + torrentHash + "\n")            #File Output. The Master List file of the names and hashes.
    writelistfile.close()

if __name__ == "__main__":
    main()  
