import pandas as pd
import datetime
def init():
    tasks = pd.DataFrame(columns=['username','task', 'time'])
    tasks.to_excel('tasks.xlsx')
#init()
tasks = pd.read_excel('tasks.xlsx')
print(tasks)
print(tasks.loc[tasks['username'] == 'tot'].values)

now = datetime.date.today()
print(str(now))
n =  str(now).split('-')
print(n)
n.reverse()
print(n)
for task in tasks.loc[tasks['username'] == 'tot'].values:
    print('03.04.2019'=='.'.join(n))