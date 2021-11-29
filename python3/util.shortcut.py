#!/usr/bin/python3
# http://www.tkdocs.com/tutorial/index.html
'''
Tkinter python3 program
the following packages are required:
  python3-tk

https://docs.python.org/3/library/tkinter.ttk.html
'''

import tkinter as tk
from tkinter import ttk
from subprocess import call

class TkApp(object):
    def __init__(self):
        # Root Window
        self.root = tk.Tk()
        self.root.title('My Shortcuts')
        self.root.bind('<q>', lambda e: self.root.destroy())
        # setup ttk theme/style
        ttk.Style().configure("TButton", padding=6, relief='flat',
            background='#ccc', font=('Inconsolata', 11))
        ttk.Style().configure("TLabel", padding=6, relief='flat',
            font=('Inconsolata', 9))
        # Root Frame
        self.rootframe = ttk.Frame(self.root, borderwidth=8)
        self.rootframe.grid(column=0, row=0)
        # Status Bar
        self.status = ttk.Label(self.root, text='..')
        self.status.grid(column=0, row=1, pady=0, padx=0, sticky=(tk.W))
        # Control Frame <- Root Frame 
        self.controlframe = ttk.LabelFrame(self.rootframe, text='Shortcuts')
        self.controlframe.grid(column=1, row=0, sticky=tk.N)
        # components/instance <- Control Frame
        self.quit = ttk.Button(self.controlframe, text='Quit', command=self.cb_quit)
        self.stub1 = ttk.Label(self.controlframe, text='')
        self.rs3700k = ttk.Button(self.controlframe, text="redshift 3700K", command=self.cb_redshift3700k)
        self.rsbar = ttk.Scale(self.controlframe, from_=1000, to=10000, orient=tk.HORIZONTAL, length=200)
        self.rsbar.set(1000)
        self.rsbut = ttk.Button(self.controlframe, text="redshift -O{}".format(self.rsbar.get()), command=self.cb_redshiftscale)
        self.fun3 = ttk.Button(self.controlframe, text='repeat rate (Xorg)', command=self.cb_function3)
        # components/grid <- Control Frame
        self.quit.grid(column=0, row=0, padx=5, pady=5, sticky=tk.N)
        self.stub1.grid(column=0, row=1)
        self.rs3700k.grid(column=0, row=2, padx=5, pady=5)
        self.rsbut.grid(column=0, row=7, padx=5, pady=5)
        self.fun3.grid(column=0, row=5, padx=5, pady=5)
        self.rsbar.grid(column=0, row=6, padx=5, pady=5)
        self.rsbar.bind('<B1-Motion>', self.bardrag)
    def cb_quit(self):
        self.status['text'] = 'quit'
        self.root.destroy()
    def cb_redshift3700k(self):
        self.status['text'] = 'redshift on (3700K)'
        call("redshift -O3700".split())
    def cb_function3(self):
        self.status['text'] = 'key repeat rate'
        call("xset r rate 160 160".split())
    def cb_redshiftscale(self):
        self.status['text'] = 'redshift ' + str(self.rsbar.get()) + 'K'
        call("redshift -O{}".format(self.rsbar.get()).split())
    def run(self):
        self.root.mainloop()
    def bardrag(self, ev):
        print('mouse motion', ev.x, ev.y, 'value', self.rsbar.get())

if __name__ == '__main__':
    app = TkApp()
    app.run()
