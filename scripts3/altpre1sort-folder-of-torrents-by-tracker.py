#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Coded for Python 3 (tested under Python 3.5 for Windows 64-bit)
#
# Code by genBTC. Created from scratch 10/6/2015.  Relies on other pre-requisite steps that I scripted also.
#   
# Version 0.1 - functional since 10/9/2015.
# Version 0.1a - now uses directory paths obtained from settings, ss.Preferences() 10/14/2015
# Version 0.1b - Changed code to target Python 3 @ 10/16/2015
#              - Changed BDecoder and use sleeker methods, now handles [announce-list] as "multiple trackers"

# Takes a bulk folder of .torrents and sorts them into folders named with the tracker it uses.


import bencode
import os
from urlparse import urlparse
from settings import Preferences


def main():
    ss = Preferences()  #settings.1py

    directory_path = os.path.join(ss.get("maindir"),u"All-Torrs\\")    #needs a unicode symbol so os. commands work at all on paths with funny chars

    files = [os.path.join(directory_path,fn) for fn in next(os.walk(directory_path))[2]]        #gives absolute paths + names

    torrentnamelist = []
    for eachfile in files:
        with open(eachfile,'rb') as stringfile:
            try:
                torrent = bencode.decode(stringfile.read())
                for key,value in torrent.iteritems():
                    if key == "announce":
                        announce = value
                        domain = '{uri.netloc}'.format(uri=urlparse(announce))
                        colon = domain.find(':',0)
                        if colon != -1:
                            domain = domain[:colon]
                        if domain:
                            tracker = domain      #only using 1 value here(lazy)
                    elif key == "announce-list":
                        tracker = "Multiple Trackers"
            except:
                tracker = "None"
        torrentfilename = eachfile[eachfile.rfind("\\")+1:]

        if not os.path.exists(directory_path + tracker):
            os.makedirs(directory_path + tracker)
        os.rename(eachfile, os.path.join(directory_path + tracker + "\\" + torrentfilename))


if __name__ == "__main__":
    main()  
