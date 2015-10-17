#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Coded for Python 3 (tested under Python 3.5 for Windows 64-bit)
#
# Code by genBTC. Created from scratch 10/6/2015.  Relies on other pre-requisite steps that I scripted also.
#   
# Version 0.1 - functional since 10/10/2015.
# Version 0.1a - now uses directory paths obtained from settings, ss.Preferences() 10/14/2015
# Version 0.1b - Changed code to target Python 3 @ 10/16/2015
#
# Script #4 - Make a new Resume.dat and commit the move/rename operations to disk
#
#1. Take the newly created proper names and open the Utorrent Resume.dat file and grabs 3 pieces of info, "caption,path,infohash".
#2. After we write a NEW utorrent file (dont modify the existing one...) we make a "before" and "after" path file, for historical reference reasons.
#3. Changes are outputted to a text file first, and with this file as an intermediate, you can scroll through and look at whats happening. 
#4. Before writing to utorrent resume.dat, or moving anything, it pauses until you press Enter to continue. 
#5. Then the user can edit the file meticulously, save and proceed with the operation. The new resume.dat file is written according to the possibly edited file.
#6. Only then does it move the folders on the filesystem (btw, its actually a rename operation = very fast).
#
#Notes: This script was not very forgiving with the filename rename process: I think there should be some sort of better error handling, resume-on-error, undo, rollback or etc...
#INFO:  Some of the above fixes have been attemped. 10/14/2015

import base64
import os.path
import traceback
from settings import Preferences
import bencode2en
import bencode
import decoder
import encode

def main():
    ss = Preferences()

    newfile = open(os.path.join(ss.get("maindir"),"NEWDAT.dat"),'wb')
    namesandhashfile = open(ss.getwpath("outpath3"),'r',encoding='utf-8').readlines()       #("3propernames.txt")

    beforeafterpath = ss.getwpath("outpath4")   #this holds the intermediate changes to happen before actually renaming so you have a chance to edit/change it. (4beforepath-afterpath.txt)

    #torrentlist = decoder.decode_from_file(ss.get("utresumedat"))  #works   10.645s 12315181 function calls
    #torrentlist = bencode2en.decode_from_file(ss.get("utresumedat")) #works 8.462s 13745202 function calls
    torrentlist = bencode.decode_from_file(ss.get("utresumedat"))  #works  8.057ss 10908143 function calls

    #These two things interfere with the processing on the next line 
    fileguarduseless = torrentlist.pop(b".fileguard",None)
    rec = torrentlist.pop(b"rec",None)   #Remove this. 
    #(dict. comprehension expects only dicts as the root keys)
    #create a reverse lookup dict with "Dict comprehension". nice and simple eh? ;-)
    reverselookup={base64.b16encode(value[b"info"]):[key,value[b"caption"],value[b"path"]] for key,value in torrentlist.items()}

    listofbeforeafter = []
    #to modify paths in reverse lookup dict, start by getting the names and hash out of the namesandhashfile   
    for eachline in namesandhashfile:
        nameandhash = eachline.strip().split(' / ')   #strip out the \n with strip() and split on the " / " i put there as a seperator.
        theNewname = nameandhash[0]
        thehash = nameandhash[1]
        #searches the dict's keys for a Hash, if exists. and if so, can be used as the [indexid]
        if bytes(thehash,'utf-8') in reverselookup:
            key = reverselookup[bytes(thehash,'utf-8')][0]
            theOldPath = torrentlist[key][b"path"].decode('utf-8')
            theNewPath = os.path.join(os.path.dirname(theOldPath),theNewname)
            if theOldPath != theNewPath:
                listofbeforeafter.append([theOldPath,theNewPath,thehash])   # make a list of a list (stringtoOutputtoFile=[0], hash=[1])            

    #sort, then write file detailing changes to path (before / after)
    listofbeforeafter.sort()
    beforeafterfile = open(beforeafterpath,'w',encoding='utf-8')
    for eachline in listofbeforeafter:
        #try:
        beforeafterfile.write(eachline[0] + " / " + eachline[2] + "\n")         #write oldpath + hash on 1st line    /The hash is duplicated for error checking in case the user accidentally bungles a character while editing...
        beforeafterfile.write(eachline[1] + " / " + eachline[2] + "\n")         #write newpath + hash on 2nd line   /
        #except:            
        #    print("Error writing the before+after file, probably a encoding/unicode error: \n", eachline[0],"\n",eachline[1])
    beforeafterfile.close()

    #At this point the script pauses, and asks the user to confirm changes shown in the beforepath-afterpath.txt file
