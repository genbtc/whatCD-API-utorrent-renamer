#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Coded for Python 3 (tested under Python 3.5 for Windows 64-bit)
#
# Based on whatapi @ https://github.com/isaaczafuta/whatapi
# JSON what.cd api documentation found @ https://github.com/WhatCD/Gazelle/wiki/JSON-API-Documentation
#
# All original code by genBTC, 10/7/2015, version 0.1
# Version 0.1a - now uses directory paths obtained from settings, ss.Preferences() 10/14/2015
# Version 0.1b - Changed code to target Python 3 @ 10/16/2015
#
# Script #2: Run 2WhatCD-API_Downloader(by ID).py to query the what.CD API by torrentID and pull down a response as JSON and dump to files
#
# Querying Based on ID's is WAYYY faster.. Able to hit 46 requests in a minute with time.sleep(1)...... need to increase wait time a little.
#napkin calculations:
#in 60 seconds, we got 46 requests with 1 second of sleep each
#time.sleep(1) * 46 = 46 seconds of sleep in internal waits
#14 seconds of actual server time per 46 requests = 0.30434782608695652173913043478261 seconds per request
#Need 1 request every 2 seconds, so need to sleep for 1.7 seconds


import whatapi
import pickle # py3k support    
import json
import os
from itertools import islice
from settings import Preferences


def main():
    ss = Preferences()

    currentline = 0   #to resume a broken download. set this to the last SUCCESSFUL number (due to 1 starting at 0) that you see was outputted to console
    try:
        cookies = pickle.load(open(ss.getwpath("cookiesfile"), 'rb'))   #cookies speed up the HTTP (supposedly)
    except:
        cookies = None          #if we cant load it, don't use it.
    credentials = open(ss.getwpath("credentialsfile"), 'rb').readlines()  #store credentials in another file and .git-ignore it
    username = credentials[0].strip()
    password = credentials[1].strip()
    
    apihandle = whatapi.WhatAPI(config_file=None,username=username,password=password,cookies=cookies)
    
    filenamewithIDs = ss.getwpath("outpath1")   # ("1seeding_ID+Hash+Filename.txt")
    hashdir = ss.getwpath("script2destdir")      #output dir

    openedfile = open(filenamewithIDs,'r',encoding='utf-8').readlines()
    for eachline in islice(openedfile,currentline,None):     #will continue where it left off
        idandhash = eachline.strip().split(' / ')
        currentID = idandhash[0]
        currentHash = idandhash[1]        
        if not os.path.exists(os.path.join(hashdir,currentHash)):
            #currentHash = "E7A5718EC52633FCCB1EA85656AA0622543994D7"   #test hash for debugging
            try:
                response = apihandle.request(1.75, "torrent", id=currentID)["response"]       #talk to server and receive a response
            except whatapi.RequestException as e:
                currentline += 1
                print(currentline, " ERROR. Your search did not match anything.")                
                continue
            with open(os.path.join(hashdir,currentHash), 'w') as outfile:
                json.dump(response,outfile, sort_keys = True)
            currentline += 1
            print(currentline, ": ", currentID)

    pickle.dump(apihandle.session.cookies, open(ss.getwpath("cookiesfile"), 'wb'))  #store cookies when script ends, for next-run.
    print("Download Complete.")

if __name__ == "__main__":
    main()