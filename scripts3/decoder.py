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
# Version 0.9.4b - Modified by genBTC to stop using OrderedDicts, and stop wrapping in tuples.  @ 10/16/2015

from collections.abc import Iterable

class Decoder:
    def __init__(self, data: bytes):
        self.data = data
        self.idx = 0

    def __read(self, i: int) -> bytes:
        """Returns a set number (i) of bytes from self.data."""
        b = self.data[self.idx: self.idx + i]
        self.idx += i
        if len(b) != i:
            raise DecodingError(
                "Incorrect byte length returned between indexes of {0} and {1}. Possible unexpected End of File."
                .format(str(self.idx), str(self.idx - i)))
        return b

    def __read_to(self, terminator: bytes) -> bytes:
        """Returns bytes from self.data starting at index (self.idx) until terminator character."""
        try:
            # noinspection PyTypeChecker
            i = self.data.index(terminator, self.idx)
            b = self.data[self.idx:i]
            self.idx = i + 1
            return b
        except ValueError:
            raise DecodingError(
                'Unable to locate terminator character "{0}" after index {1}.'.format(str(terminator), str(self.idx)))

    def __parse(self) -> object:
        """Selects the appropriate method to decode next bencode element and returns the result."""
        char = self.data[self.idx: self.idx + 1]
        if char in [b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'0']:
            str_len = int(self.__read_to(b':'))
            return self.__read(str_len)
        elif char == b'i':
            self.idx += 1
            return int(self.__read_to(b'e'))
        elif char == b'd':
            return self.__parse_dict()
        elif char == b'l':
            return self.__parse_list()
        elif char == b'':
            raise DecodingError('Unexpected End of File at index position of {0}.'.format(str(self.idx)))
        else:
            raise DecodingError('Invalid token character ({0}) at position {1}.'.format(str(char), str(self.idx)))

    def __parse_dict(self) -> dict:
        """Returns a Dictionary of nested bencode elements."""
        self.idx += 1
        d = dict()
        key_name = None
        while self.data[self.idx: self.idx + 1] != b'e':
            if key_name is None:
                key_name = self.__parse()
            else:
                d[key_name] = self.__parse()
                key_name = None
        self.idx += 1
        return d

    def __parse_list(self) -> list:
        """Returns an list of nested bencode elements."""
        self.idx += 1
        l = []
        while self.data[self.idx: self.idx + 1] != b'e':
            l.append(self.__parse())
        self.idx += 1
        return l

    def decode(self) -> Iterable:
        """Start of decode process. Returns final results."""
        return self.__parse()    


def decode_from_file(path: str) -> Iterable:
    """Convenience function. Reads file and calls decode()."""
    with open(path, 'rb') as f:
        b = f.read()
    return decode(b)


def decode(data: bytes) -> Iterable:
    """Convenience function. Initializes Decoder class, calls decode method, and returns the result."""
    decoder = Decoder(data)
    return decoder.decode()

class DecodingError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)