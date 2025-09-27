import pandas as pd

df = pd.read_csv("Rules.csv")
df = df.set_index(['policy','date'])


policies = ['Income Tax', 'Demerit Goods Tax', 'Education Spending', 'Healthcare Spending', 'Environment Spending', 'Benefits Spending', 'Interest Rates', 'Regulation', 'Protectionism', 'Infrastructure']


'''print(df.loc['Demerit Goods Tax'])
print(df.loc['Demerit Goods Tax'].sum(axis='index'))
print(df.loc['Demerit Goods Tax'].sum(axis='index').sum())
'''
temp = df.loc['Protectionism'].sum(axis='index')
temp = temp*10
temp = temp.astype(int)
s = temp.sum()
print(s/10)
temp = temp/10
print(temp)
print(temp.sum())

# policy = {'policy2': dist}

nodes = {}

for policy in policies:
    temp = df.loc[policy].sum(axis='index')
    temp = temp*10
    temp = temp.astype(int)
    s = temp.sum()
    nodes[policy] = s/10

print(nodes)


