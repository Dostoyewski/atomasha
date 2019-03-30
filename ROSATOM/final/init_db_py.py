import sqlite3
import os

def get_parent_dir(directory):
    return os.path.dirname(directory)



conn = sqlite3.connect("data.db")
cursor = conn.cursor()



conn = sqlite3.connect("data.db")
cursor = conn.cursor()

sql_idd="""
CREATE TABLE idd(
uid STRING,
uname STRING,
role STRING);
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
conn.close()