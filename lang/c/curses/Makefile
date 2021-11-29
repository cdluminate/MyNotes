main:
#	$(CC) -fPIE -pie foo.c -o foo \
#/usr/lib/x86_64-linux-gnu/libtermcap.so \
#/usr/lib/x86_64-linux-gnu/libtic.a \
#/usr/lib/x86_64-linux-gnu/libtinfo.a \
#/usr/lib/x86_64-linux-gnu/libncurses.a
	$(CC) -Wall -pedantic -fPIE -pie foo.c -o foo -static -static-libgcc -static-libstdc++ -lncurses -ltinfo -lm

# https://stackoverflow.com/questions/3283021/compile-a-standalone-static-executable
