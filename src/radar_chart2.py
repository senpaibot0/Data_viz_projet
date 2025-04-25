import pandas as pd
import plotly.graph_objects as go
from dash import dcc

INJURY_TRANSLATIONS = {
    "injuries_no_indication": "Aucune blessure",
    "injuries_non_incapacitating": "Non incapacitante",
    "injuries_reported_not_evident": "Déclarée, non visible",
    "injuries_incapacitating": "Incapacitante",
    "injuries_fatal": "Mortelle"
}

INJURY_COLORS = {
    "injuries_no_indication": "#1f77b4",
    "injuries_non_incapacitating": "#2ca02c",
    "injuries_reported_not_evident": "#ff7f0e",
    "injuries_incapacitating": "#d62728",
    "injuries_fatal": "#8B0000"
}

LIGHTING_TRANSLATIONS = {
    "DAYLIGHT": "Plein jour",
    "DARKNESS, LIGHTED ROAD": "Nuit, route éclairée",
    "DARKNESS": "Nuit, route sombre",
    "DUSK": "Crépuscule",
}

WEATHER_TRANSLATIONS = {
    "CLEAR": "Dégagé",
    "RAIN": "Pluie",
    "CLOUDY/OVERCAST": "Nuageux",
    "SNOW": "Neige",
}

LIGHTING_CONDITIONS = [
    "DAYLIGHT", 
    "DARKNESS, LIGHTED ROAD", 
    "DARKNESS", 
    "DUSK", 
]

WEATHER_CONDITIONS = [
    "CLEAR", 
    "RAIN", 
    "CLOUDY/OVERCAST", 
    "SNOW", 
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
    df = df.copy()
    df['lighting_condition'] = df['lighting_condition'].str.strip().str.upper()
    df['weather_condition'] = df['weather_condition'].str.strip().str.upper()

    charts = []

    lighting_totals = df.groupby('lighting_condition').sum(numeric_only=True)
    lighting_totals = lighting_totals.loc[[c for c in LIGHTING_CONDITIONS if c in lighting_totals.index]]
    total_values = lighting_totals.sum(axis=1).tolist()
    total_values.append(total_values[0])
    translated_labels = [LIGHTING_TRANSLATIONS[c] for c in lighting_totals.index]
    translated_labels.append(translated_labels[0])

    fig_total = go.Figure()
    max_val = 0

    for injury_col, injury_label in INJURY_TRANSLATIONS.items():
        if injury_col not in df.columns:
            continue

        group = df.groupby('lighting_condition')[injury_col].sum().reindex(LIGHTING_CONDITIONS, fill_value=0)
        values = group.tolist()
        values.append(values[0])
        translated_labels = [LIGHTING_TRANSLATIONS.get(c, c) for c in LIGHTING_CONDITIONS]
        translated_labels.append(translated_labels[0])

        fig_total.add_trace(
            go.Scatterpolar(
                r=values,
                theta=translated_labels,
                name=injury_label,
                hovertemplate="<b>%{theta}</b><br>Blessure : " + injury_label + "<br>%{r} accidents<extra></extra>",
                hoverlabel=dict(
                    font=dict(color='white', family="Lato, sans-serif"),
                    bgcolor=INJURY_COLORS[injury_col],
                    bordercolor='white'
                ),
                line=dict(color=INJURY_COLORS.get(injury_col)),
            ),
        )

        max_val = max(max_val, max(values[:-1]))

    fig_total.update_layout(
        title="Total des accidents par type d’éclairage et de blessure",
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max_val * 1.1])
        ),
        showlegend=True,
        margin=dict(l=50, r=50, t=70, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Lato, sans-serif", 
            size=12, 
            color="#031732",
        ),
    )

    charts.append(
        dcc.Graph(
            figure=fig_total,
            config={
                'displayModeBar': True,
                'modeBarButtonsToRemove': [
                    'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d',
                    'autoScale2d', 'resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian',
                    'toggleSpikelines', 'toImage', 'sendDataToCloud'
                ],
                'modeBarButtonsToShow': [['zoom2d']],
                'displaylogo': False
            },
            style={'height': '20rem', 'width': '65%'}
        )
    )

    for i, lighting_condition in enumerate(LIGHTING_CONDITIONS):
        fig = go.Figure()
        df_light = df[df['lighting_condition'] == lighting_condition]

        max_val = 0

        for injury_col, injury_label in INJURY_TRANSLATIONS.items():
            if injury_col not in df_light.columns:
                continue
            group = df_light.groupby('weather_condition')[injury_col].sum().reindex(WEATHER_CONDITIONS, fill_value=0)
            values = group.tolist()
            values.append(values[0])
            translated_weather = [WEATHER_TRANSLATIONS[c] for c in WEATHER_CONDITIONS]
            translated_weather.append(translated_weather[0])

            fig.add_trace(
                go.Scatterpolar(
                    r=values,
                    theta=translated_weather,
                    name=injury_label,
                    hovertemplate="<b>%{theta}</b><br>Blessure : " + injury_label + "<br>%{r} accidents<extra></extra>",
                    hoverlabel=dict(
                        font=dict(color='white', family="Lato, sans-serif"),
                        bgcolor=INJURY_COLORS[injury_col],
                        bordercolor='white'
                    ),
                    line=dict(color=INJURY_COLORS.get(injury_col))
                ),
            ),

            max_val = max(max_val, max(values[:-1]))

        fig.update_layout(
            title=LIGHTING_TRANSLATIONS.get(lighting_condition, lighting_condition),
            polar=dict(radialaxis=dict(visible=True, range=[0, max_val * 1.1])),
            showlegend=False,
            margin=dict(l=50, r=50, t=70, b=30),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(
                family="Lato, sans-serif", 
                size=12, 
                color="#031732",
            ),
        )
        charts.append(dcc.Graph(
            figure=fig, 
            config={
                'displayModeBar': True,
                'modeBarButtonsToRemove': [
                    'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d',
                    'autoScale2d', 'resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian',
                    'toggleSpikelines', 'toImage', 'sendDataToCloud'
                ],
                'modeBarButtonsToShow': [['zoom2d']],
                'displaylogo': False
            },
            style={'height': '20rem', 'width': '40%'}
        ))

    return charts