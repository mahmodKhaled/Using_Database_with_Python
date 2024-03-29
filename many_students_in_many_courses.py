## it is the solution to assignment of week 4 :

import json 
import sqlite3

conn = sqlite3.connect('roster.sqlite')
cur = conn.cursor()

cur.executescript('''
    DROP TABLE IF EXISTS User;
    DROP TABLE IF EXISTS Course;
    DROP TABLE IF EXISTS Member;

    CREATE TABLE User (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE
    );
    CREATE TABLE Course (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        title TEXT UNIQUE
    );
    CREATE TABLE Member (
        user_id INTEGER,
        course_id INTEGER,
        role INTEGER,
        PRIMARY KEY (user_id,course_id)
    );''')

fname = input('Enter file name: ')
if len(fname) < 1 : fname = 'roster_data.json'
fname2 = open(fname).read()
data = json.loads(fname2)
for line in data :
    name = line[0]
    title = line[1]
    role = line[2]
    print((name , title , role))
    cur.execute('''INSERT OR IGNORE INTO User(name) VALUES (?)''',(name,))
    cur.execute('''SELECT id FROM User WHERE name = ?''',(name,))
    user_id = cur.fetchone()[0]
    cur.execute('''INSERT OR IGNORE INTO Course(title) VALUES (?)''',(title,))
    cur.execute('''SELECT id FROM Course WHERE title = ?''',(title,))
    course_id = cur.fetchone()[0]
    cur.execute('''INSERT OR REPLACE INTO Member(user_id,course_id,role)
    VALUES(?,?,?)''',(user_id,course_id,role))
    conn.commit()

important sql command :

SELECT hex(User.name || Course.title || Member.role ) AS X FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X