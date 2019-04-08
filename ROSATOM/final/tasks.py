import pandas as pd

docs= pd.read_excel('docs.xlsx')
for doc in docs.values:
    print('приказ' in doc[0].lower())