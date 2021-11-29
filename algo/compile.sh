#!/bin/sh
CXX=g++

SOURCES=$(ls *.cc)
for each in $SOURCES; do
	hasmain=$(grep main $each)
	if ! test -z "$hasmain"; then
		echo $CXX $CPPFLAGS $CXXFLAGS $LDFLAGS $each -o ${each}.elf
		$CXX $CPPFLAGS $CXXFLAGS $LDFLAGS $each -o ${each}.elf
	else
		tmpfile=$(mktemp ./autogen.XXXXXX.cc )
		cat > $tmpfile <<EOF
#include <cstdio>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <unistd.h>

#include <iostream>
#include <string>
#include <vector>
#include <queue>
#include <list>
#include <map>
#include <unordered_map>

using namespace std;

EOF
		cat $each >> $tmpfile
		cat >> $tmpfile << EOF
int
main(void)
{
auto s = Solution();
// do nothing
return 0;
}
EOF
		echo $CXX $CPPFLAGS $CXXFLAGS $LDFLAGS $tmpfile -o ${each}.elf
		$CXX $CPPFLAGS $CXXFLAGS $LDFLAGS $tmpfile -o ${each}.elf
		rm $tmpfile
	fi
done
