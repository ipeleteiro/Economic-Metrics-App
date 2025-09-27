import pandas as pd
import json
import plotly.express as px


countriesMap = json.load(open("countries.geojson", 'r'))

df = pd.read_csv('Current.csv')
df = df.set_index('year')
df = df.loc[2019]
df = df.replace("United States", "United States of America")  # the geojson file has a different name, so changing it is necessary
        
metrics = df.columns.values.tolist()
for metric in metrics:
    if metric not in ['life_expectancy', 'alcohol_use_disorders', 'fertility_rate', 'income_inequality', 'wealth_inequality', 'GDP', 'GDP_per_capita', 'GDP_PPP', 'GNI','GNI_per_capita', 'GNI_PPP','child_mortality', 'political_stability', 'interest_rates', 'body_mass_index','hours_to_file_taxes', 'income_tax', 'education_pct_government_expenditure', 'government_effectiveness', 'labour_participation', 'migration', 'rural_living_pct_popoluation', 'health_pct_government_expenditure', 'government_expenditure_pct_GDP', 'R&D_expenditure_pct_GDP', 'current_account_pct_GDP', 'inflation', 'bullying_victimisation', 'drug_use', 'mental_health', 'pedestrian_road_injuries', 'literacy_rate', 'unemployment'] and metric != 'country':
        df = df.drop(metric, axis=1)
        


for country in countriesMap['features']:
    country['id'] = country['properties']['ADMIN']
            # adding a new property 'id' to the main list of properties of every country
            # the id is simply the name of the country, as they are unique
            # this is used so the id (country name) can be accessed from the first level of the geojson file

colorscale =  ["rgb(200, 240, 255)", "rgb(50, 50, 255)"]
#self.mapColour = ["rgb(200, 240, 255)", "rgb(50, 50, 255)"]
#self.mapColour = ["rgb(179, 242, 180)", "rgb(38, 128, 13)"]

        
ccmap = px.choropleth(df, locations='country', geojson=countriesMap, color='GDP', color_continuous_scale=colorscale, height=500)
print(ccmap['layout']['coloraxis']['colorscale'])
print(ccmap['layout']['coloraxis']['colorscale'][0][1])
print(ccmap['layout']['coloraxis']['colorscale'][1][1])

ccmap['layout']['coloraxis']['colorscale'] = ((0.0, "rgb(38, 128, 13)"), (1.0, "rgb(179, 242, 180)"))

print(ccmap['layout']['coloraxis']['colorscale'])