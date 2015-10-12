#!/usr/bin/env python
# -*- coding: utf-8 -*
#
## Written under Python 2.7 for Windows, not tested on Python 3
#
# Based on whatapi @ https://github.com/isaaczafuta/whatapi
# JSON what.cd api documentation found @ https://github.com/WhatCD/Gazelle/wiki/JSON-API-Documentation
#
# All original code by genBTC, 10/7/2015, version 0.1
#
# Alternate Script #3: Run alt3WhatCD-API_Downloader(by Hash).py to manually query the what.CD API by infoHash and pull down a response as JSON and dump to files
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
import cPickle as pickle
import json
import os
from itertools import islice

def main():

    currentline = 0   #to resume a broken download. set this to the last SUCCESSFUL number (due to 1 starting at 0) that you see was outputted to console

    cookies = pickle.load(open("E:\\rename-project\\scripts\\cookies.dat", 'rb'))   #cookies speed up the HTTP (supposedly)
    credentials = open("E:\\rename-project\\scripts\\credentials.txt", 'rb').readlines()  #store credentials in another file and .git-ignore it
    username = credentials[0].strip()
    password = credentials[1].strip()
      
    apihandle = whatapi.WhatAPI(config_file=None,username=username,password=password,cookies=cookies)

    #Can use torrentID instead of hashes if you use the word "id" instead of "hash" in the query
    filenamewithhashes  = "E:\\rename-project\\seeding10-7-HashOnly.txt"
    hashdir="E:\\rename-project\\hash-grabs2\\"      #output dir

    with open(filenamewithhashes,'r') as f:
        for currentHash in islice(f.read().splitlines(),currentline,None):     #will continue where it left off
            #currentHash = "E7A5718EC52633FCCB1EA85656AA0622543994D7"   #test hash for debugging
            try:
                response = apihandle.request(0, "torrent", hash=currentHash)["response"]       #talk to server and receive a response. the 0 means time.sleep(0).
            except whatapi.RequestException as e:
                currentline += 1
                print currentline, " ERROR. Your search did not match anything."                
                continue
            outfile = open(os.path.join(hashdir,currentHash), 'w')        
            json.dump(response,outfile)
            outfile.close()
            currentline += 1
            print currentline, ": ", currentHash

    pickle.dump(apihandle.session.cookies, open("E:\\rename-project\\scripts\\cookies.dat", 'wb'))  #store cookies when script ends, for next-run.

if __name__ == "__main__":
    main()