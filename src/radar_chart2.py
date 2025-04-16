import pandas as pd
import plotly.graph_objects as go
from dash import dcc


LIGHTING_TRANSLATIONS = {
    "DAYLIGHT": "Plein jour",
    "DARKNESS, LIGHTED ROAD": "Nuit, route éclairée",
    "DARKNESS": "Nuit, route sombre",
    "DUSK": "Crépuscule",
    "UNKNOWN": "Inconnu"
}

WEATHER_TRANSLATIONS = {
    "CLEAR": "Dégagé",
    "RAIN": "Pluie",
    "CLOUDY/OVERCAST": "Nuageux",
    "SNOW": "Neige",
    "UNKNOWN": "Inconnu"
}

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

    for lighting_condition in radar_data.index:
        values = radar_data.loc[lighting_condition].tolist()
        values.append(values[0])  # Ferme le cercle

        # Traduction des catégories météo
        categories = radar_data.columns.tolist()
        translated_categories = [WEATHER_TRANSLATIONS[c] for c in categories]
        translated_categories.append(translated_categories[0])  # Fermer le cercle aussi ici

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=translated_categories,
            fill='toself',
            name=LIGHTING_TRANSLATIONS.get(lighting_condition, lighting_condition),
            hoverinfo='text',
            text=[
                f"{cat}: {val}" for cat, val in zip(translated_categories, values)
            ]
        ))

        max_value = max(values[:-1])
        fig.update_layout(
            title=LIGHTING_TRANSLATIONS.get(lighting_condition, lighting_condition),
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max_value * 1.1]
                )
            ),
            showlegend=False,
            margin=dict(l=50, r=50, t=50, b=30)
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
                    'height': '20rem',
                    'width': '30%',
                })
        )

    return charts