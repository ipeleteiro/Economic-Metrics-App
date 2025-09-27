import pandas as pd
import json
import plotly.express as px
import dash
from dash import html, dcc, callback, Output, Input, Patch
import dash_bootstrap_components as dbc

import sys
sys.path.append('/Users/irenepeleteiropaniagua/Documents/shhs/computing/projectPrograms')
from mapClasses import *

# registering this page as the homepage (path='/') to the app registry
dash.register_page(__name__, name="Optimum Plan")

# MAP CLASSES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SEconSim = EconSimCCMap('blue', 'Projected.csv')
EEconSim = EconSimCCMap('green', 'Projected.csv')

econSimMaps = {'SEconSim': SEconSim, 'EEconSim': EEconSim}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


ccmap, userOptions = econSimMaps['SEconSim'].createMap()
df = econSimMaps['SEconSim'].getDataframe()
df = df.loc[econSimMaps['SEconSim'].mapDate]

dates = econSimMaps['SEconSim'].dates

layout = html.Div(
    [
        dbc.Row(
            dcc.Dropdown(options=["Italy", "United Kingdom", "United States of America", "France", "Japan", "Germany", "Canada"],
                            id='country-choice',
                            value='Italy',
                            clearable=False
            )
        ),

        dbc.Row(
            dcc.Textarea(id='optPlanText', value= '', disabled=True, style= {'textAlign':'center', 'height': 260})
        ),

        #DROPDOWN OPTION BETWEEN SOCIAL AND ENVIRONMENT
        dbc.Row(
            dcc.Dropdown(options=['Environment', 'Social'],
                            id='map-choiceO',
                            value='Social',
                            clearable=False
            )
        ),

        html.Hr(),

        dbc.Row(
            dcc.RadioItems(options=dates,
                            id='date-choiceO',
                            value='2019 QR:0',
                            inline=True,
                            labelStyle={'padding':'10px'}
            )
        ),

        html.Div(id='warningO', style= {'textAlign':'center'}),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Checklist(options=econSimMaps['SEconSim'].getMetrics(),
                                      id='metric-choiceO')
                    ], xs=4, sm=3, md=2, lg=2, xl=2, xxl=2
                ),
                
                dbc.Col(
                    [
                        dcc.Graph(id='optPlanMap',  
                                  figure= ccmap)
                    ], xs=8, sm=9, md=10, lg=10, xl=10, xxl=10
                )
            ]
        ),

        html.Hr(),

    ]
)

@callback(
    Output(component_id='metric-choiceO', component_property='options'),
    Input(component_id='map-choiceO', component_property='value')
)
def setMetricChoices(mapChoice):
    if mapChoice == 'Environment':
        return econSimMaps['EEconSim'].getMetrics()
    elif mapChoice == 'Social':
        return econSimMaps['SEconSim'].getMetrics()
    else:
        return []

@callback(
    Output(component_id='metric-choiceO', component_property='value'),
    Input(component_id='metric-choiceO', component_property='options')
)
def setInitialValue(metricOptions):
    value = metricOptions[0]
    return [value]

@callback(
    Output(component_id='warningO', component_property='children'),
    Input(component_id='metric-choiceO', component_property='value')
)
def changeWaring(metricChoice):
    if len(metricChoice) > 0:
        for metric in metricChoice:
            if metric in ['income_tax','hours_to_file_taxes','governement_effectiveness','education_pct_government_expenditure','interest_rates','trade_transport_quality','political_stability','fertility_rate','literacy_rate']:
                newWarning = 'At least one of the metrics selected is missing some data.'
                break
            else:
                newWarning = ''
        return newWarning
    else:
        return 'At least one metric must be selected.'

@callback(
    Output(component_id='optPlanText', component_property='value'),
    Input(component_id='country-choice', component_property='value')
)
def changeWaring(countryChoice):
    optPlanText = econSimMaps['SEconSim'].getOptPlanText(countryChoice)
    return optPlanText



