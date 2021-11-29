Bytefreq
========

[C, utility, Linux platform]  
Bytefreq aims to figure out the freqency of each byte or character.  
  
##### Feature:  
* Following data would be printed by default, see [DEMO](# Bytefreq Demo):
  1. Among bytes specified, which one enjoys the [maximum/minimum]() freqency.
  2. The [mathematical expectation]() of all bytes.
  3. The number of bytes that specified by user, and proportion.
  4. Total read size, should be same to the answer of stat().
* data processing approaches are choosable.  
  1. [serial]() default action, infinitely read() and count until EOF.  
  2. [parallel]() option '-p', infinitely read() and count them in 4-thread parallel.  
  3. [unix_socket]() option '-U', manipulate data with sendfile() via UNIX Socket.
* user can specify the character set to count (following can be combined randomly).  
  1. control character, symbols (option -c -s)
  2. upper and lower, alphabets also do (option -u -l -a)
  3. count all bytes (option -A)
  4. specify a single byte (option -S)  
* ANSI color used to highlight values and special entries.  
* '-v' (verbose) option offers a BSD-style-like progress bar (spinning bar and proportion number).
  
##### Info:  
* We can also do some I/O performance experiments with this utility, as it offers 3 kinds of reading method.  
* The parallel approach (OpenMP) seems to have lower performance than normal Serial one. So, likely that parallel computing doesn't help I/O intensive tasks much.  
* having analyzed the freqency of bytes/chars, we can do something further, such as decode substitude cipher (which is a kind of classic encryption method), the utilities described below may do somthing related.    
  

### Bytefreq Demo
```
$ bytefreq bytefreq -l
Crunching data ...
=========================================================
Character    Count           of_ALL          of_Specified
=========    ============    ============    ============
(0x61, 'a')              81         0.515 %         4.793 %
(0x62, 'b')              22         0.140 %         1.302 %
(0x63, 'c')              70         0.445 %         4.142 %
(0x64, 'd')              72         0.458 %         4.260 %
(0x65, 'e')             159         1.011 %         9.408 %
(0x66, 'f')             135         0.859 %         7.988 %
(0x67, 'g')              67         0.426 %         3.964 %
(0x68, 'h')              71         0.452 %         4.201 %
(0x69, 'i')             113         0.719 %         6.686 %
(0x6a, 'j')               4         0.025 %         0.237 %
(0x6b, 'k')              12         0.076 %         0.710 %
(0x6c, 'l')              78         0.496 %         4.615 %
(0x6d, 'm')              41         0.261 %         2.426 %
(0x6e, 'n')              96         0.611 %         5.680 %
(0x6f, 'o')             112         0.712 %         6.627 %
(0x70, 'p')              61         0.388 %         3.609 %
(0x71, 'q')               8         0.051 %         0.473 %
(0x72, 'r')              85         0.541 %         5.030 %
(0x73, 's')             103         0.655 %         6.095 %
(0x74, 't')             146         0.929 %         8.639 %
(0x75, 'u')              65         0.413 %         3.846 %
(0x76, 'v')              15         0.095 %         0.888 %
(0x77, 'w')              10         0.064 %         0.592 %
(0x78, 'x')              25         0.159 %         1.479 %
(0x79, 'y')              28         0.178 %         1.657 %
(0x7a, 'z')              11         0.070 %         0.651 %
Maximous of specified : (0x65  'e') : 159
Minimous of specified : (0x6A, 'j') : 4
The Math Expection    : (0x3A, ':', dec 58)
Total bytes specified : 1690, 10.751%
Total bytes read()    : 15720
```


### Bytefreq help message

```
$ bytefreq -h
Usage:
  bytefreq [options] [FILE]
Description:
  Count frequency of specified set of Bytes/Char.
  Only shows Total read size if no char specified.
  If given no <FILE>, it would read from the stdin.
Options:
  -h     show this help message
  -V     show version info
  -v     verbose mode
  -d     don't use percent output, use float instead

  -p     use parallel approach
  -U     use UNIX socket apprach (sendfile)
  -A     specify all bytes to count
  -l     specify lower to count
  -u     specify upper to count
  -s     specify symbol to count
  -c     specify control character to count
  -a     specify alphabets to count (= '-lu')
  -S <N> specify the byte N (decimal)
  ...
For more info see -v

```
  
### Compile
just make.  
  
If you want to make package of it, you can invoke  
```
$ make deb-pkg
```
as long as you have dpkg-buildpackage command installed.  

#### other utilities included in this repo
There are some other small programs that may be useful:  
[util/a8lu.c](./util/a8lu.c)     
Convert alphabets between upper and lower case.   
[util/a8shift.c](./util/a8shift.c)  
Shift alphabets by (+/-)N positions in alphabet list.  

  
---
#### Expample of util/a8lu.c
```
$ ./a8lu
# lower to upper, read from stdin.
ab cd EF  <- stdin
AB CD EF  <- stdout

$ ./a8lu -r
# upper to lower, read from stdin.
AB CD ef  <- stdin
ab cd ef  <- stdout
```

#### Example of util/a8shift.c
```
$ ./a8shift -o 2
# go right by 2 positions.
ab yz  <- stdin
cd ab  <- stdout

$ ./a8shift -o -2
# go left by 2 positions.
ab yz  <- stdin
yz wx  <- stdout
```

#### Example of util/a8shift.c :: Generate Substitution cipher
There is an rough and wild way that works:  
```
$ ORIGIN='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
# for example shift them by 1 position.
$ SUBSTI='BCDEFGHIJKLMNOPQRSTUVWXYZAbcdefghijklmnopqrstuvwxyza'
  
$ cat FILE | tr -s $ORIGIN $SUBSTI
```
If you want to simply shift them by (int)N positions, use [util/a8shift.c](./util/a8shift.c).  
```
$ cat FILE | ./a8shift -o 1
# same result as above
```

#### Example :: swap characters
The gnu's tr is enough to this purpose.  
```
$ tr -s 'ORIGIN_LIST' 'TARGET_LIST'
```
For example,
```
$ tr -s 'abc' 'xyz'  
abcdefxyz		<- from stdin  
xyzdefxyz		<- processed by tr  
```  

### Licence
The MIT licence.  
