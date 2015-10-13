#!/usr/bin/env python
# -*- coding: utf-8 -*

# Written under Python 2.7 for Windows, not tested on Python 3
#
# Code by genBTC. Created from scratch 10/6/2015.  Relies on other pre-requisite steps 1,2 that I scripted also.
#   
# Version 0.1 - functional since 10/9/2015.
#
# Script #3: Renames all your what.cd downloads to have a proper and uniform name.
#       All naming decisions happen here. You should/must edit this file to suit yourself, especially "Sorted_Record_Labels_List" 
#       This program takes the results of Script #1,#2  and re-builds from scratch the desired filename.
#       This was built specific to my needs, the what and why of which needs explaining:
#
# FUNCTIONALITY notes:
#
#   1. The Sorted_Record_Labels_List is a list of record labels that I wish to store SORTED by the catalog number such as [DMZ001] (at the start of the filename)
#       this causes the program to omit output of a {Digital Mystikz} tag near the end, as its obvious to me because I have these stored in named folders.
#   1b. Any Record labels not part of this list will have the {Record Label} tag at the end BUT the catalog number omitted entirely.
#   1c. In the catalog number I removed all spaces, and converted it all to uppercase.
#   2. Much confusion arose from "Torrentobj.torrent.remastered" Edition which is a flag where different editions can have 4 modified fields: (year,name) and 2 of which (catalog,tor.group.recordLabel)
#       needed special handling.  Upon careful inspection, about 1% of these had flawed data in some way, and the code is very branched and unclear, although i did my best.
#       I handled as many edge cases as possible while trying to ascertain whether to use the original fields or the tor.torrent.remastered edition fields. 
#       You would want to debug how these "Guesses" apply to your library and I am working on a way to delay changes until the end for confirmation or something.
#   3. The ReleaseType field (EP, Album) - fully listed below - I wanted to be handled so it would be displayed in [] on all files, but [Album] seemed redundant to me.
#       EP also got redundant as some albums are named as "The Something EP" [EP] so if the name ended in EP, i just omitted the bracketed [EP] as well.
#   3b. The (Blu-ray - FLAC - 24bit Lossless) seemed too long so i settled on just [FLAC 100%] for log FLACs or just [FLAC] and I dont have many 24-bits, so I skipped it.
#   3c. For MP3, I omitted the word MP3, and for VBR i omitted the words VBR. example: [WEB 320] [CD V0]
#   3d. For Torrentobj.torrent.scene releases, i just replaced the word [WEB] with [Torrentobj.torrent.scene] since its redundant to me, and there was no easy way to grab the Torrentobj.torrent.scene Group's name.
#   3e. For AAC, i searched the tor.torrent.description and tor.torrent.filepath (what the original torrent owner names it) for 'itunes' and if found, tagged it as [iTunes AAC].
#       tor.torrent.filePath is the field that goes into uTorrent, but is too unpredictable overall - even though it can contain valid info found nowhere else sometimes.
#       (actually, that field is what this program is attempting to correct, and there will be a followup program to re-import the new name back into uTorrent to seed)
#   4. The last thing the program does is re-copy all the tor.torrent.infoHash JSON files into the new-proper-name filenames, JUST FOR REFERENCE to have later. (easily deletable)
#       My advice to read these humanly, is to use Notepad++ with the plugin called JSON Viewer (http://nppjsonviewer.sourceforge.net/) or some other JSON viewer.
#       To use: CTRL+A (Select All) and CTRL+ALT+SHIFT+M (Torrentobj.torrent.format as JSON). Don't resave it, or there will be a ton of \t tabs and \n newlines in the saved file and will screw it up.
#   4b. Please note that simply renaming a .torrent file to the new-names will not affect the Bencoded tor.torrent.filePath inside and thus will not seed to that location, and there is no way 
#       to modify the tor.torrent.filePath inside the torrent even with a BEncode Editor, because this will change the value of the tor.torrent.infoHash and will come up as "Torrent not recognized"
#
# PROGRAMMATICALLY, the following is explained:
#
#   1. Useful comments were left along the way as i went
#   2. My python is mediocre at best, so if you're wondering why I coded it Z way instead of X or Y its because I however it came to mind is how it got coded.
#       And step-by-step readability was preferred over abstraction.
#   3. I went through hell with the ascii vs unicode vs mbcs filesystem encodings and HTML-unescaped JSON, and this is just how I cobbled it all together to work.
#   4. While I NEEDED to grab the artist from the torrent filename, for some reason I got the album, year from it. This is for no reason.
#   5. The filenames needed to be sanitized from Windows's banned character list of \ / : * ? " < > | and have been replaced by Unicode looking clones 
#       except the ? which I could only find a backwards looking replacement for.

