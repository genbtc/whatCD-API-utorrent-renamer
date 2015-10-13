#!/usr/bin/env python
# -*- coding: utf-8 -*

import HTMLParser
#HTMLParser.HTMLParser().unescape()             #un-escape the HTML ampersands
#this HTML parse thing is to remove the Ampersand HTML characters from the JSON response.... the hacky way (all i know) 
#       The JSON data-dump files contained HTML code like &amp;#12543 %20N and any HTMLParser stuff you see is a workaround.

class TorrentGroup(object):
    def __init__(self):
        #GROUP
        self.catalogueNumber = None
        self.categoryId = None
        self.categoryName = None
        self.id = None
        self.isBookmarked = None
        self.musicInfo = None
        self.name = None
        self.recordLabel = None
        self.releaseType = None
        self.tags = None
        self.time = None
        self.vanityHouse = None
        self.wikiBody = None
        self.wikiImage = None
        self.year = None

    def load(self,jsonresponse):
        for k, v in jsonresponse["group"].iteritems():
            if isinstance(v, unicode):
                v = HTMLParser.HTMLParser().unescape(v)
            setattr(self, k, v)

class TorrentTorrent(object):
    def __init__(self):
        #TORRENT        
        self.description  = None
        self.encoding = None
        self.fileCount = None
        self.fileList = None
        self.filePath = None
        self.format = None
        self.freeTorrent  = None
        self.hasCue = None
        self.hasLog = None
        self.id = None          #duplicate
        self.infoHash = None
        self.leechers = None
        self.logScore = None
        self.media = None
        self.remasterCatalogueNumber  = None
        self.remastered = None
        self.remasterRecordLabel  = None
        self.remasterTitle = None
        self.remasterYear = None
        self.reported = None
        self.scene = None
        self.seeders  = None
        self.size = None
        self.snatched = None
        self.time = None        #duplicate
        self.userId = None
        self.username = None

    def load(self,jsonresponse):
        for k, v in jsonresponse["torrent"].iteritems():
            if isinstance(v, unicode):
                v = HTMLParser.HTMLParser().unescape(v)
            setattr(self, k, v)        

class Torrent(object):
    def __init__(self,response):
        self.group = TorrentGroup()
        self.group.load(response)
        self.torrent = TorrentTorrent()
        self.torrent.load(response)

