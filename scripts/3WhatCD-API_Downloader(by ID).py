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
# Script #3: Run 3WhatCD-API_Downloader(by ID).py to manually query the what.CD API by torrentID and pull down a response as JSON and dump to files
#
# Querying Based on ID's is WAYYY faster.. Able to hit 46 requests in a minute with time.sleep(1)...... need to increase wait time a little.
#napkin calculations:
#in 60 seconds, we got 46 requests with 1 second of sleep each
#time.sleep(1) * 46 = 46 seconds of sleep in internal waits
#14 seconds of actual server time per 46 requests = 0.30434782608695652173913043478261 seconds per request
#Need 1 request every 2 seconds, so need to sleep for 1.7 seconds

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
    
    #Can use hashes instead of torrentID if you use the word "hash" instead of "id" in the query
    filenamewithIDs  = "E:\\rename-project\\seeding10-7-IDOnly.txt"
    hashdir="E:\\rename-project\\hash-grabs2-ID\\"      #output dir

    with open(filenamewithIDs,'r') as f:
        for currentID in islice(f.read().splitlines(),currentline,None):     #will continue where it left off
            try:
                response = apihandle.request(1.75, "torrent", id=currentID)["response"]       #talk to server and receive a response
            except whatapi.RequestException as e:
                currentline += 1
                print currentline, " ERROR. Your search did not match anything."                
                continue
            currentHash = response["torrent"]["infoHash"]
            outfile = open(os.path.join(hashdir,currentHash), 'w')        
            json.dump(response,outfile)
            outfile.close()
            currentline += 1
            print currentline, ": ", currentID

    pickle.dump(apihandle.session.cookies, open("E:\\rename-project\\scripts\\cookies.dat", 'wb'))  #store cookies when script ends, for next-run.

if __name__ == "__main__":
    main()