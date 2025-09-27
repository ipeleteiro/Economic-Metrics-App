import pandas as pd

df = pd.read_csv('CurrentRaw.csv')
df = df.set_index(['country', 'year'])

df = df.sort_index()    
print(df)

df.to_csv('CurrentRaw.csv')