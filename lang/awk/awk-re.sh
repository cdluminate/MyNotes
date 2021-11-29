#!/bin/sh
set -e
. ../lumin_log.sh

tempfile=$(mktemp)
cat >> $tempfile <<EOF
127.0.0.1 localhost
::1       localhost
8.8.8.8   googledns
192.168.0.1 localnet1
192.168.0.2 localnet2

1 Mangoes 45 \$3.45
2 Apples 25 \$2.45
3 Pineapples 5 \$4.45
EOF
trap "rm -f $tempfile" EXIT

# regex

warn 'original file'
cat $tempfile

info 'no pattern specified'
awk '//{print}' $tempfile

info 'match localhost'
awk '/localhost/{print}' $tempfile

info 'using dot wildcard'
awk '/l.c/{print}' $tempfile

info 'using asterisk wildcard'
awk '/l*t/{print}' $tempfile

info 'using characters match'
awk '/t[12]/{print}' $tempfile

info 'using range'
awk '/[0-9]/{print}' $tempfile

info 'using ^ and $'
awk '/^:/{print}' $tempfile
awk '/s$/{print}' $tempfile

info 'using escape'
awk '/\$/{print}' $tempfile

# fields

info 'fields'
awk '/localhost/{print $2, $1}' $tempfile
awk '/localhost/{printf "%-10s %s\n", $2, $1}' $tempfile

# comparison
# some_value ~ / pattern/
# some_value !~ / pattern/
info 'comparison'
awk '$3 <= 30 { printf "%s\t%s\n", $0, "**"; } $3 > 30 { print $0; }' $tempfile
