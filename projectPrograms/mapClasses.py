import pandas as pd
import json
import plotly.express as px


class CCMap:
    def __init__(self, mapColour, mapDataframeName):
        if mapColour == 'blue':
            self.mapColour = ["rgb(200, 240, 255)", "rgb(50, 50, 255)"]
            self.mapMetrics = ['life_expectancy', 'alcohol_use_disorders', 'fertility_rate', 'income_inequality', 'wealth_inequality', 'GDP', 'GDP_per_capita', 'GDP_PPP', 'GNI','GNI_per_capita', 'GNI_PPP','child_mortality', 'political_stability', 'interest_rates', 'body_mass_index','hours_to_file_taxes', 'income_tax', 'education_pct_government_expenditure', 'government_effectiveness', 'labour_participation', 'migration', 'rural_living_pct_popoluation', 'health_pct_government_expenditure', 'government_expenditure_pct_GDP', 'R&D_expenditure_pct_GDP', 'current_account_pct_GDP', 'inflation', 'bullying_victimisation', 'drug_use', 'mental_health', 'pedestrian_road_injuries', 'literacy_rate', 'unemployment']
        elif mapColour == 'green':
            self.mapColour = ["rgb(179, 242, 180)", "rgb(38, 128, 13)"]
            self.mapMetrics = ['pollution', 'forest_area', 'forest_depletion_pct_GNI', 'global_carbon_budget', 'environmental_occupational_risks', 'greenhouse_gas_emissions', 'renewable_electricity_capacity',  'trade_transport_quality',  'unsafe_water','GDP', 'GDP_per_capita', 'GDP_PPP', 'GNI','GNI_per_capita', 'GNI_PPP']
        else:
            return 'inavlid colour'
        self.mapDataframeName = mapDataframeName    
        self.indexName = 'year'
        self.mapDate = 2019
    
    def getMetrics(self):
        return self.mapMetrics

    def getDataframe(self):
        df = pd.read_csv(self.mapDataframeName)
        df = df.set_index(self.indexName)
        df = df.replace("United States", "United States of America")  # the geojson file has a different name, so changing it is necessary
        self.mapDataframe = df
        return self.mapDataframe

    def createMap(self):
        countriesMap = json.load(open("countries.geojson", 'r'))

        df = pd.read_csv(self.mapDataframeName)
        df = df.set_index(self.indexName)
        df = df.loc[self.mapDate]
        df = df.replace("United States", "United States of America")  # the geojson file has a different name, so changing it is necessary
        
        metrics = df.columns.values.tolist()
        for metric in metrics:
            if metric not in self.mapMetrics and metric != 'country':
                df = df.drop(metric, axis=1)
        
        self.mapDataframe = df

        for country in countriesMap['features']:
            country['id'] = country['properties']['ADMIN']
            # adding a new property 'id' to the main list of properties of every country
            # the id is simply the name of the country, as they are unique
            # this is used so the id (country name) can be accessed from the first level of the geojson file

        colorscale = self.mapColour 
        
        ccmap = px.choropleth(df, locations='country', geojson=countriesMap, color='GDP', color_continuous_scale=colorscale, height=500)
  
        userOptions = df.columns.values.tolist()
        del userOptions[0]     # removing 'country' from the list of options, as we only want user to choose between metrics

        return ccmap, userOptions
    
        
class ProjectedCCMap(CCMap):
    def __init__(self, mapColour, mapDataframe):
        CCMap.__init__(self, mapColour, mapDataframe)
        self.indexName = 'date'
        self.mapDate = "2019 QR:0"


class EconSimCCMap(ProjectedCCMap):
    def __init__(self, mapColour, mapDataframe):
        CCMap.__init__(self, mapColour, mapDataframe)
        self.indexName = 'date'
        self.mapDate = "2019 QR:0"
        self.normalMetrics = ['life_expectancy', 'fertility_rate', 'GDP', 'GDP_per_capita', 'GDP_PPP', 'GNI','GNI_per_capita', 'GNI_PPP', 'political_stability', 'interest_rates', 'income_tax', 'education_pct_government_expenditure', 'government_effectiveness', 'labour_participation', 'migration', 'rural_living_pct_popoluation', 'health_pct_government_expenditure', 'government_expenditure_pct_GDP', 'R&D_expenditure_pct_GDP', 'current_account_pct_GDP', 'inflation', 'forest_area', 'global_carbon_budget', 'environmental_occupational_risks', 'greenhouse_gas_emissions', 'renewable_electricity_capacity',  'trade_transport_quality', 'literacy_rate']
        self.oppositeMetrics = ['alcohol_use_disorders', 'income_inequality', 'wealth_inequality', 'child_mortality', 'body_mass_index', 'hours_to_file_taxes', 'drug_use', 'mental_health', 'pedestrian_road_injuries', 'pollution', 'bullying_victimisation', 'forest_depletion_pct_GNI', 'unsafe_water', 'unemployment']
        self.policies = ['Income_Tax', 'Demerit_Goods_Tax', 'Education_Spending', 'Healthcare_Spending', 'Environment_Spending', 'Benefits_Spending', 'Infrastructure', 'Regulation', 'Protectionism', 'Interest_Rates']
        
        dates = []
        for quarter in range(201900, 202125, 25):
            quarter =  quarter/100
            year = int(quarter//1)
            quarter = int((quarter%1)*4)
            dates.append(str(year)+" QR:"+str(quarter))
        dates.append("2025")
        dates.append("2035")
        dates.append("2050")
        self.dates = dates


    def getRules(self):
        policies = ['Income_Tax', 'Demerit_Goods_Tax', 'Education_Spending', 'Healthcare_Spending', 'Environment_Spending', 'Benefits_Spending', 'Regulation', 'Protectionism', 'Interest_Rates', 'Infrastructure']
        # different from self.policies due to the ordering of the Rules table
        df = pd.read_csv('Rules.csv')
        df = df.set_index(['policy', 'date'])
        for metric in self.oppositeMetrics:
            data = []
            for policy in policies:
                for date in self.dates:
                    temp = -1 * df.loc[(policy, date)][metric]
                    if temp == 0:
                        temp = 0
                    data.append(temp) 
            df[metric] = data

        return df
    
    def getEmpty(self):
        df = pd.read_csv('RulesEmpty.csv')
        df = df.set_index(['total', 'date'])
        df = df.replace("United States", "United States of America")
        return df

    def getOptEmpty(self):
        df = pd.read_csv('RulesOptEmpty.csv')
        df = df.set_index(['country', 'date'])
        return df
    
    def getOptPlan(self):
        df = pd.read_csv('EconSimOptPlan.csv')
        df = df.set_index(['country', 'policy'])

        optPlan = {}
        for i in df.index.tolist():
            optPlan[i] = df.loc[i]['amount']

        return optPlan
    
    def getOptPlanText(self, country):
        df = pd.read_csv('EconSimOptPlan.csv')
        df = df.set_index(['country', 'policy'])

        policies = ['Income_Tax', 'Demerit_Goods_Tax', 'Education_Spending', 'Healthcare_Spending', 'Environment_Spending', 'Benefits_Spending', 'Regulation', 'Protectionism', 'Interest_Rates', 'Infrastructure']
                
        optPlanText = []

        for policy in policies:
            temp = policy + ': ' + str((df.loc[(country, policy)]['amount'] * 5)) + '%       \n' 
            optPlanText.append(temp)
        optPlanText = ''.join(optPlanText)

        return optPlanText
