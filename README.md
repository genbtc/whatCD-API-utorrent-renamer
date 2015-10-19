# whatCD-API-utorrent-renamer 
For Windows, Python 2.7 - and now Python 3! (use scripts3 folder instead)
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
Confirm new filenames,Make a new Resume.dat and commit the move/rename operations to disk

## Instructions:
I tried to make this as straightforward as possible, but it's really advanced. 
You should know some programming language, even if its not python because python is very easy to learn and modify.
I used as many comments and descriptive variable names as I could to document what is going on
The naming decisions take place in Script 3 and contain MY DEFAULTS. In the future I will adapt this github to be more generic.

1. Download this repository as a .zip file (button over there >>>^^^^^) and extract it somewhere, ie: E:\rename-project\
   
2. Create a "credentials.txt" in the scripts\ folder containing your whatcd username on the first line and your whatcd password on the second line

3. Delete the files in the hash-grabs\ and hash-grabs-as-filenames\ dirs. (I only put them there to make blank dirs on github)
   Then, delete the blank text file that I put in the seeding\ folder, because you will do what it says in the next step.

4. Go on your profile on whatcd and on the bottom-right-corner, find "Seeding: [Show stats] [View] [Download]" and click the Download link to download a zipfile of all the torrents you are seeding named username's-Seeding.zip.
   This can be fairly large (52MB for 4163 files) but does not count towards your ratio. Then open the .zip of torrents you downloaded, go into the subfolder containing the torrents themselves, and Extract them all to the seeding\ dir.
   To be clear, you should have *.torrent files in seeding\ now and nothing else (do not extract the summary file or the dated folder).

5. Run Script 1 and 2 and wait for 2 to complete. Script #2 might take hours to download but, don't worry, it is resume capable and you will only have to download once.
   Each one should generate some text files in the rename-project\ parent dir. You should inspect these to see what happened. 
   While you are waiting for script 2, open Script #3 in a text editor and start reading the comments/documentation.
   At this point you will need to figure out the torrent renaming pattern I scripted, and modify it to suit yourself.
   
6. Run Script 3. It will generate a text file ("3propernames.txt") containing the newly decided names, which you should double-check that the script made good decisions.
   (Don't edit this file. You will have a chance to do that later).
  
7. At this point you need to edit scripts\settings.ini and provide it the proper location to utorrent's resume.dat file. Do not edit anything else in there.

8. Run Script 4. Halfway through Script 4 it will pause, and prompt you before renaming any files. This gives you the chance to edit any filenames in the text file "beforepath-afterpath.txt".
   You should examine this and edit/change it to suit yourself. The next instructions are so you don't mess anything up while editing:
   The format is OldPath1 / Hash1, (next line), NewPath1 / Hash1. The OldPath is on Line1, the NewPath is on Line2. Do NOT modify the OldPath or it wont be able to find it..... Only modify the 2nd line (The new path). The hash is duplicated on both lines for error checking in case the user accidentally bungles a character while editing... 
   Also the " / " was put there as a seperator, Dont Modify that either and make sure theres not extra spaces.   
   After you finish editing and save the text file, press [ENTER] to continue renaming and save the new resume.dat file as NEWDAT.dat.

9. Shut down uTorrent (wait a few secs + check task manager), rename your current resume.dat file to resume.dat.old (remove the existing .old), move the NEWDAT.dat file into the right location, and rename that to be the new resume.dat. 
   At this point you can run the optional script: "read-BencResumedat.py" which will double-check your resume-dat file and output every single torrent's 3 relevant bits of info ("Caption","path","Hash") to a text file "TorrentList.txt" for those who are paranoid.

10. Done! Start uTorrent, and marvel at your nicely renamed library and still seeding files :)

### Other Scripts are not part of the process: 
#### *alt123pre4-RenameOnlyFromFilename.py* 
Instead of running scripts 1,2,3 this just takes the name directly from torrent filename itself (with regex), and does not rely on any data from the What.CD API. Example: 
Before: 501 - Crystallize EP - 2014 (WEB - MP3 - 320)-31846936.torrent
After : 501 - Crystallize EP (2014) [WEB MP3 320]
Keep in mind you will need to use regex on the file to get your desired results. I have included a quick guide in the comments of this script.
This generates a text file that is ready to be used by Script #4 as per usual.
#### *read-BencResumedat.py*
Read uTorrent resume.dat and make a text file of EVERY torrent inside's "path", "caption", "infoHash"
#### *post3makelist-from-hashgrabs.py*
Reads the results of Script 3 and makes a textfile list of hashes and proper names to be used later. You can modify this to personally grab any data out of the JSON download files that you might want.
Perhaps you want to capture the "wikiBody" information inside it and dump them into a .txt file in the music folder. 
Perhaps you want to capture the wikiImage to download album art.
#### *altpre1sort-folder-of-torrents-by-tracker.py*
Takes a large dumpfolder of torrents, and sort them into folders based on which tracker it has in the ["announce"] field. (useful if you save every torrent from every site like me)
Note: There is an issue where some torrents use an ["announce-list"] field to list multiple trackers. This makes them go into the "None" folder. You can easily fix this with a bit of python, but it didn't affect me much.
#### *alt2WhatCD-API_Downloader(by Hash).py*
If for some reason you arent using the seeding.zip and instead you chose to use the results of "altpre1sort-folder-of-torrents-by-tracker.py", then the torrents likely will not have the -TorrentID appended onto the end of them. In that case, you will need to use THIS Downloader (by Hash) which is slower. I have not figured out any other faster way to get ID's out of an hash, and the query to the API to get the ID is the same time/work as returning the entire JSON dict.... Just stick to the normal script.... literally:)
#### *Dependencies*: torrentclass.py, settings.py, bencode.py, encoder.py, whatapi.py (contain my modifications)
#### *Unused*: bencode2en.py