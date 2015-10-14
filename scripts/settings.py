#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Written under Python 2.7 for Windows, not tested on Python 3
#
# Code by genBTC. Created from scratch 10/14/2015.  
#
# Saves all the paths for the entire program in settings.ini.  Handles dynamic path redirection generation on first run.
# Performs the settings.ini set,get,save tasks.
# The only thing you should need to edit is the .ini file. 
# You can however edit the path to resume.dat here, but please note: Editing this file does not CHANGE an existing settings.ini file once it already exists.
# This script is only to generates the default values and put them in settings.ini. You will have to edit the path to resume.dat in the settings.ini file.
#   
# Version 0.1 - functional since 10/14/2015.

from ConfigParser import RawConfigParser
import os.path

class Preferences():
    '''    Represents the application preferences.    '''
    FILENAME = 'settings.ini'
    SECTION = "MAIN"
    utresumedat = "C:\\Users\\EOFL\\AppData\\Roaming\\uTorrent\\resume.dat"

    scriptsdir = os.path.dirname(os.path.realpath(__file__))    #the dir where these scripts are run from; C:\\??\scripts
    maindir = os.path.dirname(scriptsdir)                #the parent dir of "scripts"; C:\\??
    
    # filenames needs a unicode u symbol so os. commands work on paths with funny chars
    script1sourcedir = u"seeding\\"
    outpath1 = u"1seeding_Hash+Filename.txt"
    outpath2 = u"1seeding_ID+Hash.txt"

    credentialsfile = u"scripts\\credentials.txt"
    cookiesfile = u"scripts\\cookies.dat"

    script2destdir = u"hash-grabs\\"
    script3destdir = u"hash-grabs-as-filenames\\"
    outpath3 = u"3propernames.txt"
    outpath4 = u"4beforepath-afterpath.txt"

    def __init__(self):
        self.__do_configfile()
    
    # start private methods
    
    def __do_configfile(self):
        # initialize config parser
        self.configparser = RawConfigParser()

        # __load or (if non-existent) create config file
        if os.path.isfile(self.FILENAME):
            self.__load()
        else:
            self.__init_with_defaults() #only create if it doesnt exist.
            self.save()
            
    def __init_with_defaults(self):
        self.configparser.add_section(self.SECTION)
        self.set('utresumedat', self.utresumedat)
        self.set('scriptsdir', self.scriptsdir)
        self.set('maindir', self.maindir)
        self.set('script1sourcedir', self.script1sourcedir)
        self.set('outpath1', self.outpath1)
        self.set('outpath2', self.outpath2)
        self.set('credentialsfile', self.credentialsfile)
        self.set('cookiesfile', self.cookiesfile)
        self.set('script2destdir', self.script2destdir)
        self.set('script3destdir', self.script3destdir)
        self.set('outpath3', self.outpath3)
        self.set('outpath4', self.outpath4)

    def __load(self):
        '''        Loads or reloads the config from the .ini file        '''
        self.configparser.read(self.FILENAME)

    # end private methods

    # start public methods

    def get(self, key):
        '''        Retrieves a property from the MAIN section        '''
        return self.configparser.get(self.SECTION, key)

    def getwpath(self, key):
        '''        Retrieves a property from the MAIN section 
        and pre-pend the maindir for a full pathname       '''
        return os.path.join(self.maindir,self.configparser.get(self.SECTION, key))

    def set(self, key, value):
        '''        Stores a property to the MAIN section        '''
        self.configparser.set(self.SECTION, key, value)

    def save(self):
        '''        Saves the config to the .ini file        '''
        with open(self.FILENAME, 'wb') as configfile:
            self.configparser.write(configfile)

    # end public methods
