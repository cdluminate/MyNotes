#!/usr/bin/python3
import sys
import gzip
import re

def Usage (name):
	print ("Usage: %s <Sources.gz>" % sys.argv[0])
	exit (1)

# check usage
if (1 >= len(sys.argv)):
	Usage (sys.argv[0])

# setup text filters
f_maintainer = re.compile ("^Maintainer:*")
f_uploaders  = re.compile ("^Uploaders:*")
f_mailaddr   = re.compile("<.*?@.*?>")

# decompress
with gzip.open (filename=sys.argv[1], mode='rb') as SrcGZ:
	Src = str( SrcGZ.read () ).replace('\\n','\n')

# get the text file as list
SrcList = Src.split('\n')
print ("I: [%s] has [%d] lines" % (sys.argv[1], len(SrcList)))
print (type(SrcList))
for line in SrcList:
	line = line.strip()
	lst = []
	if f_maintainer.findall (line):
		lst = f_mailaddr.findall (line)
	elif f_uploaders.findall (line):
		lst = f_mailaddr.findall (line)
	if not (0 == len(lst)):
		for item in lst:
			print (item)
