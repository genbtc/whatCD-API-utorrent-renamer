#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Coded for Python 3 (tested under Python 3.5 for Windows 64-bit)
#
# Code by genBTC. Created from scratch 10/6/2015. 
#   
# Version 0.1 - functional since 10/9/2015.
# Version 0.1a - now uses directory paths obtained from settings, ss.Preferences() 10/14/2015
# Version 0.1b - Changed code to target Python 3 @ 10/16/2015
#
# Read uTorrent resume.dat and make a text file of EVERY torrent inside's "path", "caption", "infoHash"

import base64
from settings import Preferences
import os.path
import bencode

def main():

    ss = Preferences()

    torrentlist = bencode.decode_from_file(ss.get("utresumedat"))
    partiallist = []    # set up an empty container for desired data to get put into for later

    fileguarduseless = torrentlist.pop(b".fileguard",None)
    rec = torrentlist.pop(b"rec",None)   #Remove this. 
    #(dict. comprehension expects only dicts as the root keys)
    #create a reverse lookup dict with "Dict comprehension". nice and simple eh? ;-)
    reverselookup={base64.b16encode(value[b"info"]):[value[b"path"],value[b"caption"],origkey] for origkey,value in torrentlist.items()}
    for thehash,value in reverselookup.items():
        partiallist.append([value[0].decode('utf-8'),value[1].decode('utf-8'),thehash.decode('utf-8')])
    #Those 3 lines replace all of this:
    # for key,value in torrentlist.items():
    #     sentinel = False    # reset before each while-loop
    #     if b"path" in value:
    #         path = value[b"path"].decode('utf-8')
    #     if b"caption" in value:
    #         caption = value[b"caption"].decode('utf-8')
    #     if b"info" in value:
    #         infoHash = base64.b16encode(value[b"info"]).decode('utf-8')
    #         sentinel = True  # need this because theres other dictionaries INside each file-entries' dict...
    #                          # and this will trigger the partiallist.append to write only file-entry dicts.
    #     if sentinel == True:
    #         partiallist.append([path,caption,infoHash])

    partiallist.sort()
    writelistfile = open(os.path.join(ss.get("maindir"),"TorrentList.txt"),'w',encoding='utf-8') # write-out a text file with one entry per line.
    for eachline in partiallist:
        writelistfile.write(eachline[0] + " / " + eachline[1] + " / " + eachline[2] + "\n")
        					#path 			/	#caption		  /		#infohash
    writelistfile.close()

if __name__ == "__main__":
    main()
