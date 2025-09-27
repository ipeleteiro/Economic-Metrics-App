import pandas as pd



df = pd.read_csv('Rules.csv')
df = df.set_index(['policy', 'date'])

normalMetrics = ['life_expectancy', 'fertility_rate', 'GDP', 'GDP_per_capita', 'GDP_PPP', 'GNI','GNI_per_capita', 'GNI_PPP', 'political_stability', 'interest_rates', 'income_tax', 'education_pct_government_expenditure', 'government_effectiveness', 'labour_participation', 'migration', 'rural_living_pct_popoluation', 'health_pct_government_expenditure', 'government_expenditure_pct_GDP', 'R&D_expenditure_pct_GDP', 'current_account_pct_GDP', 'inflation', 'forest_area', 'global_carbon_budget', 'environmental_occupational_risks', 'greenhouse_gas_emissions', 'renewable_electricity_capacity',  'trade_transport_quality', 'literacy_rate']
oppositeMetrics = ['alcohol_use_disorders', 'income_inequality', 'wealth_inequality', 'child_mortality', 'body_mass_index', 'hours_to_file_taxes', 'drug_use', 'mental_health', 'pedestrian_road_injuries', 'pollution', 'bullying_victimisation', 'forest_depletion_pct_GNI', 'unsafe_water', 'unemployment']
policies = ['Income_Tax', 'Demerit_Goods_Tax', 'Education_Spending', 'Healthcare_Spending', 'Environment_Spending', 'Benefits_Spending', 'Regulation', 'Protectionism', 'Interest_Rates', 'Infrastructure']

print(df)

dates = []
for quarter in range(201900, 202125, 25):
    quarter =  quarter/100
    year = int(quarter//1)
    quarter = int((quarter%1)*4)
    dates.append(str(year)+" QR:"+str(quarter))
dates.append("2025")
dates.append("2035")
dates.append("2050")



for metric in oppositeMetrics:
    data = []
    for policy in policies:
        for date in dates:
            temp = -1 * df.loc[(policy, date)][metric]
            if temp == 0:
                temp = 0
            data.append(temp) 
    df[metric] = data

print(df)