#include <stdio.h>
#include <glib.h>

int
main(void)
{
	GSList* l = NULL;
	printf("list length %d\n", g_slist_length(l));
	l = g_slist_append(l, "first");
	l = g_slist_append(l, "second");
	printf("list length %d\n", g_slist_length(l));

	return 0;
}
