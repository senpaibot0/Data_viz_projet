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
temporal_fig = create_temporal_series(dataframe)
histogram_fig = create_day_type_histogram(dataframe)
heatmap_fig = get_heatmap_figure(dataframe)
pie_bar_fig = plot_condition_vs_injury(dataframe)
pie_bar2_fig = plot_intersection_vs_injury(dataframe)

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
                    children=[
                        html.Img(
                            src='/assets/canada-logo.jpg',
                            style={'height': '40px', 'marginRight': '20px'}
                        ),
                        html.H1('TABLEAU DE BORD DES ACCIDENTS DE LA ROUTE', style={'fontSize': '33.5px'}),
                    ],
                    style={'display': 'flex', 'alignItems': 'center'},
                ),
                html.Nav(
                    children=[
                        html.A('Accueil', href='#', className='header-nav-button'),
                        html.A('Données', href='#', className='header-nav-button'),
                        html.A('Analyses', href='#', className='header-nav-button'),
                    ],
                    style={
                        'backgroundColor': '#336b95', 
                        'padding': '10px 0px', 
                        'marginTop': '10px', 
                        'width': '100%'
                    },
                )
            ]
        ),
        # Main content
        html.Div(
            className='viz-container',
            children=[
                html.Div(
                    className='nav-bar',
                    # style={'marginBottom': '20px'},
                    children=[
                        html.A(
                            'Série temporelle',
                            href='#temporal-section',
                            className='nav-button',
                        ),
                        html.A(
                            'Type de jour',
                            href='#histogram-section',
                            className='nav-button',
                        ),
                        html.A(
                            "Conditions d'éclairage/météo",
                            href='#radar-section',
                            className='nav-button',
                        ),
                        html.A(
                            'Type de collision',
                            href='#heatmap-section',
                            className='nav-button',
                        ),
                        html.A(
                            'Condition de chaussée',
                            href='#pie-bar1-section',
                            className='nav-button',
                        ),
                        html.A(
                            "Présence d'intersection",
                            href='#pie-bar2-section',
                            className='nav-button',
                        ),
                        # html.A(
                        #     'PDF',
                        #     href='#',
                        #     className='nav-button',
                        # )
                    ]
                ),
                # html.H2('Statistique Canada | Statistic Canada',),
                html.P(
                    'Released: 2025-04-25',
                    className='general-text', 
                    style={
                        'fontSize': '10px', 
                        'textAlign': 'right',
                        'marginTop': '2rem',
                    }
                ),
                html.H2(
                    children=[
                        html.Em(
                            "Visualiser les tendances des accidents de la route", 
                            style={'fontSize': '30px'},
                        ),
                    ],
                    style={
                        'fontFamily': 'Lato, sans-serif',
                        'fontWeight': 'bold',
                        'marginTop': '1rem',
                    }
                ),
                html.P(
                    'Ce tableau de bord offre un aperçu des accidents de la route, incluant les tendances temporelles, les conditions des accidents et leur gravité. Explorez les données à l’aide de visualisations interactives.',
                    className='general-text',
                    style={
                        'marginTop': '1rem',
                    }
                ),
                # Temporal Series
                html.H3('Selon plusieurs échelles temporelles'),
                html.P(
                    'Cette visualisation a pour objectif d’analyser la répartition temporelle des accidents de la route selon différents critères : l’heure de la journée, le jour de la semaine, le mois et l’année. En identifiant les périodes les plus à risque, nous visons à sensibiliser les usagers de la route et à orienter les actions de prévention.',
                    className='general-text',
                    style={
                        'marginTop': '1rem',
                    }
                ),
                html.Div(
                    id='temporal-section',
                    className='chart-container',
                    children=[
                        html.Div(
                            className='chart-section',
                            children=[
                                dcc.Graph(
                                    id='temporal-series',
                                    className='graph',
                                    figure=create_temporal_series(dataframe),
                                    config=dict(
                                        displayModeBar=True,
                                        displaylogo=False,
                                        scrollZoom=False,
                                        showTips=False,
                                        showAxisDragHandles=False,
                                        doubleClick='reset',
                                        modeBarButtonsToRemove=[
                                            'select2d', 'lasso2d', 'pan2d', 'zoomIn2d', 'zoomOut2d',
                                            'autoScale2d', 'resetScale2d', 'hoverClosestCartesian',
                                            'hoverCompareCartesian', 'toggleSpikelines', 'toImage'
                                        ],
                                        modeBarButtonsToKeep=['zoom2d']
                                    )
                                )
                            ]
                        ),
                        html.P(
                            "Par heure, les accidents culminent entre 15h et 18h, heures de pointe associées aux retours à la maison. Par jour de semaine, le vendredi enregistre le plus grand nombre d’accidents, tandis que le dimanche est le jour le moins accidentogène. Par mois, le mois d’octobre montre un pic, possiblement lié à la baisse de luminosité et aux conditions météo variables. Par année, une hausse marquée est observée entre 2015 et 2019, suivie d’une relative stabilité.",
                            className='under-chart-text',
                            style={
                                'marginTop': '1rem',
                            }
                        ),
                        html.P(
                            "Cette analyse met en évidence des moments critiques où la prudence doit être redoublée, notamment en fin d’après-midi et les vendredis. Nous encourageons les conducteurs à adapter leur conduite aux conditions de circulation, à éviter les distractions et à prévoir des marges de sécurité accrues lors des périodes identifiées comme à risque. Une vigilance accrue peut contribuer à sauver des vies.",
                            className='under-chart-text',
                            style={
                                'marginTop': '1rem',
                            }
                        ),
                    ],
                    style={'scrollMarginTop': '100px'}
                ),
                html.Hr(className='divider'),
                # Day Type Histogram
                html.H3("Selon le type de jour de l'année"),
                html.P(
                    'Cette visualisation présente un histogramme comparant la moyenne quotidienne des accidents de la route selon trois types de jours : les jours ordinaires, les fins de semaine et les jours fériés. L’objectif est de dégager des tendances en fonction du calendrier et de mieux cibler les périodes à risque.',
                    className='general-text',
                    style={
                        'marginTop': '1rem',
                    }
                ),
                html.Div(
                    id='histogram-section',
                    className='chart-container',
                    children=[
                        dcc.Graph(
                            id='day-type-histogram',
                            className='graph',
                            figure=create_day_type_histogram(dataframe),
                            config=dict(
                                displayModeBar=True,
                                displaylogo=False,
                                scrollZoom=False,
                                showTips=False,
                                showAxisDragHandles=False,
                                doubleClick='reset',
                                modeBarButtonsToRemove=[
                                    'select2d', 'lasso2d', 'pan2d', 'zoomIn2d', 'zoomOut2d',
                                    'autoScale2d', 'resetScale2d', 'hoverClosestCartesian',
                                    'hoverCompareCartesian', 'toggleSpikelines', 'toImage'
                                ],
                                modeBarButtonsToKeep=['zoom2d']
                            )
                        ),
                        html.P(
                            "Les jours ordinaires présentent la moyenne d’accidents la plus élevée, probablement liée aux déplacements domicile-travail et à la densité du trafic. Les fins de semaine affichent une moyenne légèrement inférieure, mais restent élevées, peut-être en raison des déplacements récréatifs ou festifs. Les jours fériés enregistrent la plus faible moyenne, ce qui pourrait s’expliquer par une circulation réduite.",
                            className='under-chart-text',
                            style={
                                'marginTop': '1rem',
                            }
                        ),
                        html.P(
                            "Bien que les jours fériés soient les moins accidentogènes, les jours ordinaires et les fins de semaine demeurent des périodes critiques nécessitant vigilance et prudence.",
                            className='under-chart-text',
                            style={
                                'marginTop': '1rem',
                            }
                        ),
                    ],
                    style={'scrollMarginTop': '100px'}
                ),
                html.Hr(className='divider'),
                # Radar Charts
                html.H3("Selon les conditions d'éclairage et de météo et la gravité des blessures"),
                html.P(
                    'Cette série de visualisations examine comment les conditions d’éclairage (plein jour, crépuscule, nuit éclairée ou sombre) et les conditions météorologiques (dégagé, nuageux, pluie, neige) influencent à la fois le nombre et la gravité des accidents de la route.',
                    className='general-text',
                    style={
                        'marginTop': '1rem',
                    }
                ),
                html.Div(
                    id='radar-section',
                    className='chart-container',
                    children=[
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
                        html.P(
                            'En plein jour, malgré une visibilité optimale, le nombre d’accidents est le plus élevé, possiblement en raison d’un faux sentiment de sécurité, d’une densité de circulation accrue ou d’une vigilance réduite. La majorité des accidents surviennent sous un temps dégagé, indépendamment de l’éclairage.',
                            className='under-chart-text',
                            style={
                                'marginTop': '1rem',
                            }
                        ),
                        html.Div(
                            children=create_radar_charts(dataframe)[1:3],
                            style={
                                'display': 'flex',
                                'flexDirection': 'row',
                                'justifyContent': 'space-evenly',
                                'flexWrap': 'wrap',
                                'gap': '20px',
                                'width': '100%',
                            }
                        ),
                        html.P(
                            'Les conditions extrêmes comme la neige ou la pluie sont associées à moins d’accidents, mais ceux-ci peuvent être plus graves. Peu importe les conditions, les accidents sans blessure dominent, mais des blessures mortelles ou incapacitantes surviennent dans tous les contextes.',
                            className='under-chart-text',
                            style={
                                'marginTop': '1rem',
                            }
                        ),
                        html.Div(
                            children=create_radar_charts(dataframe)[3:],
                            style={
                                'display': 'flex',
                                'flexDirection': 'row',
                                'justifyContent': 'space-evenly',
                                'flexWrap': 'wrap',
                                'gap': '20px',
                                'width': '100%',
                            }
                        ),
                        html.P(
                            'Contrairement à l’intuition, ce ne sont pas les conditions difficiles qui génèrent le plus d’accidents, mais bien les situations perçues comme sécuritaires. Cela montre que la vigilance ne doit jamais être relâchée, même par beau temps ou en plein jour. Une conduite attentive en tout temps est essentielle pour réduire les risques.',
                            className='under-chart-text',
                            style={
                                'marginTop': '1rem',
                            }
                        ),
                    ],
                    style={'scrollMarginTop': '100px'}
                ),
                html.Hr(className='divider'),
                # Heatmap
                html.H3('Selon le type de collision et la gravité des blessures'),
                html.P(
                    'Cette heatmap illustre la relation entre cinq types de collision routière et la gravité des blessures résultantes, révélant clairement que la majorité des accidents n’entraînent pas de blessures visibles, indépendamment du type de collision.',
                    className='general-text',
                    style={
                        'marginTop': '1rem',
                    }
                ),
                html.Div(
                    id='heatmap-section',
                    className='chart-container',
                    children=[
                        dcc.Graph(
                            id='heatmap-chart',
                            className='graph',
                            figure=heatmap_fig,
                            config=dict(
                                displayModeBar=True,
                                displaylogo=False,
                                scrollZoom=False,
                                showTips=False,
                                showAxisDragHandles=False,
                                doubleClick='reset',
                                modeBarButtonsToRemove=[
                                    'select2d', 'lasso2d', 'pan2d', 'zoomIn2d', 'zoomOut2d',
                                    'autoScale2d', 'resetScale2d', 'hoverClosestCartesian',
                                    'hoverCompareCartesian', 'toggleSpikelines', 'toImage'
                                ],
                                modeBarButtonsToKeep=['zoom2d']
                            )
                        ),
                        html.P(
                            'Les collisions lors de virages (Turning) et à angle produisent le plus grand nombre d’accidents sans blessure apparente, suivies par les collisions par l’arrière, tandis que les accidents impliquant des piétons sont moins fréquents mais présentent une proportion plus élevée de blessures par rapport au nombre total d’incidents de ce type.',
                            className='under-chart-text',
                            style={
                                'marginTop': '1rem',
                            }
                        ),
                        html.P(
                            'Bien que la plupart des accidents ne causent pas de blessures graves, une attention particulière devrait être portée aux collisions en virage et aux intersections où des mesures d’infrastructure et de signalisation pourraient réduire considérablement le nombre d’accidents.',
                            className='under-chart-text',
                            style={
                                'marginTop': '1rem',
                            }
                        ),
                    ],
                    style={'scrollMarginTop': '100px'}
                ),
                html.Hr(className='divider'),
                # Pie/Bar Chart (Road Condition)
                html.H3("Selon la condition de la chaussée et la gravité des blessures"),
                html.P(
                    'Cette visualisation établit le nombre de blessures en fonction de la condition de la chaussée.',
                    className='general-text',
                    style={
                        'marginTop': '1rem',
                    }
                ),
                html.Div(
                    id='pie-bar1-section',
                    className='chart-container',
                    children=[
                        dcc.Graph(
                            id='pie-bar1-chart',
                            className='graph',
                            figure=plot_condition_vs_injury(dataframe),
                            config=dict(
                                displayModeBar=True,
                                displaylogo=False,
                                scrollZoom=False,
                                showTips=False,
                                showAxisDragHandles=False,
                                doubleClick='reset',
                                modeBarButtonsToRemove=[
                                    'select2d', 'lasso2d', 'pan2d', 'zoomIn2d', 'zoomOut2d',
                                    'autoScale2d', 'resetScale2d', 'hoverClosestCartesian',
                                    'hoverCompareCartesian', 'toggleSpikelines', 'toImage'
                                ],
                                modeBarButtonsToKeep=['zoom2d']
                            )
                        ),
                        html.P(
                            "Elle montre que la majorité des accidents se produit à l'approche d'une intersection, mais que ces accidents sont majoritairement sans blessure. Il en est de même en ce qui concerne la condition de la chaussée.",
                            className='under-chart-text',
                            style={
                                'marginTop': '1rem',
                            }
                        ),
                    ],
                    style={'scrollMarginTop': '100px'}
                ),
                html.Hr(className='divider'),
                # Pie/Bar Chart (Intersection)
                html.H3("Selon la présence/absence d'intersection et la gravité des blessures"),
                html.P(
                    "Cette visualisation établit le nombre de blessures en fonction de leur gravité selon s'il y a présence ou absence d'une intersection.",
                    className='general-text',
                    style={
                        'marginTop': '1rem',
                    }
                ),
                html.Div(
                    id='pie-bar2-section',
                    className='chart-container',
                    children=[
                        dcc.Graph(
                            id='pie-bar2-chart',
                            className='graph',
                            figure=plot_intersection_vs_injury(dataframe),
                            config=dict(
                                displayModeBar=True,
                                displaylogo=False,
                                scrollZoom=False,
                                showTips=False,
                                showAxisDragHandles=False,
                                doubleClick='reset',
                                modeBarButtonsToRemove=[
                                    'select2d', 'lasso2d', 'pan2d', 'zoomIn2d', 'zoomOut2d',
                                    'autoScale2d', 'resetScale2d', 'hoverClosestCartesian',
                                    'hoverCompareCartesian', 'toggleSpikelines', 'toImage'
                                ],
                                modeBarButtonsToKeep=['zoom2d']
                            )
                        ),
                        html.P(
                            "Une attention particulière devrait être portée sur les blessures mortelles et incapacitantes en cas d'intersection et de chaussée sèche.",
                            className='under-chart-text',
                            style={
                                'marginTop': '1rem',
                            }
                        ),
                    ],
                    style={'scrollMarginTop': '100px',}
                ),
                # Footer
                html.Div(
                    className="footer",
                    children=[
                        html.Div(
                            className="footer-text",
                            children=[
                                html.P(
                                    children=[
                                        html.Small("Toutes les données sont fournies à titre indicatif et doivent être utilisées avec discernement."),
                                        html.Strong("Statistiques Canada - Statistic Canada"),
                                        html.Br(),
                                    ]
                                ),
                            ]
                        ),
                        html.Img(
                            src='/assets/canada-logo.png',
                            style={'height': '40px', 'marginTop': '1rem'}
                        ),
                    ]
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