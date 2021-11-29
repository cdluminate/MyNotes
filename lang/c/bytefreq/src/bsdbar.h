/* bsdbar.h

   part of Bytefreq
   cdluminate@gmail.com
*/

/* SYNOPSIS

   0. #include "bsdbar.h"
   
   1. when going to start the progress bar, invoke
      BSDbar_init (void);

   2. when going to refresh the progress bar, invoke
      BSDbar_refresh (int proportion);

   3. when going to clear the bar, invoke
      BSDbar_clear (void);

   4. that's all
*/

#ifndef BSDBAR_H
#define BSDBAR_H

#include <unistd.h>
#include <stdio.h>
#include "wrapper.h"

/* INTERFACE */
void BSDbar_init (void);
void BSDbar_clear (void);
void BSDbar_refresh (int num);
/* END INTERFACE */

static struct _bsdbar {
	char bar;
	struct _bsdbar * next;
} bar1, bar2, bar3;

static struct _bsdbar * _bar_cursor;

void
BSDbar_init (void)
{
    /* write a padding for the bar */
	Write (2, "[ ] ...%", 8);
	/* build a chain cycle */
	bar1.bar = '-';
	bar2.bar = '\\';
	bar3.bar = '/';
	bar1.next = &bar2;
	bar2.next = &bar3;
	bar3.next = &bar1;
	/* point the cursor to bar1 */
	_bar_cursor = &bar1;

	return;
}

/* this function is for internal use */
static void
_BSDbar_refresh (char _bar, int _propor)
{
	/* refresh BSD-style progress bar */
    /* whole buffer of the bar */
	static char bb[8] = {
        '[', ' ', ']', ' ', ' ', ' ', ' ', '%'
    };
	Write (2, "\b\b\b\b\b\b\b\b", 8); /* clear the previous bar */
	snprintf (bb, 8, "[%c] %3d%%", _bar, _propor); /* prepare buffer */
	fflush (NULL); /* sync stdio buffer to user-defined buffer */
	Write (2, bb, 8); /* print the buffer to stderr */
	return;
}

void
BSDbar_refresh (int _propor)
{
    /* note that 'int num' is the proportion to display */
    _BSDbar_refresh (_bar_cursor -> bar, _propor);
	_bar_cursor = _bar_cursor -> next;
    return;
}

void
BSDbar_clear (void)
{
    /* clear the padding/bar and newline*/
	Write (2, "\b\b\b\b\b\b\b\b        \n", 17);
	return;
}

#endif /* BSDBAR_H */