# CODING TODO LIST:
# instead of  grabbing album,year from filename, grab from named hash JSON-dump file
# think of better naming concepts
# an idea: $1 $2 $3 beginning middle end, select which pieces of the program to write as the new name
# might be a good idea to create an undo.dat file
# *DONE*maybe sort the master list output file alphabetically
# save list of  files the program modified unusually
# wait till the end to display list of errors
# *DONE*refactor->create a class or wrapper function to hold the response[] (the shell of which can be borrowed from torrent-torrent.py,torrent-group.py)
# *DONE*(see bottom)profile performance and figure out what is the most cpu intensive part, and improve performance
# use multiple threads to process many things at once. (Caps out at 12% per Core) so 8 threads would be way faster, and SSD usage is at a minimum (1-5%)
# Unify the tor.torrent.encoding schemes and remove as many conversions as possible and just stick to unicode for everything.
# lastly,create better way to interface with people other than myself / editing source code magic strings

import bencode
import base64
import sys
import os
import hashlib
from urlparse import urlparse
import time
import json
from enum import Enum
import ntpath
import re
import codecs
import HTMLParser
import shutil
import difflib
from torrentclass import Torrent


class ReleaseType(Enum):
    Unspecified = 0
    Album = 1
    Soundtrack = 3
    EP = 5
    Anthology = 6
    Compilation = 7
    DJ_Mix = 8
    Single = 9
    Live = 11
    Remix = 13
    Bootleg = 14
    Interview = 15
    Mixtape = 16
    Unknown = 21
    Concert = 22
    Demo = 23


Sorted_Record_Labels_List = ["abducted",
"abducted dub",
"abducted limited",
"abducted records",
"armada captivating",
"armada deep",
"big apple",
"butterz",
"buygore",
"chestplate",
"circus",
"deep medi",
"disciple",
"dmz",
"digital mystikz",
"dub police",
"eatbrain",
"firepower",
"hyperdub",
"kannibalen",
"kapsize",
"luckyme",
"mainstage music",
"mau5trap",
"monstercat",
"musical freedom",
"nest",
"never say die",
"nsd:",
"osiris music",
"owsla",
"play me",
"prime audio",
"revealed",
"rottun",
"smog",
"storming",
"sub soldiers",
"subhuman",
"swamp81",
"swamp 81",
"symbols",
"tempa",
"ultragore",
"zouk" ]


class TorrentEntry:
    def __init__(self):
        self.hash = None
        self.pathname = None
        self.filename = None
        self.artistalbum = None
        self.torrentid = None
        self.createdpropername = None
        self.fmttdMediaEncodeFormat = ""


def getUniqueWords(iterable):
    seen = set()
    result = []
    for item in iterable:
        if item.lower() not in seen:  # compare lowercases
            seen.add(item.lower())
            result.append(item)  # but preserve actual case
    return result  # return a list (in order)


