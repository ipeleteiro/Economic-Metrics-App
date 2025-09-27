import pandas as pd

df = pd.read_csv('Rules.csv')
df = df.set_index(['policy', 'date'])

df = df.sort_index()    
print(df)
print(df['GDP'].sum())