#!/usr/bin/env python
# -*- coding: utf-8 -*

# Coded for Python 3 (tested under Python 3.5 for Windows 64-bit)
#
# Code by genBTC. Created from scratch 10/6/2015.  Relies on other pre-requisite steps that I scripted also.
#   
# Version 0.1 - functional since 10/9/2015.
# Version 0.1a - now uses directory paths obtained from settings, ss.Preferences() 10/16/2015
# Version 0.1b - Changed code to target Python 3 @ 10/16/2015
#
# Preliminary program to make a list of hashes and proper names to be used later. Was combined into the main Script #3.

import os
import json
import codecs
from settings import Preferences

def main():

    ss = Preferences()
    directory_path = ss.getwpath("script3destdir")  #("hash-grabs-as-filenames" dir)
    allfiles = [os.path.join(directory_path,fn) for fn in next(os.walk(directory_path))[2]]        #gives absolute paths + names

    writelistfile = codecs.open(ss.getwpath("outpath3"), 'wb', "utf-8") #("3propernames.txt" file)
    for hashidfilename in allfiles:  #iterate through filenames of what.cd JSON data
        with open(hashidfilename,'r') as stringfile: #open them
            response = json.load(stringfile)
            torrentHash= response["torrent"]["infoHash"]     #grab the hash To compare.            
            writelistfile.write(hashidfilename[hashidfilename.rfind("\\")+1:] + " / " + torrentHash + "\n")            #File Output. The Master List file of the names and hashes.
    writelistfile.close()

if __name__ == "__main__":
    main()  