def main():
    global fmttdcatalogueNumber
    hashtorrlistfile = u"E:\\rename-project\\seeding_Hash_-_Torr.txt"
    directory_path = u"E:\\rename-project\\hash-grabs\\"  # needs a unicode symbol so os. commands work at all on paths with funny chars
    allfiles = [os.path.join(directory_path, fn) for fn in
                next(os.walk(directory_path))[2]]  # gives absolute paths + names

    currentfilenumber = 1

    writelistfile = codecs.open(u"E:\\rename-project\\propernames.txt", 'wb',
                                "utf-8")  # write-out a text file with one entry per line.
    writelistcontainer = []
    hashtofilenamefolder = u"E:\\rename-project\\hash-grabs-as-filenames\\"

    for hashidfilename in allfiles:  # iterate through filenames of what.cd JSON data

        with open(hashidfilename, 'r') as stringfile:  # open them
            needFixLabeltoNewEdition = False

            jsonresponse = json.load(stringfile)
            tor = Torrent(jsonresponse)

            if tor.group.categoryName != "Music":
                continue  # do not continue altering any non-music torrents.

            releaseTypeName = ReleaseType(tor.group.releaseType).name  # turn int. value into a string using the enum class above
            fmttdreleaseTypeName = "[" + releaseTypeName + "]"

            if tor.torrent.remastered:
                if tor.torrent.remasterTitle:
                    tor.group.name += " (" + tor.torrent.remasterTitle + ")"
                if tor.torrent.remasterYear > tor.group.year:
                    tor.group.year = tor.torrent.remasterYear
                if tor.torrent.remasterRecordLabel:
                    if tor.group.recordLabel.lower() != tor.torrent.remasterRecordLabel.lower():  # so not case sensitive
                        if not tor.group.recordLabel:
                            tor.group.recordLabel = tor.torrent.remasterRecordLabel
                        else:
                            # then things get complicated and we need to figure out which Label/catalog field is the best one to use, or combine them or both
                            needFixLabeltoNewEdition = True

                # if its been determined that its a remaster (new edition), process new label and catalog
                #  checking whether to combine with old, or which one to use, etc, etc.....
                if needFixLabeltoNewEdition == True:

                    score = difflib.SequenceMatcher(None, tor.group.recordLabel.lower(), tor.torrent.remasterRecordLabel.lower()).ratio()
                    if (score < 0.5):
                        # considered similar at 0.6 but this way is not that accurate. if they are lower than 0.5 similar, just use the new one
                        tor.group.recordLabel = tor.torrent.remasterRecordLabel
                        if tor.torrent.remasterCatalogueNumber:
                            tor.group.catalogueNumber = tor.torrent.remasterCatalogueNumber  # if tor.torrent.remasterCatalogueNumber is not blank, use it as the new tor.group.catalogueNumber

                    elif all(word in tor.torrent.remasterRecordLabel.lower() for word in tor.group.recordLabel.lower()) \
                            or \
                            all(word in tor.group.recordLabel.lower() for word in tor.torrent.remasterRecordLabel.lower()):
                        # If all the words in the old label is encompassed in the new one, use the new one.
                        # This would mean the new edition record label is most likely longer and is similar enough to use that,
                        # and preferred, since its more applicable to this specific release anyway.
                        # Even if the reverse is true, this code-block should only catch labels that differ in slight ways.

                        # example 1: originallabel={Big Beat Records}  remasterlabel={Big Beat}          #elif new label in old label
                        #   result:     {Big Beat}                                                      #or
                        # example 2: originallabel={Big Beat}  remasterlabel={Big Beat Records}          #if old label in new label
                        #   result:     {Big Beat Records}                                              #then
                        tor.group.recordLabel = tor.torrent.remasterRecordLabel  # always choose new label.
                        if tor.torrent.remasterCatalogueNumber:
                            tor.group.catalogueNumber = tor.torrent.remasterCatalogueNumber  # if tor.torrent.remasterCatalogueNumber is not blank, use it as the new tor.group.catalogueNumber
                    else:
                        # This else-block is used when the above are not true, and we can't decide on which one to use, so we use both. Combined.

                        # example 1: originallabel={Island Records}  remasterlabel={Island Records / Lokal Legend}
                        #   result:     {Island Records / Lokal Legend}
                        # example 2: originallabel {Wall Recordings}  remasterlabel={Tiger Records}
                        #   result:     {Wall Recordings / Tiger Records}  
                        new = ""
                        splitorig = re.sub("[(,),-]", " ",
                                           tor.group.recordLabel).split()  # remove delimiter chars that mess up stuff
                        sepchar = ["/"]
                        splitnew = re.sub("[(,),-]", " ", tor.torrent.remasterRecordLabel).split()  # turn everything into a list

                        new = " ".join(["%s" % (v) for v in getUniqueWords(
                            splitorig + sepchar + splitnew)])  # append unique words to the orig.

                        if tor.torrent.remasterCatalogueNumber:
                            if tor.group.catalogueNumber != tor.torrent.remasterCatalogueNumber:
                                if tor.group.catalogueNumber:
                                    tor.group.catalogueNumber += " / " + tor.torrent.remasterCatalogueNumber
                                else:
                                    tor.group.catalogueNumber = tor.torrent.remasterCatalogueNumber
                        tor.group.recordLabel = new

            iterhashfile = open(hashtorrlistfile, 'rb').readlines()  # read everything into memory
            for i in xrange(0, len(iterhashfile), 2):  # read (hashes) on every other line
                # ntpath.basename was really slow so doing it manually.... (32 times faster)= 0.128 seconds vs 0.004 seconds
                hashfilesepidloc = hashidfilename.rfind("\\") + 1
                if iterhashfile[i].strip() == hashidfilename[hashfilesepidloc:]:  # if it matches, start processing
                    newEntry = TorrentEntry()  # instanciate class
                    newEntry.hash = iterhashfile[i].strip()  # store Hash for reference
                    newEntry.pathname = iterhashfile[i + 1].strip().decode("utf-8")  # filename + extension
                    locextension = newEntry.pathname.find(".torrent")  # location of extension
                    locid = newEntry.pathname.rfind("-") + 1  # location of tor.torrent.id
                    newEntry.filename = newEntry.pathname[:locextension]  # chop the extension off (manually)
                    newEntry.artistalbum = newEntry.filename[:locid - 1]  # JUST the name (no ID#)
                    newEntry.torrentid = newEntry.filename[
                                         locid:locextension]  # grab ID for future reference (tor.torrent.id on what.cd)
                    # example : S-Type - Billboard (Lido Remix) - 2014 (WEB - MP3 - 320)
                    newEntry.artist = newEntry.artistalbum[:newEntry.artistalbum.find(" - ")]  # grab artist
                    tempalbum = newEntry.artistalbum[newEntry.artistalbum.find(
                        " - ") + 3:]  # temp value helps with string processing
                    newEntry.album = tempalbum[:tempalbum.find(" - ")]  # not needed since it can be pulled from [group]
                    newEntry.year = tempalbum[tempalbum.find(" - ") + 3:tempalbum.find(
                        " - ") + 7]  # not needed since it can be pulled from [group]

                    # ------------Recreate name------------#
                    # -------Special RULES SECTION---------#
                    newEntry.createdpropername = newEntry.artist + u" - " + tor.group.name + " "
                    if tor.group.releaseType > 1:  # dont put it for Album or Unspecified
                        if tor.group.releaseType != 5:  # do something different for EP
                            newEntry.createdpropername += fmttdreleaseTypeName + " "
                        else:  # make a rule so [EP] doesnt come up if there is " EP " already
                            if tor.group.name[-2:] != "EP":
                                newEntry.createdpropername += fmttdreleaseTypeName + " "

                    newEntry.createdpropername += "(" + str(tor.group.year) + ")"

                    # written like this for easy humanreading
                    #           tor.torrent.format = MP3, FLAC, AAC,
                    #          tor.torrent.media = cd, web, vinyl, soundboard, dat
                    #        tor.torrent.encoding = lossless,320,v0,256,v2,192
                    if tor.torrent.format == "FLAC":
                        newEntry.fmttdMediaEncodeFormat = "FLAC"
                        # log and tor.torrent.logscore only applicable to flac.
                        if tor.torrent.hasLog:
                            newEntry.fmttdMediaEncodeFormat += " " + str(
                                tor.torrent.logScore) + "%"  # the % implies "log" so leave out the word log
                    if tor.torrent.format == "AAC":
                        if (any("itunes" in word.lower() for word in tor.torrent.description.split())) or (
                        any("itunes" in word.lower() for word in tor.torrent.filePath.split())):
                            newEntry.fmttdMediaEncodeFormat = "iTunes "
                        newEntry.fmttdMediaEncodeFormat += "AAC"
                    if tor.torrent.format == "MP3":
                        # dont actually write mp3
                        # only write Scene or WEB if it is an mp3
                        if tor.torrent.scene:
                            newEntry.fmttdMediaEncodeFormat += "Scene"
                        elif tor.torrent.media == "WEB":
                            newEntry.fmttdMediaEncodeFormat += "WEB"
                        else:
                            newEntry.fmttdMediaEncodeFormat += tor.torrent.media
                        if "VBR" in tor.torrent.encoding:
                            newEntry.fmttdMediaEncodeFormat += " " + tor.torrent.encoding[:2]
                        else:
                            newEntry.fmttdMediaEncodeFormat += " " + tor.torrent.encoding

                    newEntry.fmttdMediaEncodeFormat = "[" + newEntry.fmttdMediaEncodeFormat + "]"

                    newEntry.createdpropername += " " + newEntry.fmttdMediaEncodeFormat

                    # put catalog number in brackets
                    if tor.group.catalogueNumber:
                        fmttdcatalogueNumber = ("[" + tor.group.catalogueNumber + "]").replace(" ", "").upper()
                    elif tor.group.recordLabel:
                        fmttdcatalogueNumber = "[" + tor.group.recordLabel + "]"  # combines with next part to put the tor.group.recordLabel in the front if Cat# missing

                    if any(word in tor.group.recordLabel.lower() for word in Sorted_Record_Labels_List):  # so not case sensitive
                        newEntry.createdpropername = fmttdcatalogueNumber + " " + newEntry.createdpropername
                    elif tor.group.recordLabel:
                        newEntry.createdpropername += " " + "{" + tor.group.recordLabel + "}"
                        # if tor.group.catalogueNumber:                                                       #This will put [CATA###] after all releases, even labels not in your list
                        #     newEntry.createdpropername += " " + fmttdcatalogueNumber              #Gets kind of cumbersome for me. (uncomment to use it anyway)

                    # these 2 lines are a quick fix, for an oversight in my naming process
                    # if these are single file .mp3's (or a single .flac) they will need a .mp3 at the end of the filename
                    if not tor.torrent.filePath:
                        newEntry.createdpropername += "." + tor.torrent.format.lower()

                    try:
                        print currentfilenumber, newEntry.createdpropername
                    except:
                        print "COULD NOT PRINT UNICODE FILENAME TO CONSOLE. HASH=", tor.torrent.infoHash
                        # pass

                    ########-------------replace characters section----------------#########
                    newEntry.createdpropername = newEntry.createdpropername.replace("\\",u"＼")  # U+FF3C               FULLWIDTH REVERSE SOLIDUS
                    # these forward slashes are strange. "FullWidth" is very wide and would be too wide if theres already spaces around it.
                    newEntry.createdpropername = newEntry.createdpropername.replace(" / ",u"／")  # U+FFOF  (wide)       FULLWIDTH SOLIDUS
                    # "Division" slash is too narrow and needs spaces inserted surrounding it (and is still less width than the fullwidth)
                    newEntry.createdpropername = newEntry.createdpropername.replace("/",u" ∕ ")  # U+2215  (narrow)     DIVISION SLASH
                    newEntry.createdpropername = newEntry.createdpropername.replace(":",u"꞉")  # U+A789               MODIFIER LETTER COLON
                    newEntry.createdpropername = newEntry.createdpropername.replace("*",u"※")  # U+203B               REFERENCE MARK
                    newEntry.createdpropername = newEntry.createdpropername.replace("?",u"؟")  # U+061F               ARABIC QUESTION MARK
                    newEntry.createdpropername = newEntry.createdpropername.replace('"',u"ʺ")  # U+02BA               MODIFIER LETTER DOUBLE PRIME
                    newEntry.createdpropername = newEntry.createdpropername.replace("<",u"˂")  # U+02C2               MODIFIER LETTER LEFT ARROWHEAD
                    newEntry.createdpropername = newEntry.createdpropername.replace(">",u"˃")  # U+02C3               MODIFIER LETTER RIGHT ARROWHEAD
                    newEntry.createdpropername = newEntry.createdpropername.replace("|",u"ǀ")  # U+01C0               LATIN LETTER DENTAL CLICK
                    #####--windows filename banned chars replacement with unicode--#########

                    ######----------HashGrabs-as-Filenames--------########
                    # File output. Move all files named as hashes to a new dir as the proper name
                    if not os.path.exists(hashtofilenamefolder + newEntry.createdpropername):
                        shutil.copy(hashidfilename, hashtofilenamefolder + newEntry.createdpropername)
                    # else:
                    #     #print "**"*80
                    #     print currentfilenumber,hashidfilename,newEntry.createdpropername
                    #     print "**"*80

                    currentfilenumber += 1
                    #####------------make propernames.txt (has the hash in it also) ---------########
                    ##File Output. The Master List file of everything.##
                    # Add it to the container (since this is in a loop)
                    writelistcontainer.append(newEntry.createdpropername + " / " + tor.torrent.infoHash + "\n")
    # when the loop exits, Sort it, and write it to the file.
    writelistcontainer.sort()
    for eachline in writelistcontainer:
        writelistfile.write(eachline)
    writelistfile.close()


