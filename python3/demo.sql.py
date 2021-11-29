#!/usr/bin/python3
'''
https://docs.python.org/3/library/sqlite3.html'
'''
import sqlite3 as db

conn = db.connect('{}.db'.format(__file__))
#conn = db.connect(':memory:') # DataBase in RAM
c = conn.cursor()

# put data into the database
c.execute('''CREATE TABLE scores
             (id real, name text, value real)''')
c.execute('''INSERT INTO scores
             VALUES (1, "anonymous", 100.0)''')
conn.commit()
conn.close() # Changes not commited will be lost.
