# Name: bencodepy
# Version: 0.9.4
# Summary: Bencode encoder/decoder written in Python 3 under the GPLv2.
# Home-page: https://github.com/eweast/BencodePy
# Author: Eric Weast
# Author-email: eweast@hotmail.com
# License: GPLv2
# Description: #BencodePy
#         A small Python 3 library for encoding and decoding Bencode data licensed under the GPLv2.
#
# Modified by genBTC a LOT  @ 10/16/2015
# New class, sorted dict, no += bytes, no error handling, added typed function dispatch specialization (encode_func[type])

def encode(obj):
    a = Encoder()
    a.run(obj)
    return b''.join(a.makelist) #this is done because bytestrings are immutable and cannot be +='ed efficiently without copying/re-creating.
       
class Encoder:
    def __init__(self):
        self.makelist = []
        self.encoding='utf-8'

    def encode_byte_str(self, b: bytes) -> None:
        """Ben-encodes string from bytes."""
        self.makelist.append(bytes(str(len(b)), self.encoding) + b':' + b)

    def encode_int(self, i: int) -> None:
        """Ben-encodes integer from int."""
        self.makelist.append(b'i' + bytes(str(i), self.encoding) + b'e')

    def encode_list(self, l: list) -> None:
        """Ben-encodes list from list."""
        self.makelist.append(b'l')
        for i in l:
            self.encode_func[type(i)](self,i)
        self.makelist.append(b'e')

    def encode_dict(self, d: dict) -> None:
        """Ben-encodes dictionary from dict."""
        self.makelist.append(b'd')
        ilist = list(d.items())
        ilist.sort()
        for k,v in ilist:
            self.encode_func[type(k)](self,k)
            self.encode_func[type(v)](self,v)
        self.makelist.append(b'e')

    encode_func = {}
    encode_func[int] = encode_int
    encode_func[bytes] = encode_byte_str
    encode_func[list] = encode_list
    encode_func[tuple] = encode_list
    encode_func[dict] = encode_dict

    def run(self,obj: object):
        return self.encode_func[type(obj)](self,obj)


class EncodingError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)        