import pandas as pd

df = pd.read_csv("Projected.csv")
df = df.set_index('date')

df['date'] = df.index
print(df)
df = df.reset_index(drop=True)

df = df.set_index(['country', 'date'])

print(df)

test = df.loc[('Italy', '2019 QR:0')]

print(df.index[0])
tempC = []
tempD = []
for i in df.index:
    tempC.append(i[0])
    tempD.append(i[1])

print(tempD, tempC)

df['date'] = tempD
df['country'] = tempC
df = df.reset_index(drop=True)
df = df.set_index('date')
print(df)