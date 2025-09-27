import pandas as pd

df = pd.read_csv('EconSimOptPlan.csv')
df = df.set_index(['country', 'policy'])

print(df)

countries = ["Italy", "United Kingdom", "United States", "France", "Japan", "Germany", "Canada"]
policies = ['Income_Tax', 'Demerit_Goods_Tax', 'Education_Spending', 'Healthcare_Spending', 'Environment_Spending', 'Benefits_Spending', 'Regulation', 'Protectionism', 'Interest_Rates', 'Infrastructure']
        

optPlanTexts = {}
for country in countries:
    countryText = []
    for policy in policies:
        temp = policy + ': ' + str(df.loc[(country, policy)]['amount']) + '\n'
        countryText.append(temp)
    countryText = ''.join(countryText)
    optPlanTexts[country] = countryText

print(optPlanTexts)
for countries in country:
    print(optPlanTexts[country])