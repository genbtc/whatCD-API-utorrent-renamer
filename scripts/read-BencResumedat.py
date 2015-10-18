#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Written under Python 2.7 for Windows, not tested on Python 3
#
# Code by genBTC. Created from scratch 10/6/2015. 
#   
# Read uTorrent resume.dat and make a text file of EVERY torrent inside's "path", "caption", "infoHash"
# Version 0.1 - functional since 10/9/2015.
# Version 0.1a - now uses directory paths obtained from settings, ss.Preferences() 10/14/2015

import base64
from settings import Preferences
import os.path
import bencode

def main():

    ss = Preferences()

    torrentlist = bencode.decode_from_file(ss.get("utresumedat"))
    partiallist = []    # set up an empty container for desired data to get put into for later

    fileguarduseless = torrentlist.pop(".fileguard",None)
    rec = torrentlist.pop("rec",None)   #Remove this. 
    #(dict. comprehension expects only dicts as the root keys)
    #create a reverse lookup dict with "Dict comprehension". nice and simple eh? ;-)
    reverselookup={base64.b16encode(value["info"]):[value["path"],value["caption"],origkey] for origkey,value in torrentlist.iteritems()}
    for thehash,value in reverselookup.iteritems():
        partiallist.append([value[0],value[1],thehash])

    partiallist.sort()
    writelistfile = open(os.path.join(ss.get("maindir"),"TorrentList.txt"),'wb') # write-out a text file with one entry per line.
    for eachline in partiallist:
        writelistfile.write(eachline[0] + " / " + eachline[1] + " / " + eachline[2] + "\n")
                            #path           /   #caption          /     #infohash
    writelistfile.close()
    print "Finished writing: TorrentList.txt"


if __name__ == "__main__":
    main()  
