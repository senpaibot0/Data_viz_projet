# -*- coding: utf-8 -*-
'''
    File name: app.py
    Author: Anouar Hnnachi
    Course: INF8808
    Python Version: 3.8

    Entry point for the Dash app displaying traffic accident visualizations.
'''

import dash
from dash import html, dcc
import pandas as pd
from pie_and_bar import plot_intersection_vs_injury, plot_condition_vs_injury
from radar_chart2 import create_radar_charts
from serie_temporelle import create_temporal_series
from histogramme_type_jour import create_day_type_histogram
from template import create_custom_theme, set_default_theme
from heatmap import get_figure as get_heatmap_figure

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = 'Traffic Accidents Dashboard | INF8808'

# Load data
import os
csv_path = os.path.join(os.path.dirname(__file__), 'assets/data/traffic_accidents.csv')
dataframe = pd.read_csv(csv_path)

# Generate figures
pie_bar_fig = plot_condition_vs_injury(dataframe)
pie_bar2_fig = plot_intersection_vs_injury(dataframe)
temporal_fig = create_temporal_series(dataframe)
histogram_fig = create_day_type_histogram(dataframe)
radar_fig = create_radar_charts(dataframe)
heatmap_fig = get_heatmap_figure(dataframe)

# Apply custom theme
create_custom_theme()
set_default_theme()

