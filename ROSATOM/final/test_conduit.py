import pandas as pd
username = 'tot'
'''conduit = pd.DataFrame(columns=[])
conduit.index.name = 'user' 
conduit = conduit.append(pd.Series({'08.04.2019': 1}, name = 'tot'))
s = pd.DataFrame(columns=[])
s = s.append(pd.Series({'09.04.2019': 1}, name = 'tot'))
print(s)
conduit = pd.concat([conduit, s], axis=1)
s1 = pd.DataFrame(columns=[])
s1.index.name = 'user' 
s1 = conduit.append(pd.Series({'09.04.2019': 1}, name = 'FeDOS'))
conduit = conduit.append(s1)
fail = 0
for i in range(0, len(conduit[username])):
    if(conduit[username][i] == 0):
        fail += 1
    print(fail)
print('Статистика: \n' + 'Количество пропусков: ' + str(round(fail/len(conduit[username])*100))+'%')
print(conduit)
conduit.to_excel('new_conduit.xlsx')'''

conduit = pd.read_excel('new_conduit.xlsx')
print(conduit)
s1 = pd.DataFrame(columns=[])
conduit = conduit.append(pd.Series({'user': 'Tot2', '09.04.2019': 1}), ignore_index=True)
print(conduit)
s = pd.DataFrame(columns=[])
s = s.append(pd.Series({'user': 'Tot2','10.04.2019': 1}), ignore_index=True)
conduit = pd.merge(conduit, s, on='user', how='outer')
print(conduit)