# -*- coding: utf-8 -*-
'''
    File name: app.py
    Author: Olivia Gélinas (modified for multiple visualizations)
    Course: INF8808
    Python Version: 3.8

    Entry point for the Dash app displaying traffic accident visualizations.
'''

import dash
from dash import html
from dash import dcc
import pandas as pd
from pie_and_bar_chart6 import plot_condition_vs_injury
from serie_temporelle import create_temporal_series
from histogramme_type_jour import create_day_type_histogram
from template import create_custom_theme, set_default_theme

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = 'Traffic Accidents Dashboard | INF8808'

# Load data
dataframe = pd.read_csv('src/assets/data/traffic_accidents.csv')  # Adjust path as needed

# Generate figures
pie_bar_fig = plot_condition_vs_injury(dataframe)
temporal_fig = create_temporal_series(dataframe)
histogram_fig = create_day_type_histogram(dataframe)

# Apply custom theme
create_custom_theme()
set_default_theme()

# Define the layout
app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Traffic Accidents Dashboard'),
        html.H2('Visualizing Accident Patterns')
    ]),
    html.Main(className='viz-container', children=[
        html.Div(children=[
            html.H3('Accidents by Roadway Condition and Injury Severity'),
            dcc.Graph(
                id='pie-bar-chart',
                className='graph',
                figure=pie_bar_fig,
                config=dict(
                    scrollZoom=False,
                    showTips=False,
                    showAxisDragHandles=False,
                    doubleClick=False,
                    displayModeBar=True
                )
            )
        ]),
        html.Div(children=[
            html.H3('Temporal Series of Accidents'),
            dcc.Graph(
                id='temporal-series',
                className='graph',
                figure=temporal_fig,
                config=dict(
                    scrollZoom=False,
                    showTips=False,
                    showAxisDragHandles=False,
                    doubleClick=False,
                    displayModeBar=True
                )
            )
        ]),
        html.Div(children=[
            html.H3('Average Accidents by Day Type'),
            dcc.Graph(
                id='day-type-histogram',
                className='graph',
                figure=histogram_fig,
                config=dict(
                    scrollZoom=False,
                    showTips=False,
                    showAxisDragHandles=False,
                    doubleClick=False,
                    displayModeBar=True
                )
            )
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)