#!/usr/bin/env python3
import xmltodict
import json

xmlstring = '''
<?xml version="1.0"?>
<root xmlns    = "http://default-namespace.org/" xmlns:py = "http://www.python.org/ns/">
  <py:elem1 />
  <elem2 xmlns="" />
</root>
'''.strip()

print('=> XML -> DICT/LIST -> JSON')
jsonstring = json.dumps(xmltodict.parse(xmlstring), indent=4)
print(jsonstring, type(jsonstring))

print('=> JSON -> DICT/LIST -> XML')
xmlstring2 = xmltodict.unparse(json.loads(jsonstring))
print(xmlstring2)