@callback(
    Output(component_id='optPlanMap', component_property='figure'),
    [Input(component_id='metric-choiceO', component_property='value'),
     Input(component_id='date-choiceO', component_property='value'),
     Input(component_id='map-choiceO', component_property='value')]
)
def update_graph(metricChoice, dateChoice, mapChoice):
    patchedFig = Patch()

    df = econSimMaps['SEconSim'].getDataframe()
    df = df.loc[dateChoice]

    dfRules = econSimMaps['SEconSim'].getRules()

    
    countries = ["Italy", "United Kingdom", "United States of America", "France", "Japan", "Germany", "Canada"]
    totalRules = econSimMaps['SEconSim'].getOptEmpty()
    optPlan =  econSimMaps['SEconSim'].getOptPlan()
    for country in countries:
        for policy in econSimMaps['SEconSim'].policies:
            sumOfRules = dfRules.loc[policy] * optPlan[(country, policy)]
            total = totalRules.add(sumOfRules, fill_value=0)
            totalRules.loc[country] = total
        

    df['date'] = df.index
    df = df.reset_index(drop=True)
    df = df.set_index(['country', 'date'])         # setting a different axis so the data can be accessed and modified
    for country in countries:
        df.loc[(country, dateChoice)] = df.loc[(country, dateChoice)]*(1 + totalRules.loc[(country, dateChoice)]/100)   


    tempC = []                       # resetting the index to be only 'data'
    tempD = []
    for i in df.index:
        tempC.append(i[0])
        tempD.append(i[1])
    df['date'] = tempD
    df['country'] = tempC
    df = df.reset_index(drop=True)
    df = df.set_index('date')


    if mapChoice == 'Environment':
        userOptions = econSimMaps['SEconSim'].getMetrics()    # list of metrics is same for raw and indexed
        metrics = df.columns.values.tolist()
        for metric in metrics:
            if metric not in userOptions and metric != 'country':
                df = df.drop(metric, axis=1)
        patchedFig['layout']['coloraxis']['colorscale'] = ((0.0, "rgb(179, 242, 180)"), (1.0, "rgb(38, 128, 13)"))

    elif mapChoice == 'Social':
        userOptions = econSimMaps['SEconSim'].getMetrics()
        metrics = df.columns.values.tolist()
        for metric in metrics:
            if metric not in userOptions and metric != 'country':
                df = df.drop(metric, axis=1)
        patchedFig['layout']['coloraxis']['colorscale'] = ((0.0, "rgb(200, 240, 255)"), (1.0,  "rgb(50, 50, 255)")) 
    

    if len(metricChoice) == 0:
        mean = []
    elif len(metricChoice) == 1:
        mean = df[metricChoice].values.tolist()
        fix = []
        for i in range(len(mean)):
            fix.append(mean[i][0])
        mean = fix
    elif len(metricChoice) > 1:
        dataList = df[metricChoice[0]]
        for i in range(len(metricChoice)-1):
            i += 1
            dataList = pd.concat([dataList, df[metricChoice[i]]], axis=1)
        mean = dataList.mean('columns')
        mean = mean.tolist()
    
    patchedFig['data'][0]['z'] = mean

    if len(metricChoice) == 0:
        pass
    elif len(metricChoice) == 1:
        patchedFig['layout']['coloraxis']['colorbar']['title']['text'] = metricChoice[0]
        patchedFig['data'][0]['hovertemplate'] = 'country=%{location}<br>'+ metricChoice[0] +'=%{z}<extra></extra>'
    else:
        patchedFig['layout']['coloraxis']['colorbar']['title']['text'] = 'Average'
        patchedFig['data'][0]['hovertemplate'] = 'country=%{location}<br>Average=%{z}<extra></extra>'

        # inside the geojson file, the hovertemplate is the following: 'country=%{location}<br>GDP=%{z}<extra></extra>' 
        # to change the metric, I simply need to change the name of the metric (from GDP to whatever ‘value’ is being chosen)

    return patchedFig
