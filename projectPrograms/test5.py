import pandas as pd
from mapClasses import *

SEconSim = EconSimCCMap('blue', 'Projected.csv')
EEconSim = EconSimCCMap('green', 'Projected.csv')

econSimMaps = {'SEconSim': SEconSim, 'EEconSim': EEconSim}


ccmap, userOptions = econSimMaps['SEconSim'].createMap()
df = econSimMaps['SEconSim'].getDataframe()
df = df.loc[econSimMaps['SEconSim'].mapDate]

dates = econSimMaps['SEconSim'].dates


dfRules = econSimMaps['SEconSim'].getRules()


df = pd.read_csv('RulesOptEmpty.csv')
df = df.set_index(['country', 'date'])

countries = ["Italy", "United Kingdom", "United States", "France", "Japan", "Germany", "Canada"]
totalRules = df
optPlan =  econSimMaps['SEconSim'].getOptPlan()
print(optPlan)

for country in countries:
    for policy in econSimMaps['SEconSim'].policies:
        sumOfRules = dfRules.loc[policy] * optPlan[(country, policy)]
        print(sumOfRules)
        total = totalRules.add(sumOfRules, fill_value=0)
        print(total)
        totalRules.loc[country] = total

print(totalRules)
totalRules.to_csv('ihate.csv')