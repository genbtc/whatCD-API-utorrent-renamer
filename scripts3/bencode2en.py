# Version 0.1b - Changed code to target Python 3 @ 10/16/2015

def bencode2(obj):
    #Seems to be working under Python 3
    if isinstance(obj, bytes):
        coded_bytes = b''
        length = len(obj)
        coded_bytes += bytes(str(length), 'utf-8') + b':'
        coded_bytes += obj
        return coded_bytes

    elif isinstance(obj, str):
        """Converts the input string to bytes and passes it the __encode_byte_str function for encoding."""
        b = bytes(obj, 'utf-8')
        return bencode2(b)

    elif isinstance(obj, int):
        """B-encodes integer from int."""
        coded_bytes = b''        
        coded_bytes += b'i'
        coded_bytes += bytes(str(obj), 'utf-8')
        coded_bytes += b'e'
        return coded_bytes

    elif isinstance(obj, list):
        res = b"l"
        for elem in obj:
            res += bencode2(elem)
        return res + b"e"
    
    elif isinstance(obj, dict):
        res = b"d"
        for key in sorted(obj.keys()):
            res += bencode2(key) + bencode2(obj[key])
        return res + b"e"




def bencode4(x):#,newfile):
    r = []
    encode_func[type(x)](x, r)
    return b''.join(r)

def encode_bytes(obj, r):
    coded_bytes = b''
    length = len(obj)
    coded_bytes += bytes(str(length), 'utf-8') + b':'
    coded_bytes += obj
    r.append(coded_bytes)

def encode_string(obj, r):
    """Converts the input string to bytes and passes it the __encode_byte_str function for encoding."""
    b = bytes(obj, 'utf-8')
    encode_bytes(b,r)

def encode_int(obj, r):
    """B-encodes integer from int."""
    coded_bytes = b''        
    coded_bytes += b'i'
    coded_bytes += bytes(str(obj), 'utf-8')
    coded_bytes += b'e'
    r.append(coded_bytes)

def encode_list(obj, r):
    r.append(b'l')
    for i in obj:
        encode_func[type(i)](i, r)
    r.append(b'e')

def encode_dict(obj,r):
    r.append(b'd')
    for key in sorted(obj.keys()):
        encode_func[type(key)](key, r)
        encode_func[type(obj[key])](obj[key], r)
    r.append(b'e')

encode_func = {}
encode_func[int] = encode_int
encode_func[str] = encode_string
encode_func[bytes] = encode_bytes
encode_func[list] = encode_list
encode_func[tuple] = encode_list
encode_func[dict] = encode_dict


def bdecodetext(text):
    def bdecode_next(start):

        if chr(text[start]) == 'i':  #process ints
            end = text.find(b'e', start)
            return int(text[start+1:end], 10), end + 1
        
        if chr(text[start]) == 'l':  #process the lists
            res = []
            start += 1
            while chr(text[start]) != 'e':
                elem, start = bdecode_next(start)
                res.append(elem)
            return res, start + 1

        if chr(text[start]) == 'd':  #process every dict
            res = {}
            start += 1

            while chr(text[start]) != 'e':
                key, start = bdecode_next(start)
                value, start = bdecode_next(start)
                res[key] = value

            return res, start + 1

        lenend = text.find(b':', start)
        length = int(text[start:lenend], 10)
        end = lenend + length + 1
        return text[lenend+1:end], end    

    return bdecode_next(0)[0]

def decode_from_file(path: str):
    """Convenience function. Reads file and calls decode()."""
    with open(path, 'rb') as f:
        b = f.read()
    return bdecodetext(b)    