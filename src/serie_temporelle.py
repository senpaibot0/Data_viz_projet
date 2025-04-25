import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

day_names_full = {1: 'Lundi', 2: 'Mardi', 3: 'Mercredi', 4: 'Jeudi', 5: 'Vendredi', 6: 'Samedi', 7: 'Dimanche'}
month_names_full = {1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril', 5: 'Mai', 6: 'Juin',
                    7: 'Juillet', 8: 'Août', 9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'}

line_colors = {
    'Par heure': '#1f77b4',
    'Par jour': '#2ca02c',
    'Par mois': '#ff7f0e',
    'Par année': '#d62728',
}

def create_temporal_series(df):
    df['crash_date'] = pd.to_datetime(df['crash_date'])
    df['year'] = df['crash_date'].dt.year
    df['month'] = df['crash_date'].dt.month
    df['day'] = df['crash_date'].dt.day
    df['hour'] = df['crash_date'].dt.hour
    df['day_of_week'] = df['crash_date'].dt.dayofweek + 1

    day_names = {1: 'Lun', 2: 'Mar', 3: 'Mer', 4: 'Jeu', 5: 'Ven', 6: 'Sam', 7: 'Dim'}
    df['day_name'] = df['day_of_week'].map(day_names)
    month_names = {1: 'Jan', 2: 'Fév', 3: 'Mar', 4: 'Avr', 5: 'Mai', 6: 'Juin',
                   7: 'Juil', 8: 'Août', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Déc'}
    df['month_name'] = df['month'].map(month_names)

    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{'type': 'scatter'}, {'type': 'scatter'}],
               [{'type': 'scatter'}, {'type': 'scatter'}]],
        subplot_titles=('Par heure', 'Par jour de semaine', 'Par mois', 'Par année'),
        vertical_spacing=0.2,
        horizontal_spacing=0.08
    )

    hour_counts = df.groupby('hour').size()
    fig.add_trace(
        go.Scatter(
            x=hour_counts.index, 
            y=hour_counts.values, 
            mode='lines+markers', 
            name='Par heure', 
            line=dict(width=2, color=line_colors['Par heure']),
            hovertemplate='<b>%{x}h</b><br>%{y} accidents<extra></extra>',
            hoverlabel=dict(bgcolor=line_colors['Par heure'], font=dict(color='white', family="Lato, sans-serif")),
        ), 
        row=1, col=1,
    )
    fig.update_xaxes(title_text="Heure", row=1, col=1)
    fig.update_yaxes(title_text="Nombre d'accidents", row=1, col=1)

    day_counts = df['day_of_week'].value_counts().sort_index()
    days_short = [day_names[d] for d in day_counts.index]
    days_full = [day_names_full[d] for d in day_counts.index]

    day_counts = df['day_of_week'].value_counts().sort_index()
    fig.add_trace(
        go.Scatter(
            x=[day_names[d] for d in day_counts.index], 
            y=day_counts.values, 
            mode='lines+markers', 
            name='Par jour', 
            line=dict(width=2, color=line_colors['Par jour']),
            customdata=[[d] for d in days_full],
            hovertemplate='<b>%{customdata[0]}</b><br>%{y} accidents<extra></extra>',
            hoverlabel=dict(bgcolor=line_colors['Par jour'], font=dict(color='white', family="Lato, sans-serif")),
        ), 
        row=1, col=2,
    ),
    fig.update_xaxes(title_text="Jour de la semaine", row=1, col=2)
    fig.update_yaxes(title_text="Nombre d'accidents", row=1, col=2)

    month_counts = df['month'].value_counts().sort_index()
    months_full = [month_names_full[m] for m in month_counts.index]

    month_counts = df['month'].value_counts().sort_index()
    fig.add_trace(
        go.Scatter(
            x=[month_names[m] for m in month_counts.index], 
            y=month_counts.values, 
            mode='lines+markers', 
            name='Par mois', 
            line=dict(width=2, color=line_colors['Par mois']),
            customdata=[[m] for m in months_full],
            hovertemplate='<b>%{customdata[0]}</b><br>%{y} accidents<extra></extra>',
            hoverlabel=dict(bgcolor=line_colors['Par mois'], font=dict(color='white', family="Lato, sans-serif")),
        ), row=2, col=1,
    ),
    fig.update_xaxes(title_text="Mois", row=2, col=1)
    fig.update_yaxes(title_text="Nombre d'accidents", row=2, col=1)

    year_counts = df['year'].value_counts().sort_index()
    fig.add_trace(
        go.Scatter(
            x=year_counts.index, 
            y=year_counts.values, 
            mode='lines+markers', 
            name='Par année', 
            line=dict(width=2, color=line_colors['Par année']),
            hovertemplate='<b>%{x}</b><br>%{y} accidents<extra></extra>',
            hoverlabel=dict(bgcolor=line_colors['Par année'], font=dict(color='white', family="Lato, sans-serif")),
        ), row=2, col=2,
    ),
    fig.update_xaxes(title_text="Année", row=2, col=2)
    fig.update_yaxes(title_text="Nombre d'accidents", row=2, col=2)

    fig.update_layout(
        title="",
        height=600,
        width=900,
        showlegend=False,
        margin=dict(l=50, r=50, t=30, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hoverlabel=dict(
            font=dict(color='white', family="Lato, sans-serif"),
            bordercolor='white',
        ),
        font=dict(
            family="Lato, serif",
            size=12,
            color="#031732",
        ),
    )

    return fig