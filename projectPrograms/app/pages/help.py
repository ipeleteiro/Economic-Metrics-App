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
dash.register_page(__name__, name="Help")

image_path = 'assets/helpForCurrent.png'


layout = html.Div(
    [

        dbc.Row(
            html.Img(src=image_path)
        )

    ]
)
