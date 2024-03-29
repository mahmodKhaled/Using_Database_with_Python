## the solution of the assignment of week 3 :

import sqlite3
import xml.etree.ElementTree as ET

conn = sqlite3.connect('DB4.sqlite')
cur = conn.cursor()

cur.executescript('''
    DROP TABLE IF EXISTS Artist;
    DROP TABLE IF EXISTS Album;
    DROP TABLE IF EXISTS Genre;
    DROP TABLE IF EXISTS Track;

    CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);''')

inp = input('Enter a file: ')
if len(inp) < 1 : inp = 'Library.xml'

def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None
file = ET.parse(inp)
data = file.findall('dict/dict/dict')
print('Dict count: ',len(data))
for line in data :
    if lookup(line,'Track ID') is None : continue
    title = lookup(line,'Name')
    artist = lookup(line,'Artist')
    album = lookup(line,'Album')
    genre = lookup(line,'Genre')
    len = lookup(line,'Total Time')
    rating = lookup(line,'Rating')
    count = lookup(line,'Play Count')
    if artist is None or album is None or title is None or genre is None : continue 
    print(title, artist, album, genre, count, rating, len)
    cur.execute('''INSERT OR IGNORE INTO Artist(name) VALUES (?)''',(artist,))
    cur.execute('''SELECT id FROM Artist WHERE name = ?''',(artist,))
    artist_id = cur.fetchone()[0]
    cur.execute('''INSERT OR IGNORE INTO Album(title,artist_id) VALUES (?,?)''',(album,artist_id))
    cur.execute('''SELECT id FROM Album WHERE title = ?''',(album,))
    album_id = cur.fetchone()[0]
    cur.execute('''INSERT OR IGNORE INTO Genre(name) VALUES (?)''',(genre,))
    cur.execute('''SELECT id FROM Genre WHERE name = ?''',(genre,))
    genre_id = cur.fetchone()[0]
    cur.execute('''INSERT OR IGNORE INTO Track(title,album_id,genre_id,len,rating,count) 
    VALUES (?,?,?,?,?,?)''',(title,album_id,genre_id,len,rating,count))
    conn.commit()
    
some important sql commands :

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);



SELECT Track.title, Artist.name, Album.title, Genre.name 
    FROM Track JOIN Genre JOIN Album JOIN Artist 
    ON Track.genre_id = Genre.ID and Track.album_id = Album.id 
        AND Album.artist_id = Artist.id
    ORDER BY Artist.name LIMIT 3