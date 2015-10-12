#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Written under Python 2.7 for Windows, not tested on Python 3
#
# Code by genBTC. Created from scratch 10/6/2015.  Relies on other pre-requisite steps that I scripted also.
#   
# Version 0.1 - functional since 10/9/2015.
# Takes a bulk folder of .torrents and sorts them into folders named with the tracker it uses.

import bencode
import base64
import sys
import os
import hashlib
from urlparse import urlparse
import time

def bdecodetext(text):
    torrentnamelist = []    #container (list) = (will only ever contain 1 string cause...lazy. will rewrite later)
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

            announce = ""    #initialize
            domain = ""

            while text[start] != 'e':
                key, start = bdecode_next(start)
                value, start = bdecode_next(start)
                res[key] = value

#THIS WAS MODIFIED, DONT FORGET
                if key == "announce":
                    announce = res["announce"]
                    domain = '{uri.netloc}'.format(uri=urlparse(announce))
                    colon = domain.find(':',0)
                    if colon != -1:
                        domain = domain[:colon]
                    if domain:
                        torrentnamelist.append(domain)      #only using 1 value here(lazy)
#                
            return res, start + 1

        lenend = text.find(':', start)
        length = int(text[start:lenend], 10)
        end = lenend + length + 1
        return text[lenend+1:end], end    

    bdecode_next(0) #run the decode recurseively.
    try:                           #give the stored list back to the main function so it can be written out
        return torrentnamelist[0]  #    [0] = using a list for only 1 value here (lazy code-reuse)
    except:
        return "None"


def main():

    directory_path = u"E:\\rename-project\\D-All-Torr\\"    #needs a unicode symbol so os. commands work at all on paths with funny chars

    files = [os.path.join(directory_path,fn) for fn in next(os.walk(directory_path))[2]]        #gives absolute paths + names

    for eachfile in files:
        with open(eachfile,'rb') as stringfile:
            try:
                tracker = bdecodetext(stringfile.read())
            except:
                tracker = "None"
        torrentfilename = eachfile[eachfile.rfind("\\")+1:]

        #print tracker, " / ", torrentfilename          #errors out when console can't print codepage

        if not os.path.exists(directory_path + tracker):
            os.makedirs(directory_path + tracker)
        os.rename(eachfile, os.path.join(directory_path + tracker + "\\" + torrentfilename))

if __name__ == "__main__":
    main()  
