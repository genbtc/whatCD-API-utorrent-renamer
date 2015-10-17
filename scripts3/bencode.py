# The contents of this file are subject to the BitTorrent Open Source License
# Version 1.1 (the License).  You may not copy or use this file, in either
# source code or executable form, except in compliance with the License.  You
# may obtain a copy of the License at http://www.bittorrent.com/license/.
#
# Software distributed under the License is distributed on an AS IS basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied.  See the License
# for the specific language governing rights and limitations under the
# License.

# Written by Petru Paler

# Obtained from @ https://pypi.python.org/pypi/BitTorrent-bencode

# Modified by genBTC @ 10/9/2015, and again 10/16 
# Coded for Python 3 (tested under Python 3.5 for Windows 64-bit)
# Modification is allowed under license & source code is available free of charge
#Reason: Encode functions were not unicode compatible..... 
#Status: Not completely unicode compatible yet.
# Version 0.1b - Changed code to target Python 3 @ 10/16/2015

from types import *

class BTFailure(Exception):
    pass

def decode_int(x, f):
    f += 1
    newf = x.index(b'e', f)
    n = int(x[f:newf])
    return (n, newf+1)

def decode_string(x, f):
    colon = x.index(b':', f)
    n = int(x[f:colon])
    colon += 1
    return (x[colon:colon+n], colon+n)

def decode_list(x, f):
    r, f = [], f+1
    while chr(x[f]) != 'e':
        v, f = decode_func[chr(x[f])](x, f)
        r.append(v)
    return (r, f + 1)

def decode_dict(x, f):
    r, f = {}, f+1
    while chr(x[f]) != 'e':
        k, f = decode_string(x, f)
        r[k], f = decode_func[chr(x[f])](x, f)
    return (r, f + 1)

decode_func = {}
decode_func['l'] = decode_list
decode_func['d'] = decode_dict
decode_func['i'] = decode_int
decode_func['0'] = decode_string
decode_func['1'] = decode_string
decode_func['2'] = decode_string
decode_func['3'] = decode_string
decode_func['4'] = decode_string
decode_func['5'] = decode_string
decode_func['6'] = decode_string
decode_func['7'] = decode_string
decode_func['8'] = decode_string
decode_func['9'] = decode_string

def bdecode(x):
    # try:
    r, l = decode_func[chr(x[0])](x, 0)
    # except (IndexError, KeyError, ValueError):
    #     raise BTFailure("not a valid bencoded string")
    # if l != len(x):
    #     raise BTFailure("invalid bencoded value (data after valid prefix)")
    return r

def decode_from_file(path: str):
    """Convenience function. Reads file and calls decode()."""
    with open(path, 'rb') as f:
        b = f.read()
    return bdecode(b)

#------------------------------

def encode_int(x, r):
    r.extend((b'i', bytes(str(x),'utf-8'), b'e'))

def encode_string(x, r):
    b = bytes(x, 'utf-8')
    encode_bytes(b,r)

def encode_bytes(x, r):
    r.extend((bytes(str(len(x)),'utf-8'),b':', x))

def encode_list(x, r):
    r.append(b'l')
    for i in x:
        encode_func[type(i)](i, r)
    r.append(b'e')

def encode_dict(x,r):
    r.append(b'd')
    ilist = list(x.items())
    ilist.sort()
    for k,v in ilist:
        encode_func[type(k)](k, r)
        encode_func[type(v)](v, r)
    r.append(b'e')

encode_func = {}
encode_func[int] = encode_int
encode_func[str] = encode_string
encode_func[bytes] = encode_bytes
encode_func[list] = encode_list
encode_func[tuple] = encode_list
encode_func[dict] = encode_dict

def bencode(x):
    r = []
    encode_func[type(x)](x, r)
    return b''.join(r)