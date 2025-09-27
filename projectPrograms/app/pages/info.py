import pandas as pd
import json
import plotly.express as px
import dash
from dash import html, dcc, callback, Output, Input, Patch, dash_table
import dash_bootstrap_components as dbc


import sys
sys.path.append('/Users/irenepeleteiropaniagua/Documents/shhs/computing/projectPrograms')
from mapClasses import *

# registering this page as the homepage (path='/') to the app registry
dash.register_page(__name__, name="Information")

df = pd.read_csv('Info.csv')

layout = html.Div(
    [
        dbc.Row([
            html.H4('About the software'),
            html.P('With this software I wanted to solve the following problem: there is currently no easy way to understand the wellbeing and economy of a country without simply looking at its GDP (or other factors individually). GDP is known to have many problems and could be seen as an outdated metric. Most modern economists now care more about the environmental and social issues rather than simple growth, making sure the population actually benefits from decisions made by governments and firms, and so use metrics relating directly to these issues. For this reason, I want to create a program in which the user can: view and compare countries’ social and environmental qualities; see projections, and advice on what should be done to improve them; and use an economic simulator to test out their policies with an ‘optimised’ plan to compare against. This could allow the public to easily check the current economic picture, and allow policy makers to find the current problems and see possible solutions.')
        ]),

        dbc.Row([
            html.H4('The Data'),
            html.P('All data is imported from Our World in Data and World Bank.')
        ]),

        dbc.Row([
            html.H4('The Process'),
            html.H5('Indexing'),
            html.P('To index the data, the program starts by finding the mean and standard deviation of each metric. It then sets a maximum value as 2 standard deviations above the mean, and a minimum as 2 standard deviations below (if any of the G7 data are above/below these, they are sets as the minimum/maximum). The algorithm then calculates the index value of the G7 countries based on this minimum and maximum, so all data is within 0-1 and can be easily compared and averaged.'),
            html.H5('Projections'),
            html.P('The algorithm creates a linear model based on the 2000-2019 data and uses linear regression to get the projections.'),
            html.H5('Optimum Plan'),
            html.P("The optimum plan is calculated based on an adjusted version of Dijkstra's algorithm to find the 'optimum' route to take with the policies.")
        ]),

        dbc.Row([
            html.H4('The Metrics'),
            html.H6('Below are descriptions of all of the metrics included in the application:'),

            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in df.columns],
                style_cell={'textAlign': 'left'},
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                }
            )
        ])

    ]
)
