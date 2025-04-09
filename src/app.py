# -*- coding: utf-8 -*-
'''
    File name: app.py
    Author: Olivia Gélinas (modified for pie/bar chart)
    Course: INF8808
    Python Version: 3.8

    Entry point for the Dash app displaying pie and bar charts.
'''

import dash
from dash import html
from dash import dcc
import pandas as pd
from pie_and_bar_chart6 import plot_condition_vs_injury
from template import create_custom_theme, set_default_theme

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = 'Traffic Accidents Visualization | INF8808'

# Load and prepare data
dataframe = pd.read_csv('src/assets/data/traffic_accidents.csv')  
figure = plot_condition_vs_injury(dataframe)  # Get the pie/bar chart figure

# Apply custom theme
create_custom_theme()
set_default_theme()

# Define the layout
app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Traffic Accidents by Roadway Condition'),
        html.H2('Pie and Bar Chart Visualization')
    ]),
    html.Main(className='viz-container', children=[
        dcc.Graph(
            id='pie-bar-chart',
            className='graph',
            figure=figure,
            config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=True  # Enable mode bar for interactivity
            )
        )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)