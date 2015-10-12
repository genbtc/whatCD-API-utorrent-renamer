#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Written under Python 2.7 for Windows, not tested on Python 3
#
# Code by genBTC. Created from scratch 10/6/2015.  Relies on other pre-requisite steps that I scripted also.
#   
# Version 0.1 - functional since 10/10/2015.
#
# Script #5 - Make a new Resume.dat and commit the move/rename operations to disk
#
#Take the newly created proper names and open the Utorrent Resume.dat file and carefully replace the visual "Caption", and the actual path location.
#theoretically you could only replace the path, but then if you use "Set download location" to move the download to a new parent folder in the future,
#  it will use the caption to move it, and mess it up. So its better for the caption to match the path.
#After we write a NEW utorrent file (dont modify the existing one...) we make a "before" and "after" path file, for historical reference reasons.
#Then it goes ahead and moves the folders on the filesystem (its actually a rename operation=fast).
#
#Notes: This script was not very forgiving with the filename rename process: I think there should be some sort of better error handling, resume-on-error, undo, rollback or etc...
#
#NOTE #1: TO UNDO...=(if anything goes wrong, IMMEDIATELY !!!) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<IMPORTANT>>>>>>>>>>>>>>>>>>>>>>>>>
#
#    SWITCH variables BEFORE AND AFTER and run script again. THEN debug the issue. Do not manually change a filename to anything other than the beforepath or afterpath listed in the listfile
#
#TODO: Make this program output changes to file first, and before writing to utorrent resume.dat, pause indefinitely. Then user can edit the file meticulously, save and proceed with the move
#    with a file as an intermediate, you can scroll through and look at whats happening. 

import base64
import bencode
import codecs
import os.path
import time
import traceback

def main():
    #testdat = "E:\\rename-project\\EntireDAT.dat"
    olddat = "C:\\Users\\EOFL\\AppData\\Roaming\\uTorrent\\resume.dat"

    oldfile = open(olddat,'rb').read()

    newfile = open("E:\\rename-project\\NEWDAT.dat",'wb')
    namesandhashfile = codecs.open(u"E:\\rename-project\\propernames.txt",'rb',"utf-8").readlines()

    torrentlist = bencode.bdecode(oldfile)

    fileguarduseless = torrentlist.pop(".fileguard",None)
    rec = torrentlist.pop("rec",None)   #Remove this. 
    #interferes with the dict processing since it is a list
    #the next line dict. comprehension expects only dicts as the root keys
    #create a reverse lookup dict. nice and simple eh? ;-)
    reverselookup={base64.b16encode(value["info"]):[key,value["caption"],value["path"]] for key,value in torrentlist.iteritems()}

    #to modify paths in reverse lookup dict, start by getting the names and hash out of the namesandhashfile   
    for eachline in namesandhashfile:
        nameandhash = eachline.strip().split(' / ')   #strip out the \n with strip() and split on the " / " i put there as a seperator.
        theNewname = nameandhash[0]
        thehash = nameandhash[1]
        #searches the dict's keys for a Hash, if exists. and if so, can be used as the [indexid]
        if thehash in reverselookup:
            key = reverselookup[thehash][0]
            theOldPath = torrentlist[key]["path"]
            theNewPath = os.path.join(os.path.dirname(theOldPath),theNewname)
            torrentlist[key]["caption"] = theNewname
            torrentlist[key]["path"] = theNewPath
            if theNewname.endswith(".mp3") or theNewname.endswith(".flac"):     #.mp3 .flac = I personally didnt have any "Single file" .ogg, .aac, etc that needed special handling in this manner
                if torrentlist[key].has_key("targets"):                     #these lines are a quick fix, for an oversight in the uTorrent process. changing path is not enough
                    torrentlist[key]["targets"][0][1] = theNewname           #single-file-mode torrents have a "targets" list that controls the filename
                    #print torrentlist[key]["targets"] #debuginfo
            reverselookup[thehash].append(theNewname)
            reverselookup[thehash].append(theNewPath)
            # now the reverselookup dict looks like {Infohash : [key, caption, oldpath, newfilename, newpath] }    all info saved for later
            #                                       (key) : (value)[0 ,   1  ,    2   ,      3     ,   4    ] }            

    torrentlist["rec"]=rec   #add the thing we removed back in so we dont break anything (not sure what this is)
                            #fileguard does not need to go back, in fact, purposefully needs to stay out.
    newfile.write(bencode.bencode(torrentlist))
    newfile.close()

    beforeafterpath = u"E:\\rename-project\\beforepath-afterpath.txt"

    beforeafterfile = open(beforeafterpath,'wb')

    for key,value in reverselookup.iteritems():
        if len(value) == 5:
            try:
                beforeafterfile.write(value[2] + " / " +  value[4].encode("utf-8") + "\n")
            except:
                print "Error handling things, probably encoding/unicode error: \n", value[2],"\n",value[4].encode("utf-8")
    beforeafterfile.close()

    print "Finished. Wrote to:", newfile.name
    # print "You have 10 seconds to sort this file"
    # time.sleep(10)
#RENAME SECTION    
    print "Begin Renaming files......."
    beforeafterfile = open(beforeafterpath,'rb').readlines()
    for i in xrange(0, len(beforeafterfile), 1):
        beforeafter = beforeafterfile[i].strip().split(' / ')
        before = beforeafter[0].decode('utf-8')                 #NOTE #1: TO UNDO...=(if anything goes wrong, IMMEDIATELY !!!)
        after = beforeafter[1].decode('utf-8')                  #    SWITCH variables BEFORE AND AFTER and run script again. THEN debug the issue
        print i                                                 # do not manually change a filename to anything other than 
        try:                                                    # the beforepath or afterpath listed in the listfile
            if before != after:
                os.rename(before, after)
        except Exception as e:
            #traceback.print_exc()
            pass
#

if __name__ == "__main__":
    main()  