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
dash.register_page(__name__, path='/', name="Current Map")

# MAP CLASSES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SCurrentData = CCMap('blue', 'Current.csv')
ECurrentData = CCMap('green', 'Current.csv')

SCurrentRawData = CCMap('blue', 'CurrentRaw.csv')
ECurrentRawData = CCMap('green', 'CurrentRaw.csv')

currentMaps = {'SCurrentData': SCurrentData, 'ECurrentData': ECurrentData}
currentRawMaps = {'SCurrentRawData': SCurrentRawData, 'ECurrentRawData': ECurrentRawData}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


ccmap, userOptions = currentMaps['SCurrentData'].createMap()
df = currentMaps['SCurrentData'].getDataframe()
df = df.loc[currentMaps['SCurrentData'].mapDate]
years = []
for i in range(2000,2020):
    years.append(i)

layout = html.Div(
    [

        dbc.Row(
            dcc.Dropdown(options=['Environment', 'Social'],
                            id='map-choiceC',
                            value='Social',
                            clearable=False
            )
        ),

        html.Hr(),
        
        dbc.Row(
            dcc.RadioItems(options=years,
                            id='date-choiceC',
                            value=2019,
                            inline=True,
                            labelStyle={'padding':'10px'}
            )
        ),

        html.Div(id='warningC', style= {'textAlign':'center'}),

        dbc.Row(
            dcc.RadioItems(options=['Indexed Data', 'Raw Data'],
                            id='data-choiceC',
                            value='Indexed Data',
                            inline = True,
                            labelStyle={'padding':'10px'}
            )
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Checklist(options=currentMaps['SCurrentData'].getMetrics(),
                                       id='metric-choiceC')
                    ], xs=4, sm=3, md=2, lg=2, xl=2, xxl=2
                ),
                
                dbc.Col(
                    [
                        dcc.Graph(id='currentMap',  
                                  figure= ccmap)
                    ], xs=8, sm=9, md=10, lg=10, xl=10, xxl=10
                )
            ]
        ),

        html.Hr(),

    ]
)

@callback(
    Output(component_id='metric-choiceC', component_property='options'),
    Input(component_id='map-choiceC', component_property='value')
)
def setMetricChoices(mapChoice):
    if mapChoice == 'Environment':
        return currentMaps['ECurrentData'].getMetrics()
    elif mapChoice == 'Social':
        return currentMaps['SCurrentData'].getMetrics()
    else:
        return []

@callback(
    Output(component_id='metric-choiceC', component_property='value'),
    Input(component_id='metric-choiceC', component_property='options')
)
def setInitialValue(metricOptions):
    value = metricOptions[0]
    return [value]

@callback(
    Output(component_id='warningC', component_property='children'),
    Input(component_id='metric-choiceC', component_property='value')
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
    Output(component_id='currentMap', component_property='figure'),
    [Input(component_id='metric-choiceC', component_property='value'),
     Input(component_id='date-choiceC', component_property='value'),
     Input(component_id='map-choiceC', component_property='value'),
     Input(component_id='data-choiceC', component_property='value')]
)
def update_graph(metricChoice, dateChoice, mapChoice, dataChoice):
    patchedFig = Patch()

    if dataChoice == 'Indexed Data':
        df = currentMaps['SCurrentData'].getDataframe()
    elif dataChoice == 'Raw Data':
        df = currentRawMaps['SCurrentRawData'].getDataframe()


    df = df.loc[dateChoice]


    if mapChoice == 'Environment':
        userOptions = currentMaps['ECurrentData'].getMetrics()    # list of metrics is same for raw and indexed
        metrics = df.columns.values.tolist()
        for metric in metrics:
            if metric not in userOptions and metric != 'country':
                df = df.drop(metric, axis=1)       
        patchedFig['layout']['coloraxis']['colorscale'] = ((0.0, "rgb(179, 242, 180)"), (1.0, "rgb(38, 128, 13)"))

    elif mapChoice == 'Social':
        userOptions = currentMaps['SCurrentData'].getMetrics()
        metrics = df.columns.values.tolist()
        for metric in metrics:
            if metric not in userOptions and metric != 'country':
                df = df.drop(metric, axis=1)
        patchedFig['layout']['coloraxis']['colorscale'] = ((0.0, "rgb(200, 240, 255)"), (1.0,  "rgb(50, 50, 255)")) 

        # add change in colour


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
        patchedFig['layout']['coloraxis']['colorbar']['title']['text'] = '('+dataChoice+') ' + metricChoice[0]
        patchedFig['data'][0]['hovertemplate'] = 'country=%{location}<br>'+ metricChoice[0] +'=%{z}<extra></extra>'
    else:
        patchedFig['layout']['coloraxis']['colorbar']['title']['text'] = '('+dataChoice+') ' + 'Average'
        patchedFig['data'][0]['hovertemplate'] = 'country=%{location}<br>Average=%{z}<extra></extra>'

        # inside the geojson file, the hovertemplate is the following: 'country=%{location}<br>GDP=%{z}<extra></extra>' 
        # to change the metric, I simply need to change the name of the metric (from GDP to whatever ‘value’ is being chosen)

    return patchedFig
