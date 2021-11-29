/*
 * reference: http://invisible-island.net/ncurses/ncurses-intro.html
 */

#include <signal.h>
#include <unistd.h>
#include <curses.h> // -lncurses

#include <cstdlib>
#include <cstring>
#include <cmath> // maybe -lm

#include <iostream>
#include <string>
#include <vector>

static void
finish(int sig)
{
	endwin();
	exit(0);
}

int
main(int argc, char *argv[])
{
	(void) signal(SIGINT, finish);

	(void) initscr();
	keypad(stdscr, TRUE);
	(void) nonl();
	(void) cbreak();
	(void) echo();

	// https://stackoverflow.com/questions/19614156/c-curses-remove-blinking-cursor-from-game
	curs_set(0); // no blinking cursor;

	if (has_colors()) {
		start_color();
		init_pair(1, COLOR_RED,   COLOR_BLACK);
		init_pair(2, COLOR_GREEN, COLOR_BLACK);
		init_pair(3, COLOR_YELLOW,COLOR_BLACK);
		init_pair(4, COLOR_BLUE,  COLOR_BLACK);
		init_pair(5, COLOR_MAGENTA,COLOR_BLACK);
		init_pair(6, COLOR_CYAN,  COLOR_BLACK);
		init_pair(7, COLOR_WHITE, COLOR_BLACK);
	}

	// sine wave
	{
		char buf[] = "                                       ";
		for (double t = 0.; t < 0.3*3.14; t+=3.1415926/1000.) {
			double x = (sin(t)+1.)/2.; // x \in [0., 1.]

			snprintf(buf, sizeof(buf), "t=%lf, x=%lf, row=%d, col=%d", t, x, (int)(.5*LINES), (int)(x*COLS));
			//mvaddstr(0, 0, buf);
			//mvaddch((int)(.5*LINES), (int)(x*COLS), '*');
			for (int i = 0; i < 7; i++) {
				attrset(COLOR_PAIR(i) | A_BOLD);
				x = (sin(t + i*(3.14159/4.))+1.)/2.;
				mvaddch((int)(.5*LINES), (int)(x*COLS), '*');
			}

			refresh();
			usleep(2500);
			clear();
		}
	}

	// revolving arches
	{
		clear();
		float radius = (LINES < COLS) ? LINES/2. : COLS/2.;
		std::pair<float, float> centre {LINES/2., COLS/2.}; // origin point
		for (float theta = 0.; theta < 10*3.14; theta += 3.14/100.) {
			for (int j = 0; j < 3.14*radius/4; j++) {
				auto p = std::pair<float, float> {
					radius*cos(-theta - j*3.14/LINES) + centre.first,
					2.*radius*sin(-theta - j*3.14/LINES) + centre.second  // for wide screen
				}; // (rho,theta) -> (x, y)
				auto p_Int = std::pair<int, int> {(int)(p.first), (int)(p.second)};
				mvaddch(p_Int.first, p_Int.second, '*');
			}
			refresh();
			usleep(1000*10);
			clear();
		}
	}

	finish(0);
	return 0;
}
