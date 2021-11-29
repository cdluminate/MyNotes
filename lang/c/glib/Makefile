CFLAGS += $(shell pkg-config --libs --cflags glib-2.0)

%:
	$(CC) $@.c $(CFLAGS) -o $@
