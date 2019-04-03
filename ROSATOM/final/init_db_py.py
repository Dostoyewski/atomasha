import sqlite3
import os


def onload(id, uname, role, position, salary, cid):
    data1 = [(id, uname, role, position, salary, cid)]
    cursor.executemany("INSERT INTO idd(uid, uname, role, position, salary, cid) VALUES (?,?,?,?,?,?)", data1)
    conn.commit()
    
def search(arg):
    sql = "SELECT * FROM idd WHERE uname=?"
    cursor.execute(sql, [(str(arg))])
    print(cursor.fetchall())

conn = sqlite3.connect("data.db")
cursor = conn.cursor()



conn = sqlite3.connect("data.db")
cursor = conn.cursor()

sql_idd="""
CREATE TABLE idd(
uid STRING,
uname STRING,
role STRING,
position STRING,
salary FLOAT,
cid STRING);
"""

sql_tasks="""
CREATE TABLE tasks(
id STRING NOT NULL,
name STRING NOT NULL,
descr STRING NOT NULL,
date REAL NOT NULL);
"""


cursor.executescript(sql_idd)
cursor.executescript(sql_tasks)

conn.commit()
#conn.close()
onload('id', 'FeDOS', 'admin', 'CTO', 150000, '069442')
onload('id', 'FeDOS', 'admin', 'CTO', 150000, '069442')
