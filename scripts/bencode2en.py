def bencode2(obj):
    if isinstance(obj, int):
        return "i" + str(obj) + "e"

    if isinstance(obj, unicode):
        obj = obj.encode('utf-8')
        return str(len(obj)) + ":" + obj
    
    if isinstance(obj, str):
        return str(len(obj)) + ":" + obj
    
    if isinstance(obj, list):
        res = "l"
        for elem in obj:
            res += bencode2(elem)
        return res + "e"
    
    if isinstance(obj, dict):
        res = "d"
        for key in sorted(obj.keys()):
            res += bencode2(key) + bencode2(obj[key])
        return res + "e"
    
    raise Exception, "Unknown object: %s"%repr(obj)