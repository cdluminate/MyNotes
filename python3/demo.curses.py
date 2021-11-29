#!/usr/bin/python3
'''
https://docs.python.org/3/howto/curses.html
'''
# UTF8

#import curses
#''' curses is shipped in standard python package '''
#
#def main():
#  sc = curses.initscr()
#  curses.noecho()
#
#  sc.clear()
#  sc.border(0)
#  sc.addstr(12, 25, "Python curses!")
#  sc.refresh()
#  key = sc.getch()
#  curses.endwin()
#
#main()

import curses
import time

def main2(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.start_color()
    stdscr.clear()

    for i in range(10):
        time.sleep(0.1)
        stdscr.addstr(i+1, 1, 'square of {} is {}\n'.format(i, i**2))
        stdscr.refresh()

    stdscr.refresh()

    stdscr.addstr(20, 1, "Pretty text", curses.color_pair(1) | curses.A_BOLD | curses.A_UNDERLINE)
    stdscr.refresh()

    for i in range(101):
        time.sleep(0.1)
        stdscr.addstr(12, 1, 'progress ... {:.0%}'.format(i/100.))
        stdscr.refresh()

    vertex_x, vertex_y, xoff, yoff = 20, 7, 40, 5
    win = curses.newwin(yoff, xoff, vertex_y, vertex_x)
    stdscr.border(0)
    #pad = curses.newpad(100, 100)
    stdscr.refresh()

    stdscr.getkey()

curses.wrapper(main2)
