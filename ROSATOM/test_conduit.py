import pandas as pd
username = 'tot'
conduit = pd.read_excel('conduit.xlsx')
fail = 0
for i in range(0, len(conduit[mes])):
    if(conduit[mes][i] == 0):
        fail += 1
    print(fail)
print('Статистика: \n' + 'Количество пропусков: ' + str(fail))