# whatCD-API-utorrent-renamer 
For Windows (Python 2.7)
## Overall Description
Queries the API for all your seeding torrents to download all possible metadata. 
Renames all your what.cd downloads to have a proper and uniform name. 
Also modifies uTorrent resume.dat to keep seeding after the renaming.

## Script #1: *1read-BencResumedat.py*
Read uTorrent resume.dat and make a text file of EVERY torrent inside's "path", "caption", "infoHash"
## Script #2: *2analyze-folder-of-torrents.py*
Analyze a folder of .torrent's, and write 2 files containing options such as infohash, torrentID, filename, internalname (utorrent "caption")
## Script #3: *3WhatCD-API_Downloader(by ID).py*
Automatically query the whatCD API by torrentID for every .torrent and pull down a response as JSON and dump to files. 
This script is throttled to 30 torrents per minute, so prepare to wait a few hours. 
The download is small (mine was 10.0MB for 4163 files) since it is just ~2-3KB of metadata each.
## Script #4: *4create-proper-names.py*
All naming decisions happen here. You should/must edit this file to suit yourself, especially "Sorted_Record_Labels_List" 
This program takes the results of Script #1,#2,#3 and re-builds from scratch the desired filename.
## Script #5: *5write-uT-resumedat.py*
Make a new Resume.dat and commit the move/rename operations to disk

## Instructions:
I tried to make this as straightforward as possible, but it's really advanced. 
You should know some programming language, even if its not python because python is very easy to learn and modify.
I used as many comments and descriptive variable names as I could to document what is going on
The naming decisions take place in Script 4 and contain MY DEFAULTS. In the future I will adapt this github to be more generic.

1. Download this repository as a .zip file (button over there >>>^^^^^) and extract it to E:\rename-project\
   If you extract it somewhere else, you will need to change all the paths in all the scripts.
   
2. Create a "credentials.txt" in the scripts\ folder containing your whatcd username on the first line and your whatcd password on the second line

3. Go on your profile on whatcd and on the bottom-right-corner, find "Seeding: [Show stats] [View] [Download]" and click the Download link to download a zipfile of all the torrents you are seeding named username's-Seeding.zip.
   This can be fairly large (52MB for 4163 files) but does not count towards your ratio. Open it, go  into the subfolder containing the torrents, and Extract them all to the seeding\ dir.
   To be clear, you should have *.torrent files in \seeding\ now and nothing else.

4. Open the scripts 1-5 in your text editor and modify the directory paths to match up or do a bulk-find-and-replace on E:\\rename-project\\
   Make sure you use double backslashes for your paths. This is how it needs to be done for python on windows.
   
5. Script 1 and 5 contain a path/reference to C:\Users\EOFL\Appdata\Local\utorrent\resume.dat, make sure you change "EOFL" to your username, or change the entire path to point to your resume.dat
   Don't worry your resume file will not be written to.

6. Delete the file in the hash-grabs\ dir (I only put that there to make a blank dir on github)

7. Run Script 1,2,3 and wait for 3 to complete(hours). Each one should generate a text file in the rename-project\ parent dir. You should inspect these to see what happened. 
   Also don't worry, you will only have to run script 3 once.
   While you are waiting for script 3, open Script #4 and start reading the comments/documentation
   At this point you will need to figure out the renaming pattern I scripted, and modify it to suit yourself.
   
8. Run Script 4. It will generate a text file, which you should check, and then run Script 5.

9. Shut down uTorrent, back-up your resume.dat file, and replace it with the file NEWDAT.dat that was created.

10. Start uTorrent, and marvel at your nicely renamed library and still seeding files :)

