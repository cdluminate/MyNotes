#!/usr/bin/python3
# translate argv with youdao
'''
# ydtrans
[py3] youdao translation shortcut in terminal, very simple one

It translates the argv you'd given, that's all.

### example
```
$ python3.4 t.py python
```

### hint
add this into bashrc:
```
t () {
  python3.4 some/dir/t.py $@
}
```
then you can just call the script with
```
$ t <your keyword or sentense>
```
'''

import sys
import requests
import json

# configure
# http://fanyi.youdao.com/openapi
baseurl = "http://fanyi.youdao.com/openapi.do?keyfrom=github-ydtrans&key=164101779&type=data&doctype=json&version=1.1&q="
quiry   = baseurl

# check argv
if len(sys.argv) < 2:
	print ("* missing argv[1:]")
	exit (1)

# generate quiry
for item in sys.argv[1:]:
	quiry = quiry + item + "+"

# do query and dump json response
response = requests.get (quiry)
trans    = json.loads(response.text)
ans = json.dumps (trans, indent=4, sort_keys=True, ensure_ascii=False)
print (ans)
