## second assignment of week 2 in using database with python :

import sqlite3
conn = sqlite3.connect('DB2.sqlite')
cur = conn.cursor()
cur.execute('''DROP TABLE IF EXISTS Counts''')
cur.execute('''CREATE TABLE Counts(org TEXT , count INTEGER)''')

file_name = input('Enetr file: ')
if len(file_name) <1 : file_name = 'mbox.txt'
data = open(file_name)
for line in data :
    if not line.startswith('From: ') : continue 
    pieces = line.split()
    email = pieces[1]
    email_cutting = email.split('@')
    org = email_cutting[1]
    cur.execute('SELECT count FROM Counts WHERE org = ? ',(org,))
    row = cur.fetchone()
    if row is None :
        cur.execute('''INSERT INTO Counts(org,count) VALUES (?,1)''',(org,))
    else :
        cur.execute('''UPDATE Counts SET count = count +1 WHERE org = ?''',(org,))
    conn.commit()
sqlrt = ('SELECT org , count FROM Counts ORDER BY count DESC LIMIT 10')
for r in cur.execute(sqlrt) :
    print(str(r[0]),r[1])
cur.close()
