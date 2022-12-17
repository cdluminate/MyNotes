# py3

def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value

def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value

#with open('/tmp/a', 'w') as f:
    #f.write(os.urandom(10)) # error
#with open('/tmp/a', 'wb') as f:
#    f.write(os.urandom(10)) # ok