if __name__ == "__main__":
    main()

    # PROFILING:
    # if __name__ == "__main__":
    #     import cProfile, pstats
    #     cProfile.run("main()", "{}.profile".format(__file__))
    #     s = pstats.Stats("{}.profile".format(__file__))
    #     s.strip_dirs()
    #     s.sort_stats("time").print_stats(10)


    # Sun Oct 11 00:19:57 2015    create-proper-names.py.profile
    #          35543736 function calls (35543709 primitive calls) in 28.724 seconds
    #    Ordered by: internal time
    #    List reduced from 171 to 10 due to restriction <10>
    #
    #    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    #         1   14.085   14.085   28.723   28.723 create-proper-names.py:175(main)
    #  17309720    4.716    0.000    4.716    0.000 {method 'rfind' of 'unicode' objects}
    #      4161    4.478    0.001    4.478    0.001 {method 'readlines' of 'file' objects}
    #  17313841    1.725    0.000    1.725    0.000 {method 'strip' of 'str' objects}
    #     16565    1.007    0.000    1.007    0.000 {open}
    #      4120    0.501    0.000    1.700    0.000 shutil.py:66(copyfile)
    #     16481    0.492    0.000    0.492    0.000 {nt.stat}
    #      4163    0.349    0.000    0.349    0.000 decoder.py:372(raw_decode)
    #     12418    0.251    0.000    0.251    0.000 {method 'read' of 'file' objects}
    #      4120    0.152    0.000    0.152    0.000 {nt.chmod}