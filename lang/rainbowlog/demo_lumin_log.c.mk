# Makefile for demo_lumin_log.c
main: clean
	$(CC) -std=gnu11 -g -Wall demo_lumin_log.c -o demo_lumin_log
	./demo_lumin_log
	$(MAKE) clean
clean:
	$(RM) demo_lumin_log
