/*
 * fir_flags.h
 *
 * header of fir_chess 
 * it contains some functions to judge stage in game.
 */

#include <stdio.h>

int 
db (char *msg)  
{
	/* print debug message */
	fputs ("db : ", stderr);
	fputs (msg, stderr);
	fputs ("\n", stderr);
	return 0;
}

int
flagwin (char g[15][15], char token)
{
	/* to judge if a player who holds token is win.
	 * the **g is game board.
	 * the size is of game board. 
	 */
	int size = 15; /* size of board */

	/* gx and gy is g-locator on game board */
	int gx, gy;

	/* wx and wy : worker locator */
	int wx, wy;

	/* dx and dy : direction, a vector */
	int dx, dy;

	/* score of each scan. */
	int score;

	/* figure out flag of winnning. */
	/* try row by row, in a row one by one test */
	for (gy = 0; gy < size; gy++) {
	for (gx = 0; gx < size; gx++) {
		/* if here (gx, gy) occupied token */
		if (g[gy][gx] == token) {
			/* from here, test all directions */
			for (dy = -1; dy < 2; dy++) {
			for (dx = -1; dx < 2; dx++) {

				/* if directin is invalid */
				if (dy == 0 && dx == 0)
					continue;

				/* move worker here */
				wy = gy;
				wx = gx;
				/* initial score */
				score = 0;

				/* count score on current direction */
				while (
					/* ensure that no going beyond */
					wx >= 0 && wx < size &&
					wy >= 0 && wy < size &&
					/* ensure if this location placed a token */
					g[wy][wx] == token
				      ) {
					/* add 1 score and move worker along direction */
					score++;
					wy = wy + dy;
					wx = wx + dx;
				}

				/* if score >= 5 */
				if (score >= 5) {
					db ("win!");
					return 1;
				}
			}
			}
		}
	}
	}
	/* this means no one win */
	return 0;
}
