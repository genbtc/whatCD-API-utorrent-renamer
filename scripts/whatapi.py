# slightly edited from whatapi @ https://github.com/isaaczafuta/whatapi
#
# server documentation says (max 5 requests in 10 secs)
# Modified the Sleep, to provide the desired sleep time in seconds to the request function. The get_torrent function uses a 1.8 second fixed default sleep.

try:
    from ConfigParser import ConfigParser
except ImportError:
    import configparser as ConfigParser # py3k support

import requests
import time

#added for For mental Reference:

C192 = "192"
APS = "APS (VBR)"
V2 = "V2 (VBR)"
V1 = "V1 (VBR)"
C256 = "256"
APX = "APX (VBR)"
V0 = "V0 (VBR)"
C320 = "320"
LOSSLESS = "Lossless"
LOSSLESS_24 = "24bit Lossless"
V8 = "V8 (VBR)"
ALL_ENCODINGS = [C192, APS, V2, V1, C256, APX, V0, C320, LOSSLESS, LOSSLESS_24, V8]


MP3 = "MP3"
FLAC = "FLAC"
AAC = "AAC"
AC3 = "AC3"
DTS = "DTS"
OGG_VORBIS = "Ogg Vorbis"
ALL_FORMATS = [MP3, FLAC, AAC, AC3, DTS, OGG_VORBIS]


CD = "CD"
DVD = "DVD"
VINYL = "Vinyl"
SOUNDBOARD = "Soundboard"
SACD = "SACD"
DAT = "DAT"
CASETTE = "Casette"
WEB = "WEB"
BLU_RAY = "Blu-ray"
ALL_MEDIAS = [CD, DVD, VINYL, SOUNDBOARD, SACD, DAT, CASETTE, WEB, BLU_RAY]


ALBUM = "Album"
SOUNDTRACK = "Soundtrack"
EP = "EP"
ANTHOLOGY = "Anthology"
COMPILATION = "Compilation"
DJ_MIX = "DJ Mix"
SINGLE = "Single"
LIVE_ALBUM = "Live album"
REMIX = "Remix"
BOOTLEG = "Bootleg"
INTERVIEW = "Interview"
MIXTAPE = "Mixtape"
UNKNOWN = "Unknown"
ALL_RELEASE_TYPES = [ALBUM, SOUNDTRACK, EP, ANTHOLOGY, COMPILATION, DJ_MIX, SINGLE, LIVE_ALBUM, REMIX, BOOTLEG,
                     INTERVIEW, MIXTAPE, UNKNOWN]

#Release types strings
# 1 = "Album"
# 3 = "Soundtrack"
# 5 = "EP"
# 6 = "Anthology"
# 7 = "Compilation"
# 8 = "DJ Mix"
# 9 = "Single"
# 11 = "Live"
# 13 = "Remix"
# 14 = "Bootleg"
# 15 = "Interview"
# 16 = "Mixtape"
# 21 = "Unknown"
# 22 = "Concert Recording"
# 23 = "Demo"

#Release types as enum
# Album = 1
# Soundtrack = 3
# EP = 5
# Anthology = 6
# Compilation = 7
# DJ_Mix = 8
# Single = 9
# Live = 11
# Remix = 13
# Bootleg = 14
# Interview = 15
# Mixtape = 16
# Unknown = 21
# Concert Recording = 22
# Demo = 23

headers = {
    'Content-type': 'application/x-www-form-urlencoded',
    'Accept-Charset': 'utf-8',
    'User-Agent': 'whatapi [isaaczafuta]'
    }

class LoginException(Exception):
    pass


class RequestException(Exception):
    pass


class WhatAPI:
    def __init__(self, config_file=None, username=None, password=None, cookies=None):
        self.session = requests.Session()
        self.session.headers = headers
        self.authkey = None
        self.passkey = None
        if config_file:
            config = ConfigParser()
            config.read(config_file)
            self.username = config.get('login', 'username')
            self.password = config.get('login', 'password')
        else:
            self.username = username
            self.password = password
        if cookies:
            self.session.cookies = cookies
            try:
                self._auth()
            except RequestException:
                self._login()
        else:
            self._login()

    def _auth(self):
        '''Gets auth key from server'''
        accountinfo = self.request(0,"index")
        print "Authorization Obtained!"
        self.authkey = accountinfo["response"]["authkey"]
        self.passkey = accountinfo["response"]["passkey"]

    def _login(self):
        '''Logs in user'''
        loginpage = 'https://ssl.what.cd/login.php'
        data = {'username': self.username,
                'password': self.password,
                'keeplogged': 1,
                'login': 'Login'
        }
        r = self.session.post(loginpage, data=data, allow_redirects=False)
        if r.status_code != 302:
            raise LoginException
        self._auth()

    def get_torrent(self, torrent_id):
        '''Downloads the torrent at torrent_id using the authkey and passkey'''
        torrentpage = 'https://ssl.what.cd/torrents.php'
        params = {'action': 'download', 'id': torrent_id}
        if self.authkey:
            params['authkey'] = self.authkey
            params['torrent_pass'] = self.passkey
        r = self.session.get(torrentpage, params=params, allow_redirects=False)
        time.sleep(1.8)
        if r.status_code == 200 and 'application/x-bittorrent' in r.headers['content-type']:
            return r.content
        return None

    def logout(self):
        '''Logs out user'''
        logoutpage = 'https://ssl.what.cd/logout.php'
        params = {'auth': self.authkey}
        self.session.get(logoutpage, params=params, allow_redirects=False)

    def request(self, sleep, action, **kwargs):
        '''Makes an AJAX request at a given action page'''
        ajaxpage = 'https://ssl.what.cd/ajax.php'
        params = {'action': action}
        if self.authkey:
            params['auth'] = self.authkey
        params.update(kwargs)

        r = self.session.get(ajaxpage, params=params, allow_redirects=False)
        time.sleep(sleep)
        try:
            json_response = r.json()
            if json_response["status"] != "success":
                raise RequestException
            return json_response
        except ValueError:
            raise RequestException
