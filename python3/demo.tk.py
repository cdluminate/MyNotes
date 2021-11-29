#!/usr/bin/python3
# http://www.tkdocs.com/tutorial/index.html
'''
Tkinter python3 program
the following packages are required:
  python3-tk
  python3-pil
  python3-pil.imagetk
'''

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

print('Create root window...')

root = tk.Tk()
root.title('My Application')
root.bind('<q>', lambda e: root.destroy())

print('Load resources...')
image = Image.open('test.jpg')
image = image.resize((240, 320), Image.ANTIALIAS)#image.show()
image = ImageTk.PhotoImage(image)

print('Create child windows...')
rootframe = tk.Frame(root, borderwidth=8)
rootframe.grid(column=0, row=0)

status = tk.Label(root, text='This is status')
status.grid(column=0, row=1, pady=0, padx=0, sticky=(tk.W))

imageframe = tk.LabelFrame(rootframe, text='Images')
imageframe.grid(column=0, row=0)
controlframe = tk.LabelFrame(rootframe, text='Control')
controlframe.grid(column=1, row=0, sticky=tk.N)
statusframe = tk.Frame(rootframe)
statusframe.grid(column=0, row=0)

im1 = tk.Label(imageframe, image=image)
im1.grid(column=0, row=0, padx=5, pady=5)
im2 = tk.Label(imageframe, image=image)
im2.grid(column=1, row=0, padx=5, pady=5)

def callback_quit():
  status['text'] = 'quit'
  root.destroy()
quit = tk.Button(controlframe, text='Quit', command=callback_quit)
quit.grid(column=0, row=0, padx=5, pady=5, sticky=tk.N)

stub1 = tk.Label(controlframe, text='')
stub1.grid(column=0, row=1)

def callback_function1():
  status['text'] = 'invoke function1'
fun1 = tk.Button(controlframe, text='fun1', command=callback_function1)
fun1.grid(column=0, row=2, padx=5, pady=5)

def callback_function2():
  status['text'] = 'invoke function2'
fun2 = tk.Button(controlframe, text='fun2', command=callback_function2)
fun2.grid(column=0, row=3, padx=5, pady=5)

def callback_function3():
  status['text'] = 'invoke function3'
fun3 = tk.Button(controlframe, text='fun3', command=callback_function3)
fun3.grid(column=0, row=4, padx=5, pady=5)

print('Main loop...')
root.mainloop()

print('Quit.')
