import pandas as pd
import plotly.graph_objects as go
from dash import dcc

LIGHTING_CONDITIONS = [
    "DAYLIGHT", 
    "DARKNESS, LIGHTED ROAD", 
    "DARKNESS", 
    "DUSK", 
    "UNKNOWN"
]

WEATHER_CONDITIONS = [
    "CLEAR", 
    "RAIN", 
    "CLOUDY/OVERCAST", 
    "SNOW", 
    "UNKNOWN"
]

def prepare_radar_data(df):
    df = df.copy()
    df['lighting_condition'] = df['lighting_condition'].str.strip().str.upper()
    df['weather_condition'] = df['weather_condition'].str.strip().str.upper()

    lighting_conditions_upper = [c.upper() for c in LIGHTING_CONDITIONS]
    weather_conditions_upper = [c.upper() for c in WEATHER_CONDITIONS]

    df = df[df['lighting_condition'].isin(lighting_conditions_upper)]
    df = df[df['weather_condition'].isin(weather_conditions_upper)]

    radar_data = df.groupby(['lighting_condition', 'weather_condition']).size().unstack(fill_value=0)

    for condition in weather_conditions_upper:
        if condition not in radar_data.columns:
            radar_data[condition] = 0

    radar_data = radar_data[weather_conditions_upper]
    return radar_data

def create_radar_charts(df):
    radar_data = prepare_radar_data(df)
    charts = []

    # total = 0
        
    for lighting_condition in radar_data.index:
        values = radar_data.loc[lighting_condition].tolist()
        values.append(values[0])  # Ferme le cercle
        categories = radar_data.columns.tolist()
        categories.append(categories[0])

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=lighting_condition,
            hoverinfo='text',
            text=[f"{cat}: {val}" for cat, val in zip(categories, values)]
        ))

        max_value = max(values[:-1])  # Exclude the repeated first value
        fig.update_layout(
            title=f"{lighting_condition.title()}",
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max_value * 1.1]  # Dynamic per chart
                )
            ),
            showlegend=False,
            margin=dict(l=30, r=30, t=50, b=30)
        )

        charts.append(
            dcc.Graph(
                figure=fig,
                config=dict(
                    scrollZoom=False,
                    displayModeBar=True,
                    displaylogo=False
                ),
                style={
                    'height': 'auto',
                    'width': '30%',
                })
        )

    return charts
