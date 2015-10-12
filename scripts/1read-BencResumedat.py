#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Written under Python 2.7 for Windows, not tested on Python 3
#
# Code by genBTC. Created from scratch 10/6/2015. 
#   
# Version 0.1 - functional since 10/9/2015.
#
# Read uTorrent resume.dat and make a text file of EVERY torrent inside's "path", "caption", "infoHash"
#
# Script #1: Master list of all the torrents you are seeding on what.cd (Profile -> Seeding [Download zip])
#           This is needed because this is the only way to properly get the "Artist" field as it was formatted by Gazelle (hard to believe but true)
#   reason: the API returns a RAW List of composers,dj,producers,conductor,remixedby,and artists and Gazelle uses this script-(i believe)
#           https://github.com/WhatCD/Gazelle/blob/master/classes/artists.class.php to format it as Human-readable with such intricacies as:
#               if ((count($Composers) > 0) && (count($Composers) < 3) && (count($MainArtists) > 0)) {
#                   $link .= ' performed by ';}

import base64
import bencode

def bdecodetext(text):
    torrentlist = []    #set up an empty container for desired data to get put into for later
    def bdecode_next(start):

        if text[start] == 'i':  #process ints
            end = text.find('e', start)
            return int(text[start+1:end], 10), end + 1
        
        if text[start] == 'l':  #process the lists
            res = []
            start += 1
            while text[start] != 'e':
                elem, start = bdecode_next(start)
                res.append(elem)
            return res, start + 1

        if text[start] == 'd':  #process every dict
            res = {}
            start += 1
            caption = ""    #initialize
            path = ""       # and
            info = ""       #info-hash
            sentinel = False    #reset before each while-loop
            while text[start] != 'e':
                key, start = bdecode_next(start)
                value, start = bdecode_next(start)
                res[key] = value

                if key == "caption":
                    caption = res["caption"]
                if key == "info":
                    info = res["info"]
                if key == "path":
                    path = res["path"]
                    sentinel = True #need this because theres other dictionaries INside each file-entries' dict...
                                 #  and this will trigger the torrentlist.append to write only file-entry dicts.
            if sentinel == True:
                torrentlist.append([path,caption,info])
            return res, start + 1

        lenend = text.find(':', start)
        length = int(text[start:lenend], 10)
        end = lenend + length + 1
        return text[lenend+1:end], end    

    bdecode_next(0) #run the decode recurseively.
    return torrentlist  #give the stored list back to the main function so it can be written out


def main():

    #olddat = "E:\\rename-project\\settings.dat"
    #olddat = "E:\\rename-project\\EntireDAT.dat"
    #olddat = "C:\\uTorrents\\2\\resume.dat"    
    olddat = "C:\\Users\\EOFL\\AppData\\Roaming\\uTorrent\\resume.dat"

    datfile = open(olddat,'rb').read()
    torrentlist = bdecodetext(datfile)

    writelistfile = open("E:\\rename-project\\TorrentList.txt",'w') # write-out a text file with one entry per line.
    for eachline in torrentlist:
        writelistfile.write(eachline[0] + " / " + eachline[1] + " / " + base64.b16encode(eachline[2]) + "\n")
        					#path 			/	#caption		  /		#infohash
    writelistfile.close()

if __name__ == "__main__":
    main()  
