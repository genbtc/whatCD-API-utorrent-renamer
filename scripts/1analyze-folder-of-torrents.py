#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Written under Python 2.7 for Windows, not tested on Python 3
#
# Code by genBTC. Created from scratch 10/6/2015.
#   
# Version 0.1 - functional since 10/9/2015.
# Version 0.1a - now uses directory paths obtained from settings, ss.Preferences() 10/14/2015
#
# Analyze a folder of .torrent's, and write out text files containing options such as infohash, torrentID, filename, internalname (utorrent "caption")
#
# Script #1: Run analyze-folder-of-torrents.py on the contents of your seeding.zip to generate a master list containing the torrentID, name, hash
#           automatically calculates/SHA1 hashes each torrent's [info] dict to get the info-hash
#           AND most importantly the artist along with the rest of the filename including such info as:
#               example:   Nirvana - Nevermind - 2013 (Blu-ray - FLAC - 24bit Lossless)-31112621.torrent
#   Info:   Master list of all the torrents you are seeding on what.cd (Profile -> Seeding [Download zip])
#           This is needed because this is the only way to properly get the "Artist" field as it was formatted by Gazelle (hard to believe but true)
#   reason: the API returns a RAW List of composers,dj,producers,conductor,remixedby,and artists and Gazelle uses this script-(i believe)
#           https://github.com/WhatCD/Gazelle/blob/master/classes/artists.class.php to format it as Human-readable with such intricacies as:
#               if ((count($Composers) > 0) && (count($Composers) < 3) && (count($MainArtists) > 0)) {
#                   $link .= ' performed by ';}

import bencode
import os
import hashlib
import codecs
from settings import Preferences


def main():
    ss = Preferences()
    script1sourcedir = ss.getwpath(u"script1sourcedir")+u''            #("seeding\"), needs unicode u for file opening.
    files = [os.path.join(script1sourcedir,filename) for filename in next(os.walk(script1sourcedir))[2]]        #gives absolute paths + names

    currentfile = 0

    container = []    #set up an empty container for desired data to get put into for later
    for eachfile in files:

        metainfo = bencode.decode_from_file(eachfile)
        # #need to manually SHA1 hash the torrent file's info-dict to get the info-hash
        infodict = metainfo['info']
        info_hash = hashlib.sha1(bencode.bencode(infodict)).hexdigest().upper()

        internalname = infodict['name']
        torrentfilename = eachfile[eachfile.rfind("\\")+1:]
        locextension = torrentfilename.find(".torrent")           #location of extension (char position)
        locid = torrentfilename.rfind("-")+1                      #location of torrentID (char position)
        torrentid = torrentfilename[locid:locextension]           #grab torrentID 
      
        container.append([torrentfilename, internalname, info_hash, torrentid])
        currentfile += 1 
        print currentfile, torrentfilename.encode('ascii', errors='ignore')     #console output is ascii only, cannot print unicode - chars are omitted

    #WRITE FILE 1
    writelistfile = codecs.open(ss.getwpath("outpath1"),'wb',"utf-8") # write-out a text file with torrentID and Hash (on one line) ("1seeding_ID+Hash+Filename.txt")
    for eachline in container:
        writelistfile.write(eachline[3] + " / " + eachline[2] + " / " + eachline[0] + "\n")     #output torrentID / Hash / torrentfilename
    writelistfile.close()


if __name__ == "__main__":
    main()  
