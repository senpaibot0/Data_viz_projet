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
from radar_chart2 import create_radar_charts
from serie_temporelle import create_temporal_series
from histogramme_type_jour import create_day_type_histogram
from template import create_custom_theme, set_default_theme
from heatmap import get_figure as get_heatmap_figure

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = 'Traffic Accidents Dashboard | INF8808'

# # Load data
# dataframe = pd.read_csv('src/assets/data/traffic_accidents.csv')  # Adjust path as needed
import os
csv_path = os.path.join(os.path.dirname(__file__), '/assets/data/traffic_accidents.csv')
dataframe = pd.read_csv(csv_path)


# Generate figures
pie_bar_fig = plot_condition_vs_injury(dataframe)
temporal_fig = create_temporal_series(dataframe)
histogram_fig = create_day_type_histogram(dataframe)
radar_fig = create_radar_charts(dataframe)
heatmap_fig = get_heatmap_figure(dataframe)

# Apply custom theme
create_custom_theme()
set_default_theme()

# Define the layout
app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Traffic Accidents Dashboard'),
        html.H2('Visualizing Accident Patterns')
    ]),
    # html.Main(className='viz-container', children=[
    #     html.Div(children=[
    #         html.H3('Accidents by Roadway Condition and Injury Severity'),
    #         dcc.Graph(
    #             id='pie-bar-chart',
    #             className='graph',
    #             figure=pie_bar_fig,
    #             config=dict(
    #                 scrollZoom=False,
    #                 showTips=False,
    #                 showAxisDragHandles=False,
    #                 doubleClick=False,
    #                 displayModeBar=True
    #             )
    #         )
    #     ]),
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
        ]),
        html.Div(children=[
            html.H3("Accidents selon les conditions d'éclairage et de météo"),
            html.Div(
                children=create_radar_charts(dataframe),
                style={
                    'display': 'flex',
                    'flexDirection': 'row',
                    'justifyContent': 'space-evenly',
                    'flexWrap': 'nowrap',  # Set to 'wrap' if too many charts overflow
                    'overflowX': 'auto',  # Optional: allow scrolling if too many charts
                    'gap': '20px'
                }
            )
        ]),
        html.Div(children=[
        html.H3('Matrice de chaleur des accidents par type de collision et gravité des blessures'),
        dcc.Graph(
            id='heatmap-chart',
            className='graph',
            figure=heatmap_fig,
            config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=True
                )
            )
        ]),
        html.Div(className='viz-container', children=[
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
        ])    
    ])
])


