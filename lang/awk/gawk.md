Gawk Note
===
> GNU Awk Manual :  
> GAWK: Effective AWK Programming  
> A User’s Guide for GNU Awk  
> Edition 4.1 August, 2016  

# Part I: the awk language

## getting started
```
pattern { action }

awk 'AWKPROGRAM' input.txt
awk -f program.awk input.txt
#!/bin/awk -f
```

```
awk '/pattern/{print $0}' input.txt
awk 'length($0)>80' data.txt
awk '{if (length($0)>max) max = length($0) } END { print max }' data.txt
awk 'NF>0' data.txt # field number > 0, blank lines will be filtered.
awk 'BEGIN { for (i = 1; i <= 7; i++) print int(101 * rand()) }'
ls -l files | awk '{ x += $5 } END { print "total bytes: " x }'
ls -l files | awk '{ x += $5 } END { print "total K-bytes:", x / 1024 }'
awk -F: '{ print $1 }' /etc/passwd | sort
awk 'END { print NR }' data
awk 'NR % 2 == 0' data
awk '/pattern1/{print $0}; /pattern2/{print $0}' data.txt
```

hint, convert TABs into spaces with tool `expand`.

## running awk and gawk
pass

functionality to include awk files is available in awk.

## regular expressions
```
exp ~ /pattern/  # match expression with pattern
exp !~ /pattern/ # not match

$1 ~ /patter/    # field 1 match
```

regular expression operations
```
\      escape
^      string begining
$      string ending
.      match a single character
[...]  matches any one character provided within brackets
|      alternation
(...)  grouping regular expressions, e.g. (apple|banana)
*      repeat preceding character or not, greedy.
+      repeat preceding character at least once
?      repeat once or not.
{n}
{n,}
{n,m}  interval expression
```
see also: POSIX character classes

case sensitivity
```
tolower($1) ~ /regexp/
```

## chap4: reading input files
```
FILENAME
RS = "u" # record separator
NF       # number of fields
NR       # number of records read so far, starts from 1
FS       # field separator
BEGIN { FIELDWIDTHS = "9 6 10 6 7 7 35" }
```

`getline` function ...

## chap5: printing output
```
print item1, item2, ...
print "this is a string\n"
print $1 $2   # <-- this is an common error, which yields no space between items
print $1, $2  # correct.

msg = "do not panic!"
printf "%s\n", msg
```

`OFS` is output field separator.

output redirectoring # seems important to me.
```
$ awk ’{ print $2 > "phone-list"
>        print $3 >> "append"
>        print $4 | "sort -r > c4.sorted"
>        print $1 > "name-list" }’ mail-list
```

## chap6: expressions
operators
```
arithmatic:
 x^y, x**y   exponentiation
 -x
 +x
 x*y
 x/y
 x%y
 x+y
 x-y

assignment:
 z = 1
 += -= *= /= %= ^= (**=)

increment and decrement:
  ++ --

true and false:
  1 0

comparison:
  < <= > >= == != ~ !~
  <subscript> in <array>

boolean:
  && || !

conditional:
  selector ? if-true-exp : if-false-exp
```

Note, Do not put any space between the function name and the open-
ing parenthesis!

## chap7: pattern, action, variable

#### pattern elements
```
/regexp/
experssion
BEGIN
END
```

e.g.
```awk
/foo|bar|baz/ { buzzwords++ }
END           { print buzzwords, "buzzwords seen" }
```

control flow
```
if (expr) {
  then-body
} else {
  else-body
}

while (condition) {
  body
}

do {
  body
} while (condition)

for (initialization; condition; increment) {
  body
}

switch (expression) {
case value or regular expression:
  case-body
default:
  default-body
}

break

continue

next

nextfile

exit [code]
```

pre-defined variables
```
FS             field separator
IGNORECASE
OFS            output field separator
ORS            output record separator
RS             input record separator

FILENAME
NF             number of fields
NR             number of records read so far
```

## chap8: arrays in awk
in awk, generally array index starts from 0. however actually awk array
is similar to lua table.
```
array[index-expression] = value
```

## chap9: functions

#### mathematical functions
```
atan2(y, x) # y/x in radians, and `pi = atan2(0,-1)`
cos(x) exp(x) int(x) log(x)
rand() # [0, 1)
sin(x) sqrt(x) srand([x])
```

#### string functions
```
asort(...   # array sort
asorti(...
gensub(regexp, replacement, how[, target]) # able to specify components
gsub(regexp, replacement [, target])
index(in, find)
length([string])
match(string, regexp, [array])
patsplit(string, array [, fieldpat [, seps ] ]) # devide string into pieces
split(string, array [, fieldsep [, seps ] ]) # Divide string into pieces separated by fieldsep and store the pieces in array
sprintf(format, expression1, ...)
strtonum(str)
sub(regexp, replacement [, target])
substr(string, start [, length ])
tolower(string)
toupper(string)
```

```
$ gawk ’
> BEGIN {
> a = "abc def"
> b = gensub(/(.+) (.+)/, "\\2 \\1", "g", a)
> print b
> }’
a def abc
```

#### input/output functions
```
close(filename[, how])
fflush([filename])
system(command)
```

#### time functions
```
mktime(datespec)
strftime([format [, timestamp [, utc-flag] ] ])
systime()
```

#### bit-wise
pass

#### user functions
```
function name([parameter-list])
{
    body-of-function
    [return]
}

```

## practical awk programs
TODO

# appendix D: basic programming concepts
```
|input|-->--|program|-->--|output|
```

marked as basically done. 2016 Oct 29