# Define the layout
app.layout = html.Div(
    className='content',
    children=[
        # Header with logo and navigation
        html.Header(
            children=[
                html.Div(
                    style={'display': 'flex', 'alignItems': 'center'},
                    children=[
                        html.Img(
                            src='/assets/canada-logo.jpg',
                            style={'height': '40px', 'marginRight': '20px'}
                        ),
                        html.H1('DASHBOARD DES ACCIDENTS DE LA ROUTE')
                    ]
                ),
                html.Nav(
                    style={'backgroundColor': '#E5E5E5', 'padding': '10px 0', 'marginTop': '10px', 'width': '100%', 'justifyContent': 'center'},
                    children=[
                        html.A('Home', href='#', style={'margin': '0 15px', 'color': '#333', 'textDecoration': 'none'}),
                        html.A('Data', href='#', style={'margin': '0 15px', 'color': '#333', 'textDecoration': 'none'}),
                        html.A('Analysis', href='#', style={'margin': '0 15px', 'color': '#333', 'textDecoration': 'none'}),
                    ]
                )
            ]
        ),
        # Main content
        html.Div(
            className='viz-container',
            children=[
                # Buttons for Visualizations (using anchor tags)
                html.Div(
                    style={'marginBottom': '20px'},
                    children=[
                        html.A(
                            'Série temporelle',
                            href='#temporal-section',
                            style={
                                'padding': '8px 20px',
                                'color': '#333',
                                'textDecoration': 'none',
                                'border': '1px solid #999',
                                'backgroundColor': '#F5F5F5',
                                'fontSize': '14px',
                                'marginRight': '5px',
                                'cursor': 'pointer'
                            }
                        ),
                        html.A(
                            'Type de jour',
                            href='#histogram-section',
                            style={
                                'padding': '8px 20px',
                                'color': '#333',
                                'textDecoration': 'none',
                                'border': '1px solid #999',
                                'backgroundColor': '#F5F5F5',
                                'fontSize': '14px',
                                'marginRight': '5px',
                                'cursor': 'pointer'
                            }
                        ),
                        html.A(
                            'Conditions éclairage/météo',
                            href='#radar-section',
                            style={
                                'padding': '8px 20px',
                                'color': '#333',
                                'textDecoration': 'none',
                                'border': '1px solid #999',
                                'backgroundColor': '#F5F5F5',
                                'fontSize': '14px',
                                'marginRight': '5px',
                                'cursor': 'pointer'
                            }
                        ),
                        html.A(
                            'Matrice de chaleur',
                            href='#heatmap-section',
                            style={
                                'padding': '8px 20px',
                                'color': '#333',
                                'textDecoration': 'none',
                                'border': '1px solid #999',
                                'backgroundColor': '#F5F5F5',
                                'fontSize': '14px',
                                'marginRight': '5px',
                                'cursor': 'pointer'
                            }
                        ),
                        html.A(
                            'Condition chaussée',
                            href='#pie-bar1-section',
                            style={
                                'padding': '8px 20px',
                                'color': '#333',
                                'textDecoration': 'none',
                                'border': '1px solid #999',
                                'backgroundColor': '#F5F5F5',
                                'fontSize': '14px',
                                'marginRight': '5px',
                                'cursor': 'pointer'
                            }
                        ),
                        html.A(
                            'Présence intersection',
                            href='#pie-bar2-section',
                            style={
                                'padding': '8px 20px',
                                'color': '#333',
                                'textDecoration': 'none',
                                'border': '1px solid #999',
                                'backgroundColor': '#F5F5F5',
                                'fontSize': '14px',
                                'marginRight': '5px',
                                'cursor': 'pointer'
                            }
                        ),
                        html.A(
                            'PDF',
                            href='#',
                            style={
                                'padding': '8px 20px',
                                'color': '#333',
                                'textDecoration': 'none',
                                'border': '1px solid #999',
                                'backgroundColor': '#F5F5F5',
                                'fontSize': '14px',
                                'marginLeft': '5px'
                            }
                        )
                    ]
                ),

                html.H2('Statistiques Canada'),
                html.H2(
                    children=[
                        html.Em("Visualiser les tendances des accidents de la route")
                    ],
                    style={
                        'fontFamily': 'Arial, Helvetica, sans-serif',
                        'fontWeight': 'bold'
                    }
                ),
                html.P('Released: 2025-04-23'),
                html.P(
                    'Ce tableau de bord offre un aperçu des accidents de la route, incluant les tendances temporelles, les conditions des accidents et leur gravité. Explorez les données à l’aide de visualisations interactives.'
                ),
                # Temporal Series
                html.Div(
                    id='temporal-section',
                    className='chart-container',
                    children=[
                        html.Div(
                            className='chart-section',
                            children=[
                                html.H3('Série temporelle des accidents de la route', style={'justify-content': 'center'}),
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
                            ]
                        ),
                        html.Div(
                            className='text-section',
                            children=[
                                html.P(
                                    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
                                ),
                                html.P(
                                    'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
                                ),
                                html.P(
                                    'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.'
                                )
                            ]
                        )
                    ],
                    style={'scrollMarginTop': '100px'}
                ),
                # Day Type Histogram
                html.Div(
                    id='histogram-section',
                    className='chart-container',
                    children=[
                        html.H3('Moyenne des accidents selon le type de jour'),
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
                    ],
                    style={'scrollMarginTop': '100px'}
                ),
                # Radar Charts
                html.Div(
                    id='radar-section',
                    className='chart-container',
                    children=[
                        html.H3("Nombre et gravité des accidents selon les conditions d'éclairage et de météo"),
                        html.Div(
                            children=create_radar_charts(dataframe)[0],
                            style={
                                'display': 'flex',
                                'flexDirection': 'row',
                                'justifyContent': 'space-evenly',
                                'flexWrap': 'wrap',
                                'gap': '20px',
                                'width': '100%',
                            }
                        ),
                        html.Div(
                            children=create_radar_charts(dataframe)[1:],
                            style={
                                'display': 'flex',
                                'flexDirection': 'row',
                                'justifyContent': 'space-evenly',
                                'flexWrap': 'wrap',
                                'gap': '20px',
                                'width': '100%',
                            }
                        )
                    ],
                    style={'scrollMarginTop': '100px'}
                ),
                # Heatmap
                html.Div(
                    id='heatmap-section',
                    className='chart-container',
                    children=[
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
                        ),
                    ],
                    style={'scrollMarginTop': '100px'}
                ),
                # Pie/Bar Chart (Road Condition)
                html.Div(
                    id='pie-bar1-section',
                    className='chart-container',
                    children=[
                        html.H3("Nombre d'accidents selon la gravité des blessures et la condition de la chaussée"),
                        dcc.Graph(
                            id='pie-bar1-chart',
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
                    ],
                    style={'scrollMarginTop': '100px'}
                ),
                # Pie/Bar Chart (Intersection)
                html.Div(
                    id='pie-bar2-section',
                    className='chart-container',
                    children=[
                        html.H3("Nombre d'accidents selon la gravité des blessures et la présence/absence d'intersection"),
                        dcc.Graph(
                            id='pie-bar2-chart',
                            className='graph',
                            figure=pie_bar2_fig,
                            config=dict(
                                scrollZoom=False,
                                showTips=False,
                                showAxisDragHandles=False,
                                doubleClick=False,
                                displayModeBar=True
                            )
                        ),
                        html.Div(
                            children=[
                                html.P(
                                    "Cette visualisation établit le nombre de blessures en fonction de leur gravité selon s'il y a présence ou absence d'une intersection d'une part et d'autre part selon la condition de la chaussée.",
                                    style={
                                        'fontFamily': 'Arial, Helvetica, sans-serif',
                                        'fontSize': '14px',
                                        'color': '#333',
                                        'textAlign': 'justify',
                                        'maxWidth': '85%'
                                    }
                                ),
                                html.P(
                                    "Elle montre que la majorité des accidents se produit à l'approche d'une intersection, mais que ces accidents sont majoritairement sans blessure. Il en est de même en ce qui concerne la condition de la chaussée.",
                                    style={
                                        'fontFamily': 'Arial, Helvetica, sans-serif',
                                        'fontSize': '14px',
                                        'color': '#333',
                                        'textAlign': 'justify',
                                        'maxWidth': '85%'
                                    }
                                ),
                                html.P(
                                    "Une attention particulière devrait être portée sur les blessures mortelles et incapacitantes en cas d'intersection et de chaussée sèche.",
                                    style={
                                        'fontFamily': 'Arial, Helvetica, sans-serif',
                                        'fontSize': '14px',
                                        'color': '#333',
                                        'textAlign': 'justify',
                                        'maxWidth': '85%'
                                    }
                                )
                            ],
                            style={
                                'marginTop': '30px'
                            }
                        )
                    ],
                    style={'scrollMarginTop': '100px', 'marginBottom': '60px'}
                ),
                # JavaScript for chart visibility animation only
                html.Script(
                    '''
                    document.addEventListener("DOMContentLoaded", function() {
                        const elements = document.querySelectorAll(".chart-container");
                        const observer = new IntersectionObserver((entries) => {
                            entries.forEach(entry => {
                                if (entry.isIntersecting) {
                                    entry.target.classList.add("visible");
                                }
                            });
                        }, { threshold: 0.1 });

                        elements.forEach(element => {
                            observer.observe(element);
                        });
                    });
                    '''
                )
            ]
        )
    ]
)