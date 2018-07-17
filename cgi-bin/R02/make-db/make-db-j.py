#15K1039 山本ゆう大
#問題2

import csv, sqlite3

con = sqlite3.connect(r"..\johnnys.sqlite3")
cur = con.cursor()

try:
    cur.execute("CREATE TABLE johnnys(name TEXT, team TEXT, birthday TEXT, age INT, birthplace TEXT, blood TEXT);")
except sqlite3.OperationalError:
    cur.execute("DELETE FROM johnnys")
    
reader = csv.reader(open('j.txt', 'r',encoding='utf-8-sig'), delimiter=',')
for row in reader:
    for p in row[1].split(","):
        to_db = (row[0], p, row[2], int(row[3]), row[4], row[5])
        cur.execute(
            """INSERT INTO johnnys (name, team, birthday, age, birthplace, blood) 
              VALUES (?, ?, ?, ?, ?, ?);""", 
    to_db)
cur.execute("SELECT name FROM johnnys WHERE team = '嵐'")
print(cur.fetchall())
cur.execute("SELECT * FROM johnnys")
print(cur.fetchall())
con.commit()


try:
    cur.execute("CREATE TABLE cd (team TEXT, title TEXT);")
except sqlite3.OperationalError:
    cur.execute("DELETE FROM cd")

reader = csv.reader(open('j_cd.txt', 'r',encoding='utf-8-sig'), delimiter=',')
for row in reader:
    to_db = (row[0], row[1])
    cur.execute(
        """INSERT INTO cd (team, title) 
              VALUES (?, ?);""", 
    to_db)

i = input()    
cur.execute("SELECT team FROM johnnys WHERE name = ?",(i,))
for j in cur.fetchall():
    print(j)
    cur.execute("SELECT * FROM cd WHERE team = ?", j)
    print(cur.fetchall())
cur.execute("SELECT * FROM cd")
print(cur.fetchall())
con.commit()
con.close()