#    input("Press Enter to begin Renaming files.......\\> ")  #wait for the user to press Enter before continuing with anything.

    #WRITE TORRENT RESUME.DAT
    beforeafterfile = open(beforeafterpath,'r',encoding='utf-8').readlines()
    for i in range(0, len(beforeafterfile), 2):
        beforeandhash = beforeafterfile[i].strip().split(' / ')
        afterandhash = beforeafterfile[i+1].strip().split(' / ')
        before = beforeandhash[0]
        beforehash = beforeandhash[1]
        after = afterandhash[0]
        afterhash = afterandhash[1]
        if beforehash == afterhash:
            thehash = beforehash
        else:
            print("Error. You have inadvertently modified one of the hash files, and there is a hash mismatch between before/after entries.")
            print("Cannot continue. Exiting. Please save your changes into a new file, locate your error, and re-run and fix it...")
            print("Another possibility is you were missing a / (with 1 character of whitespace on each side surrounding it) as a seperator.")
        #searches the dict's keys for a Hash, if exists. and if so, can be used as the [indexid]
        if bytes(thehash,'utf-8') in reverselookup:
            key = reverselookup[bytes(thehash,'utf-8')][0]
            torrentlist[key][b"caption"] = bytes(after[after.rfind("\\")+1:],'utf-8')
            try:
               # prints a number to console to show progress. corresponds to the numbers in the file (every-two-lines).  (tip:) to show incremental numbers use (((i+1)/2)+1) 
               # filenames printed to console, will be missing any unicode chars because the windows console is not unicode compatible!!!! (annoying)
                print(i,before.encode('ascii', errors='ignore').decode())
                print(i+1,after.encode('ascii', errors='ignore').decode())
                os.rename(before, after)
            except Exception as e:
                traceback.print_exc()       #will output any errors to console but keep going
            torrentlist[key][b"path"] = bytes(after,'utf-8')
            if after.endswith(".mp3") or after.endswith(".flac"):     #.mp3 .flac = I personally didnt have any "Single file" .ogg, .aac, etc that needed special handling in this manner
                if b"targets" in torrentlist[key]:                     #these lines are a quick fix, for an oversight in the uTorrent process. changing path is not enough
                    torrentlist[key][b"targets"][0][1] = torrentlist[key][b"caption"]           #single-file-mode torrents have a "targets" list that controls the filename

        torrentlist[b"rec"]=rec   #add the thing we removed back in so we dont break anything (not sure what this is)
                                #fileguard does not need to go back, in fact, purposefully needs to stay out.
    #newfile.write(encode.encode(torrentlist))       #works    10.295s 15361310 function calls
    #newfile.write(bencode2en.bencode2(torrentlist)) #v.slow  31.872s 12452142 function calls
    #newfile.write(bencode2en.bencode4(torrentlist))  #works   7.864s 10906619 function calls
    newfile.write(bencode.bencode(torrentlist))     #works    7.699s 10906619 function calls
    newfile.close()
    print("\nPlease note that the filenames shown are missing any unicode characters due to Windows Command Prompt limitations.")
    print("Finished writing: ", newfile.name)


if __name__ == "__main__":
    main()  
    # PROFILING:
# if __name__ == "__main__":
#     import cProfile, pstats
#     cProfile.run("main()", "{}.profile".format(__file__))
#     s = pstats.Stats("{}.profile".format(__file__))
#     s.strip_dirs()
#     s.sort_stats("time").print_stats(25)