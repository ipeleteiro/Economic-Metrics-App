import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

'''
Testing LinearRegression
x = np.array([5, 15, 25, 35, 45, 55]).reshape((-1, 1))
y = np.array([5, 20, 14, 32, 22, 38])

print(x)

model = LinearRegression()
model.fit(x, y)

print('intercept =', model.intercept_)
print("slope =", model.coef_)

# must use 2d arrays for prediction, can resize array to fir this with .reshape((-1, 1))
print("for x= 65, y=", model.predict([[65]]))
'''

# get values from .csv file
# turn them into array
# create models for the data
# predict the values for next 8 quarters in the future

df = pd.read_csv("Current.csv")
df = df.set_index(['country','year'])

data = {}

countries = ["United Kingdom", "United States", "France", "Japan", "Germany", "Canada", "Italy"]
metrics = ['life_expectancy', 'fertility_rate', 'GDP', 'GDP_per_capita', 'GDP_PPP', 'GNI','GNI_per_capita', 'GNI_PPP', 'political_stability', 'interest_rates', 'income_tax', 'education_pct_government_expenditure', 'government_effectiveness', 'labour_participation', 'migration', 'rural_living_pct_popoluation', 'health_pct_government_expenditure', 'government_expenditure_pct_GDP', 'R&D_expenditure_pct_GDP', 'current_account_pct_GDP', 'inflation', 'forest_area', 'global_carbon_budget', 'environmental_occupational_risks', 'greenhouse_gas_emissions', 'renewable_electricity_capacity',  'trade_transport_quality', 'literacy_rate', 'alcohol_use_disorders', 'income_inequality', 'wealth_inequality', 'child_mortality', 'body_mass_index', 'hours_to_file_taxes', 'drug_use', 'mental_health', 'pedestrian_road_injuries', 'pollution', 'bullying_victimisation', 'forest_depletion_pct_GNI', 'unsafe_water', 'unemployment']
for country in countries:
    countryData = {}
    for metric in metrics:
        dfCut = df.loc[country, metric]
        countryData[metric] = dfCut.tolist()
    data[country] = countryData


projectedData = {}
slopesData = {}

for metric in metrics:
    metricList = []
    slopesMetricList = []
    for country in countries:
        x = np.array([i for i in range(2000, 2020)])
        y = np.array(data[country][metric])

        length = 0
        while length < len(y):
            if str(y[length]) == 'nan':
                y = np.delete(y, length)
                x = np.delete(x, length)
            else:
                length = length + 1


        if len(x) == 0:
            for i in range(15):
                metricList.append('NaN')
            slopesMetricList.append('NaN')
            continue

        x = x.reshape((-1, 1))

        model = LinearRegression()
        model.fit(x, y)

        slope = model.coef_
        slopesMetricList.append(slope[0])

        #                    times by 100 since range needs to be integers, will need to divide at the end
        for quarter in range(201900, 202125, 25):
            quarter = quarter/100
            projection = model.predict([[quarter]])
            metricList.append(projection[0])
        for year in range(2025, 2055, 5):
            projection = model.predict([[year]])
            metricList.append(projection[0])
    
    projectedData[metric] = metricList
    slopesData[metric] = slopesMetricList


projectedIndex = []
for country in countries:
    for quarter in range(201900, 202125, 25):
        quarter =  quarter/100
        year = int(quarter//1)
        quarter = int((quarter%1)*4)
        projectedIndex.append((country, str(year)+" QR:"+str(quarter)))
    for year in range(2025, 2055, 5):
        projectedIndex.append((country, str(year)))


projectedIndex = pd.MultiIndex.from_tuples(projectedIndex, names=["country", "date"])


projectedDf = pd.DataFrame(data= projectedData, index=projectedIndex)
projectedDf.to_csv('Projected.csv')

# this is for the economic simulator
slopesDf = pd.DataFrame(data= slopesData, index= countries)
#slopesDf = slopesDf.transpose() # I want the index to be the countries, not the metrics, so reflect it by the diagonal
slopesDf.index.name = 'country'
slopesDf.to_csv('Slopes.csv')



