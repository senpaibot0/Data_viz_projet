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
                                    "Cette visualisation a pour objectif d’analyser la répartition temporelle des accidents de la route selon différents critères : l’heure de la journée, le jour de la semaine, le mois et l’année. En identifiant les périodes les plus à risque, nous visons à sensibiliser les usagers de la route et à orienter les actions de prévention."
                                ),
                                html.P(
                                    "Points saillants : Par heure, les accidents culminent entre 15h et 18h, heures de pointe associées aux retours à la maison. Par jour de semaine, le vendredi enregistre le plus grand nombre d’accidents, tandis que le dimanche est le jour le moins accidentogène. Par mois, le mois d’octobre montre un pic, possiblement lié à la baisse de luminosité et aux conditions météo variables. Par année, une hausse marquée est observée entre 2015 et 2019, suivie d’une relative stabilité."
                                ),
                                html.P(
                                    "Cette analyse met en évidence des moments critiques où la prudence doit être redoublée, notamment en fin d’après-midi et les vendredis. Nous encourageons les conducteurs à adapter leur conduite aux conditions de circulation, à éviter les distractions et à prévoir des marges de sécurité accrues lors des périodes identifiées comme à risque. Une vigilance accrue peut contribuer à sauver des vies."
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
                        ),
                        html.Div(
                            className='text-section',
                            children=[
                                html.P(
                                    "Cette visualisation présente un histogramme comparant la moyenne quotidienne des accidents de la route selon trois types de jours : les jours ordinaires, les fins de semaine et les jours fériés. L’objectif est de dégager des tendances en fonction du calendrier et de mieux cibler les périodes à risque."
                                ),
                                html.P(
                                    "Points saillants : Les jours ordinaires présentent la moyenne d’accidents la plus élevée, probablement liée aux déplacements domicile-travail et à la densité du trafic. Les fins de semaine affichent une moyenne légèrement inférieure, mais restent élevées, peut-être en raison des déplacements récréatifs ou festifs. Les jours fériés enregistrent la plus faible moyenne, ce qui pourrait s’expliquer par une circulation réduite."
                                ),
                                html.P(
                                    "Bien que les jours fériés soient les moins accidentogènes, les jours ordinaires et les fins de semaine demeurent des périodes critiques nécessitant vigilance et prudence."
                                )
                            ]
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
                        ),
                        html.Div(
                            className='text-section',
                            children=[
                                html.P(
                                    "Cette série de visualisations examine comment les conditions d’éclairage (plein jour, crépuscule, nuit éclairée ou sombre) et les conditions météorologiques (dégagé, nuageux, pluie, neige) influencent à la fois le nombre et la gravité des accidents de la route."
                                ),
                                html.P(
                                    "Points saillants : En plein jour, malgré une visibilité optimale, le nombre d’accidents est le plus élevé, possiblement en raison d’un faux sentiment de sécurité, d’une densité de circulation accrue ou d’une vigilance réduite. La majorité des accidents surviennent sous un temps dégagé, indépendamment de l’éclairage. Les conditions extrêmes comme la neige ou la pluie sont associées à moins d’accidents, mais ceux-ci peuvent être plus graves. Peu importe les conditions, les accidents sans blessure dominent, mais des blessures mortelles ou incapacitantes surviennent dans tous les contextes."
                                ),
                                html.P(
                                    "Contrairement à l’intuition, ce ne sont pas les conditions difficiles qui génèrent le plus d’accidents, mais bien les situations perçues comme sécuritaires. Cela montre que la vigilance ne doit jamais être relâchée, même par beau temps ou en plein jour. Une conduite attentive en tout temps est essentielle pour réduire les risques."
                                )
                            ]
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
                        html.Div(
                            className='text-section',
                            children=[
                                html.P(
                                    "Cette heatmap illustre la relation entre cinq types de collision routière et la gravité des blessures résultantes, révélant clairement que la majorité des accidents n’entraînent pas de blessures visibles, indépendamment du type de collision."
                                ),
                                html.P(
                                    "Les collisions lors de virages (Turning) et à angle produisent le plus grand nombre d’accidents sans blessure apparente, suivies par les collisions par l’arrière, tandis que les accidents impliquant des piétons sont moins fréquents mais présentent une proportion plus élevée de blessures par rapport au nombre total d’incidents de ce type."
                                ),
                                html.P(
                                    "Bien que la plupart des accidents ne causent pas de blessures graves, une attention particulière devrait être portée aux collisions en virage et aux intersections où des mesures d’infrastructure et de signalisation pourraient réduire considérablement le nombre d’accidents."
                                )
                            ]
                        )
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