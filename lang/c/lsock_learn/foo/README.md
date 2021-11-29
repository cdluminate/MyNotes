foo
===
Brute force, parallel(OpenMP) MD5 cracker.  
It can only crack 4-char string, 
but it can be extended/rewrited to fit other lengths of strings.  

###Usage/Example
* First, make
```
$ make
```

* Generate a raw MD5 digest file, witch consists 16 Bytes.  
```
$ ./md5bin 0000 > 0000.md5
```
here I calculates the MD5 of "0000", then put it in file "0000.md5"  
The MD5 Message Digest is a 16-Bytes matter.  

* Change foo.c referring that formerly generated file  
```
- #define MD5_FILE_TO_CRACK "hhhh.md5"
+ #define MD5_FILE_TO_CRACK "0000.md5"
```

* run and wait for answer, you can measure the time meanwhile.
```
$ time ./foo
```
after some seconds, it will throw this to stdout:
```
0000
```
