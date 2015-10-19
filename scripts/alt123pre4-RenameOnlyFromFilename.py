#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Written under Python 2.7 for Windows, not tested on Python 3
#
# Code by genBTC. Created from previous scripts 10/6/2015.
#   
# Version 0.1 - alt123pre4-RenameOnlyFromFilename.py  functional since 10/18/2015
#
# This version was provided for simplistic users to skip any confusion, and rename using the .torrent filename as the source of the name
# To do anything more complicated than just re-formatting information already provided in original the filename, you have to use the "#2 What.cd downloader script".
# There is a bit of regex quick help provided, for additional formatting in Notepad++ once the textfile is generated with this script.

    #File comes out in a format, where regex can be used:
    #    501 - Beat The System EP - 2013 (WEB - MP3 - 320)    
    #ex: artist - album - year - (media - format - encoding)

    #    ^(.*) - (.*) - (\d\d\d\d) (.*)
    #    $1 - $2 - $3 $4
    #to have year in parentheses, backslash escape them
    #    $1 - $2 \($3\) $4
    #    501 - Crystallize EP (2014) (WEB - MP3 - 320)

    #if you want to re-format the web mp3 320 part, you'll need to extract them as $4,$5,$6
    #    ^(.*) - (.*) - (\d\d\d\d) \((.*) - (.*) - (.*)\)
    #    $1 - $2 \($3\) $4/$5/$6
    #    501 - Crystallize EP (2014) WEB/MP3/320
    #keep in mind a filename with a forwardslash is banned, so you'd have to replace it with that unicode character like this:
    #    $1 - $2 \($3\) $4 ∕ $5 ∕ $6
    #    501 - Crystallize EP (2014) WEB ∕ MP3 ∕ 320
    #another formatting choice using square brackets:
    #    $1 - $2 \($3\) [$4 $5 $6]
    #    501 - Crystallize EP (2014) [WEB MP3 320]

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
        
        torrentfilename = torrentfilename[:locid-1]

        #####-------------replace banned characters with unicode section-----------------######
        ###
        # Forward slashes are strange. "FullWidth" is very wide and would be too wide if theres already spaces around it.
        torrentfilename = torrentfilename.replace(" / ",u"／")  # U+FFOF  (wide)       FULLWIDTH SOLIDUS
        # "Division" slash is too narrow and needs spaces inserted surrounding it (and is still less width than the fullwidth)
        torrentfilename = torrentfilename.replace("/",u" ∕ ")  # U+2215  (narrow)     DIVISION SLASH
        # Backslash (requires two slashes in python)
        torrentfilename = torrentfilename.replace("\\",u"＼")  # U+FF3C               FULLWIDTH REVERSE SOLIDUS
        # Colon
        torrentfilename = torrentfilename.replace(":",u"꞉")  # U+A789               MODIFIER LETTER COLON
        # asterisk
        torrentfilename = torrentfilename.replace("*",u"※")  # U+203B               REFERENCE MARK
        # question mark (replacement is backwards, sorry)
        torrentfilename = torrentfilename.replace("?",u"؟")  # U+061F               ARABIC QUESTION MARK
        # Double-quote
        torrentfilename = torrentfilename.replace('"',u"ʺ")  # U+02BA               MODIFIER LETTER DOUBLE PRIME
        # Left angle bracket
        torrentfilename = torrentfilename.replace("<",u"˂")  # U+02C2               MODIFIER LETTER LEFT ARROWHEAD
        # right angle bracket
        torrentfilename = torrentfilename.replace(">",u"˃")  # U+02C3               MODIFIER LETTER RIGHT ARROWHEAD
        # Pipe
        torrentfilename = torrentfilename.replace("|",u"ǀ")  # U+01C0               LATIN LETTER DENTAL CLICK
        ###
        #####----------windows filename banned chars replacement with unicode-----------######

        container.append([torrentfilename, internalname, info_hash, torrentid])
        currentfile += 1 
        print currentfile, torrentfilename.encode('ascii', errors='ignore')

    print "\nReminder: Console output is ascii only, Cannot Print Unicode. (chars omitted)"
    ##File Output. The Master List file of everything.##                    
    # when the loop exits, Sort it, and write it to the file.
    container.sort()
    writelistfile = codecs.open(ss.getwpath("outpath3"), 'wb', "utf-8")  # write-out a text file with one entry per line. main output file (3propernames.txt)
    for eachline in container:
        writelistfile.write(eachline[0] + " / " + eachline[2] + "\n")   #torrentname  / infohash
    writelistfile.close()
    print "Completed. Unicode File Written to: ", os.path.basename(ss.getwpath("outpath3"))


if __name__ == "__main__":
    main()  