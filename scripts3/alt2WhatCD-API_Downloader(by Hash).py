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
# Alternate Script #2: Run alt2WhatCD-API_Downloader(by Hash).py to query the what.CD API by infoHash and pull down a response as JSON and dump to files
#
# whatapi was edited slightly to change time.sleep(2) to be time.sleep(0) when issuing a request
# # Querying Based on ID's is WAYYY faster.. (46 requests in 60sec) vs. 20-22 items per minute with hash as a query
# napkin calculations:
#    Even though 2 seconds per request is correct (max 5 requests in 10 secs), the server has its own delays
# # in 60 seconds, we got 16 requests with 1 second of sleep each
# # time.sleep(1) * 46 = 16 seconds of sleep in internal waits
# # 44 seconds of actual server time per 16 requests = 2.75 seconds per request
# # Need 1 request every 2 seconds, so do not need to sleep at all.

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

    filenamewithIDs = ss.getwpath("outpath2")   # ("1seeding_ID+Hash.txt")
    hashdir = ss.getwpath("script2destdir")      #output dir

    openedfile = open(filenamewithIDs,'r',encoding='utf-8').readlines()
    for eachline in islice(openedfile,currentline,None):     #will continue where it left off
        idandhash = eachline.strip().split(' / ')
        currentID = idandhash[0]
        currentHash = idandhash[1]     
        if not os.path.exists(os.path.join(hashdir,currentHash)):
            #currentHash = "E7A5718EC52633FCCB1EA85656AA0622543994D7"   #test hash for debugging
            try:
                response = apihandle.request(0, "torrent", hash=currentHash)["response"]       #talk to server and receive a response. the 0 means time.sleep(0).
            except whatapi.RequestException as e:
                currentline += 1
                print(currentline, " ERROR. Your search did not match anything.")                
                continue
            with open(os.path.join(hashdir,currentHash), 'w') as outfile:
                json.dump(response,outfile, sort_keys = True)
            currentline += 1
            print(currentline, ": ", currentHash)

    pickle.dump(apihandle.session.cookies, open(ss.getwpath("cookiesfile"), 'wb'))  #store cookies when script ends, for next-run.
    print("Download Complete.")

if __name__ == "__main__":
    main()