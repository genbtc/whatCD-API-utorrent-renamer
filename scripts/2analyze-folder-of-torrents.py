#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Written under Python 2.7 for Windows, not tested on Python 3
#
# Code by genBTC. Created from scratch 10/6/2015.
#   
# Version 0.1 - functional since 10/9/2015.
#
# Analyze a folder of .torrent's, and write 2 files containing options such as infohash, torrentID, filename, internalname (utorrent "caption")
#
# Script #2: Run analyze-folder-of-torrents.py on the contents of your seeding.zip to generate a master list containing the torrentID,
#           automatically calculates/SHA1 hashes each torrent's [info] dict to get the info-hash
#           AND most importantly the artist along with the rest of the filename including such info as:
#           example:   Nirvana - Nevermind - 2013 (Blu-ray - FLAC - 24bit Lossless)-31112621.torrent

import bencode
import base64
import sys
import os
import hashlib
import codecs

def bdecodetext(text):
    torrentnamelist = [] 
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

            name = ""    #initialize

            while text[start] != 'e':
                key, start = bdecode_next(start)
                value, start = bdecode_next(start)
                res[key] = value

                if key == "name":
                    name = res["name"].decode("utf-8")
                    torrentnamelist.append(name)
                
            return res, start + 1

        lenend = text.find(':', start)
        length = int(text[start:lenend], 10)
        end = lenend + length + 1
        return text[lenend+1:end], end    

    bdecode_next(0) #run the encode recurseively.
    return torrentnamelist[0]  #give the stored list back to the main function so it can be written out


def main():

    #directory_path = u"E:\\rename-project\\torrents1\\"
    #directory_path = u"E:\\rename-project\\D-All-Torr\\tracker.what.cd\\"
    #directory_path = u"D:\\RandomMisc\\ABC - filetime fakedata\\"
    #directory_path = u"C:\\uTorrents\\2\\finished\\"
    directory_path = u"E:\\rename-project\\seeding10-7\\"

    files = [os.path.join(directory_path,fn) for fn in next(os.walk(directory_path))[2]]        #gives absolute paths + names

    container = []    #set up an empty container for desired data to get put into for later
    for eachfile in files:
        stringfile = open(eachfile,'rb').read()
        internalname = bdecodetext(stringfile)
        torrentfilename = eachfile[eachfile.rfind("\\")+1:]

        #need to manually SHA1 hash the torrent file's info-dict to get the info-hash
        metainfo = bencode.bdecode(stringfile)
        info = metainfo['info']
        info_hash = hashlib.sha1(bencode.bencode(info)).hexdigest().upper()
        
        container.append([torrentfilename, internalname, info_hash])

    #------Idea 1---------
    # writelistfile = open(u"E:\\rename-project\\Torrent-to-Name_MappingList.txt",'w') # write-out a text file with [filename,internalname,infohash]
    # for eachline in container:
    #     writelistfile.write(eachline[0] + " / " + eachline[1] + " / " + eachline[2] + "\n")
    # writelistfile.close()
    # writelistfile = open(u"E:\\rename-project\\Name-to-Torrent_MappingList.txt",'w') # write-out a text file with [internalname,filename,infohash]
    # for eachline in container:
    #     writelistfile.write(eachline[1] + " / " + eachline[0] + " / " + eachline[2] + "\n")
    # writelistfile.close()

    #------Idea 2---------(using codecs.open to write and utf-8 encoding)
    # writelistfile = codecs.open(u"E:\\rename-project\\D-All-Torr\\ALLTorrent-to-Name_List.txt",'wb',"utf-8") # write-out a text file with [filename,internalname,infohash]
    # for eachline in container:
    #     writelistfile.write(eachline[0] + u" / " + eachline[1] + " / " + eachline[2] + "\n")
    # writelistfile.close()
    # writelistfile = codecs.open(u"E:\\rename-project\\D-All-Torr\\ALLName-to-Torrent_List.txt",'wb',"utf-8") # write-out a text file with [internalname,filename,infohash]
    # for eachline in container:
    #     writelistfile.write(eachline[1] + u" / " + eachline[0] + " / " + eachline[2] + "\n")
    # writelistfile.close()

    #------Idea 3---------
    # writelistfile = codecs.open(u"E:\\rename-project\\seeding10-7_TorrNameHash.txt",'wb',"utf-8") # write-out a text file with [filename,internalname,infohash]
    # for eachline in container:
    #     writelistfile.write(eachline[0] + u" / " + eachline[1] + " / " + eachline[2] + "\n")
    # writelistfile.close()
    # writelistfile = codecs.open(u"E:\\rename-project\\seeding10-7_NameTorrHash.txt",'wb',"utf-8") # write-out a text file with [internalname,filename,infohash]
    # for eachline in container:
    #     writelistfile.write(eachline[1] + u" / " + eachline[0] + " / " + eachline[2] + "\n")
    # writelistfile.close()
    # writelistfile = codecs.open(u"E:\\rename-project\\seeding10-7_HashTorrName.txt",'wb',"utf-8") # write-out a text file with [infohash,filename,internalname]
    # for eachline in container:
    #     writelistfile.write(eachline[2] + u" / " + eachline[0] + " / " + eachline[1] + "\n")
    # writelistfile.close()
    writelistfile = codecs.open(u"E:\\rename-project\\seeding10-7_Hash_-_Torr.txt",'wb',"utf-8") # write-out a text file with [infohash \n filename]
    for eachline in container:
        writelistfile.write(eachline[2] + "\n")
        writelistfile.write(eachline[0] + "\n")
    writelistfile.close()

    #------Idea 4---------
    # writelistfile = codecs.open(u"E:\\rename-project\\seeding10-7_TorrentName+ID.txt",'wb',"utf-8") # write-out a text file with only filename(includes ID)
    # for eachline in container:
    #     writelistfile.write(eachline[0] + "\n")
    # writelistfile.close()

    #------Idea 5---------
    # writelistfile = codecs.open(u"E:\\rename-project\\seeding10-7-HashOnly.txt",'wb',"utf-8") # write-out a text file with only infohash
    # for eachline in container:
    #     writelistfile.write(eachline[2] + "\n")
    # writelistfile.close()

    #------Idea 6---------
    writelistfile = codecs.open(u"E:\\rename-project\\seeding10-7-IDOnly.txt",'wb',"utf-8") # write-out a text file with only ID
    for eachline in container:
        locextension = eachline[0].find(".torrent")           #location of extension
        locid = eachline[0].rfind("-")+1                      #location of torrentID
        torrentid = eachline[0][locid:locextension]      #grab torrentID 
        writelistfile.write(torrentid + "\n")
    writelistfile.close()


if __name__ == "__main__":
    main()  
