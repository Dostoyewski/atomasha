import sqlite3
import time
global answer
global file
file = 'data.db'

conn = sqlite3.connect(file)
cursor = conn.cursor()



def onload(id, uname, role):
    data1 = [(id, uname, role)]
    cursor.executemany("INSERT INTO idd(uid, uname, role) VALUES (?,?,?)", data1)
    conn.commit()
    
def search(arg):
    sql = "SELECT * FROM idd WHERE uname=?"
    cursor.execute(sql, [(str(arg))])
    print(cursor.fetchall())
    
    
#onload(2,2,6,1,1)
#onload('JdjtjvHMmtjnJa9DsoyJLq8BjyvnsrhsjD', 'FeDOS', 'admin')
onload()
search('JdjtjvHMmtjnJa9DsoyJLq8BjyvnsrhsjD')
time.sleep(5)
conn.close()
   