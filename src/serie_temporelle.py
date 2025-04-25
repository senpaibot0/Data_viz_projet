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

    available_years = sorted(df['year'].unique())

    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{'type': 'scatter'}, {'type': 'scatter'}],
               [{'type': 'scatter'}, {'type': 'scatter'}]],
        subplot_titles=('Par heure', 'Par jour de semaine', 'Par mois', 'Par année'),
        vertical_spacing=0.2,
        horizontal_spacing=0.08
    )

    buttons = []

    hour_counts_all = df.groupby('hour').size()
    fig.add_trace(
        go.Scatter(
            x=list(range(24)),
            y=[hour_counts_all.get(hour, 0) for hour in range(24)],
            mode='lines+markers',
            name='Par heure (toutes années)',
            line=dict(width=2, color=line_colors['Par heure']),
            hovertemplate='<b>%{x}h</b><br>%{y} accidents<extra></extra>',
            hoverlabel=dict(bgcolor=line_colors['Par heure'], font=dict(color='white', family="Lato, sans-serif")),
            visible=True
        ),
        row=1, col=1
    )

    day_counts_all = df['day_of_week'].value_counts().sort_index()
    fig.add_trace(
        go.Scatter(
            x=[day_names[d] for d in day_names.keys()],
            y=[day_counts_all.get(d, 0) for d in day_names.keys()],
            mode='lines+markers',
            name='Par jour (toutes années)',
            line=dict(width=2, color=line_colors['Par jour']),
            customdata=[[day_names_full[d]] for d in day_names.keys()],
            hovertemplate='<b>%{customdata[0]}</b><br>%{y} accidents<extra></extra>',
            hoverlabel=dict(bgcolor=line_colors['Par jour'], font=dict(color='white', family="Lato, sans-serif")),
            visible=True
        ),
        row=1, col=2
    )

    month_counts_all = df['month'].value_counts().sort_index()
    fig.add_trace(
        go.Scatter(
            x=[month_names[m] for m in month_names.keys()],
            y=[month_counts_all.get(m, 0) for m in month_names.keys()],
            mode='lines+markers',
            name='Par mois (toutes années)',
            line=dict(width=2, color=line_colors['Par mois']),
            customdata=[[month_names_full[m]] for m in month_names.keys()],
            hovertemplate='<b>%{customdata[0]}</b><br>%{y} accidents<extra></extra>',
            hoverlabel=dict(bgcolor=line_colors['Par mois'], font=dict(color='white', family="Lato, sans-serif")),
            visible=True
        ),
        row=2, col=1
    )

    nb_years = len(available_years)
    visibility_all_years = [True, True, True] + [False] * (nb_years * 3) + [True]
    buttons.insert(0, dict(
        method='update',
        args=[
            {'visible': visibility_all_years},
            {'title': "Séries temporelles des accidents de la route - Toutes les années"}
        ],
        label="Toutes les années"
    ))

    for i, year in enumerate(available_years):
        year_data = df[df['year'] == year]
        visible = False

        hour_counts = year_data.groupby('hour').size()
        fig.add_trace(
            go.Scatter(
                x=list(range(24)),
                y=[hour_counts.get(hour, 0) for hour in range(24)],
                mode='lines+markers',
                name=f'Par heure ({year})',
                line=dict(width=2, color=line_colors['Par heure']),
                hovertemplate='<b>%{x}h</b><br>%{y} accidents<extra></extra>',
                hoverlabel=dict(bgcolor=line_colors['Par heure'], font=dict(color='white', family="Lato, sans-serif")),
                visible=visible
            ),
            row=1, col=1
        )

        day_counts = year_data['day_of_week'].value_counts().sort_index()
        days = list(day_names.keys())
        days_short = [day_names[d] for d in days]
        days_full = [day_names_full[d] for d in days]
        fig.add_trace(
            go.Scatter(
                x=days_short,
                y=[day_counts.get(d, 0) for d in days],
                mode='lines+markers',
                name=f'Par jour ({year})',
                line=dict(width=2, color=line_colors['Par jour']),
                customdata=[[d] for d in days_full],
                hovertemplate='<b>%{customdata[0]}</b><br>%{y} accidents<extra></extra>',
                hoverlabel=dict(bgcolor=line_colors['Par jour'], font=dict(color='white', family="Lato, sans-serif")),
                visible=visible
            ),
            row=1, col=2
        )

        month_counts = year_data['month'].value_counts().sort_index()
        months = list(month_names.keys())
        months_short = [month_names[m] for m in months]
        months_full = [month_names_full[m] for m in months]
        fig.add_trace(
            go.Scatter(
                x=months_short,
                y=[month_counts.get(m, 0) for m in months],
                mode='lines+markers',
                name=f'Par mois ({year})',
                line=dict(width=2, color=line_colors['Par mois']),
                customdata=[[m] for m in months_full],
                hovertemplate='<b>%{customdata[0]}</b><br>%{y} accidents<extra></extra>',
                hoverlabel=dict(bgcolor=line_colors['Par mois'], font=dict(color='white', family="Lato, sans-serif")),
                visible=visible
            ),
            row=2, col=1
        )

        visibility = [False, False, False] + [False] * (len(available_years) * 3)
        visibility[3 + i*3 : 3 + (i+1)*3] = [True, True, True]
        buttons.append(dict(
            method='update',
            args=[{'visible': visibility + [True]},
                  {'title': f'Séries temporelles des accidents de la route - {year}'}],
            label=str(year)
        ))

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
            visible=True
        ),
        row=2, col=2
    )

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
        updatemenus=[dict(
            buttons=buttons,
            direction="down",
            showactive=True,
            x=0.55,  
            xanchor="right",
            y=1.1,
            yanchor="top",
            bgcolor="white",
            bordercolor="lightgrey",
            borderwidth=1,
            font=dict(
                family="Lato, sans-serif",
            ),
        )]
    )


    fig.update_xaxes(title_text="Heure", row=1, col=1)
    fig.update_yaxes(title_text="Nombre d'accidents", row=1, col=1)
    fig.update_xaxes(title_text="Jour de la semaine", row=1, col=2)
    fig.update_yaxes(title_text="Nombre d'accidents", row=1, col=2)
    fig.update_xaxes(title_text="Mois", row=2, col=1)
    fig.update_yaxes(title_text="Nombre d'accidents", row=2, col=1)
    fig.update_xaxes(title_text="Année", row=2, col=2)
    fig.update_yaxes(title_text="Nombre d'accidents", row=2, col=2)

    return fig