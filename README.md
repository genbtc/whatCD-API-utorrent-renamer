# whatCD-API-utorrent-renamer 
For Windows (Python 2.7)
## Overall Description
Queries the API for all your seeding torrents to download all possible metadata. 
Renames all your what.cd downloads to have a proper and uniform name. 
Also modifies uTorrent resume.dat to keep seeding after the renaming.

## Script #1: *1analyze-folder-of-torrents.py*
Analyze a folder of .torrent's, and write 2 files containing options such as infohash, torrentID, filename, internalname (utorrent "caption")
## Script #2: *2WhatCD-API_Downloader(by ID).py*
Automatically query the whatCD API by torrentID for every .torrent and pull down a response as JSON and dump to files. 
This script is throttled to 30 torrents per minute, so prepare to wait a few hours. 
The download is small (mine was 10.0MB for 4163 files) since it is just ~2-3KB of metadata each.
## Script #3: *3create-proper-names.py*
All naming decisions happen here. You should/must edit this file to suit yourself, especially "Sorted_Record_Labels_List" 
This program takes the results of Script #1,#2 and re-builds from scratch the desired filename.
## Script #4: *4write-uT-resumedat.py*
Make a new Resume.dat and commit the move/rename operations to disk

## Instructions:
I tried to make this as straightforward as possible, but it's really advanced. 
You should know some programming language, even if its not python because python is very easy to learn and modify.
I used as many comments and descriptive variable names as I could to document what is going on
The naming decisions take place in Script 3 and contain MY DEFAULTS. In the future I will adapt this github to be more generic.

1. Download this repository as a .zip file (button over there >>>^^^^^) and extract it to E:\rename-project\
   If you extract it somewhere else, you will need to change all the paths in all the scripts.
   
2. Create a "credentials.txt" in the scripts\ folder containing your whatcd username on the first line and your whatcd password on the second line

3. Go on your profile on whatcd and on the bottom-right-corner, find "Seeding: [Show stats] [View] [Download]" and click the Download link to download a zipfile of all the torrents you are seeding named username's-Seeding.zip.
   This can be fairly large (52MB for 4163 files) but does not count towards your ratio. Open it, go  into the subfolder containing the torrents, and Extract them all to the seeding\ dir.
   To be clear, you should have *.torrent files in \seeding\ now and nothing else.

4. Open the scripts 1-4 in your text editor and modify the directory paths to match up or do a bulk-find-and-replace on E:\\rename-project\\
   Make sure you use double backslashes for your paths. This is how it needs to be done for python on windows.  
   Script 4 contains a path/reference to C:\Users\EOFL\Appdata\Local\utorrent\resume.dat, make sure you change "EOFL" to your username, or change the entire path to point to your resume.dat
   Don't worry your resume file will not be written to.

5. Delete the file in the hash-grabs\ dir (I only put that there to make a blank dir on github)

6. Run Script 1 and 2 and wait for 2 to complete(hours). Each one should generate a text file in the rename-project\ parent dir. You should inspect these to see what happened. 
   Also don't worry, you will only have to run script 2 once.
   While you are waiting for script 2, open Script #3 and start reading the comments/documentation
   At this point you will need to figure out the renaming pattern I scripted, and modify it to suit yourself.
   
7. Run Script 3. It will generate a text file containing the newly decided names, which you should check, and then run Script 4.

8. Halfway through Script 4, it gives you the chance to modify any files in the text file "beforepath-afterpath.txt" You should examine this and 

9. Shut down uTorrent, renaming your resume.dat file to resume.dat.old (remove the existing one), move the NEWDAT.dat that was created, and rename that to be the new resume.dat. 
   At this point you can run the optional script: read-BencResumedat.py which will double-check your resume-dat file and output every single torrent inside's 3 relevant bits of info ("Caption","path","Hash") to a text file "TorrentList.txt" for those who are paranoid.    (to run this optional script you need to change the path its looking for the resume.dat file at)

10. Start uTorrent, and marvel at your nicely renamed library and still seeding files :)

### Other Scripts are not part of the process: 
#### *read-BencResumedat.py*
Read uTorrent resume.dat and make a text file of EVERY torrent inside's "path", "caption", "infoHash"
#### *post3makelist-from-hashgrabs.py*
Reads the results of Script 3 and makes a textfile list of hashes and proper names to be used later. You can modify this to personally grab any data out of the JSON download files that you might want.
Perhaps you want to capture the "wikiBody" information inside it and dump them into a .txt file in the music folder. 
Perhaps you want to capture the wikiImage to download album art.
#### *altpre1sort-folder-of-torrents-by-tracker.py*
Takes a large dumpfolder of torrents, and sort them into folders based on which tracker it has in the ["announce"] field.
(useful if you save every torrent from every site like me)
Note: There is an issue where some torrents use an ["announce-list"] field to list multiple trackers. This makes them go into the "None" folder. You can easily fix this with a bit of python, but it didn't affect me much.
#### *alt2WhatCD-API_Downloader(by Hash).py*
If for some reason you arent using the seeding.zip and instead you chose to use the results of "altpre1sort-folder-of-torrents-by-tracker.py", then the torrents likely will not have the -TorrentID appended onto the end of them. In that case, you will need to use THIS Downloader (by Hash) which is slower. I have not figured out any other faster way to get ID's out of an hash, and the query to the API to get the ID is the same time/work as returning the entire JSON dict.... Just stick to the normal script.... literally:)
#### *Dependencies*: Bencode.py, BTL.py, munkres.py, whatapi.py (contain my modifications)
#### *Unused*: bencode2en.py, torrent-torrent.py, torrent-group.py