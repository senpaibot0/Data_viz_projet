# import pandas as pd
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

# def create_temporal_series(df):
#     df['crash_date'] = pd.to_datetime(df['crash_date'])
#     df['year'] = df['crash_date'].dt.year
#     df['month'] = df['crash_date'].dt.month
#     df['day'] = df['crash_date'].dt.day
#     df['hour'] = df['crash_date'].dt.hour
#     df['day_of_week'] = df['crash_date'].dt.dayofweek + 1

#     day_names = {1: 'Lun', 2: 'Mar', 3: 'Mer', 4: 'Jeu', 5: 'Ven', 6: 'Sam', 7: 'Dim'}
#     df['day_name'] = df['day_of_week'].map(day_names)
#     month_names = {1: 'Jan', 2: 'Fév', 3: 'Mar', 4: 'Avr', 5: 'Mai', 6: 'Juin',
#                    7: 'Juil', 8: 'Août', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Déc'}
#     df['month_name'] = df['month'].map(month_names)

#     fig = make_subplots(
#         rows=2, cols=2,
#         specs=[[{'type': 'scatter'}, {'type': 'scatter'}],
#                [{'type': 'scatter'}, {'type': 'scatter'}]],
#         subplot_titles=('Par heure', 'Par jour de semaine', 'Par mois', 'Par année'),
#         vertical_spacing=0.2,
#         horizontal_spacing=0.08
#     )

#     hour_counts = df.groupby('hour').size()
#     fig.add_trace(go.Scatter(x=hour_counts.index, y=hour_counts.values, mode='lines+markers', name='Par heure', line=dict(width=2)), row=1, col=1)

#     day_counts = df['day_of_week'].value_counts().sort_index()
#     fig.add_trace(go.Scatter(x=[day_names[d] for d in day_counts.index], y=day_counts.values, mode='lines+markers', name='Par jour', line=dict(width=2)), row=1, col=2)

#     month_counts = df['month'].value_counts().sort_index()
#     fig.add_trace(go.Scatter(x=[month_names[m] for m in month_counts.index], y=month_counts.values, mode='lines+markers', name='Par mois', line=dict(width=2)), row=2, col=1)

#     year_counts = df['year'].value_counts().sort_index()
#     fig.add_trace(go.Scatter(x=year_counts.index, y=year_counts.values, mode='lines+markers', name='Par année', line=dict(width=2)), row=2, col=2)

#     fig.update_layout(
#         title="",
#         height=700,
#         width=1000,
#         showlegend=False,
#         margin=dict(l=50, r=50, t=100, b=50)
#     )

#     fig.update_xaxes(title_text="Heure", row=1, col=1)
#     fig.update_yaxes(title_text="Nombre d'accidents", row=1, col=1)
#     fig.update_xaxes(title_text="Jour de la semaine", row=1, col=2)
#     fig.update_yaxes(title_text="Nombre d'accidents", row=1, col=2)
#     fig.update_xaxes(title_text="Mois", row=2, col=1)
#     fig.update_yaxes(title_text="Nombre d'accidents", row=2, col=1)
#     fig.update_xaxes(title_text="Année", row=2, col=2)
#     fig.update_yaxes(title_text="Nombre d'accidents", row=2, col=2)

#     return fig
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_temporal_series(df):
    # Ensure crash_date is in datetime format
    df['crash_date'] = pd.to_datetime(df['crash_date'])
    
    # Extract temporal components
    df['year'] = df['crash_date'].dt.year
    df['month'] = df['crash_date'].dt.month
    df['day'] = df['crash_date'].dt.day
    df['hour'] = df['crash_date'].dt.hour
    df['day_of_week'] = df['crash_date'].dt.dayofweek + 1

    # Map day and month names
    day_names = {1: 'Lun', 2: 'Mar', 3: 'Mer', 4: 'Jeu', 5: 'Ven', 6: 'Sam', 7: 'Dim'}
    df['day_name'] = df['day_of_week'].map(day_names)
    month_names = {1: 'Jan', 2: 'Fév', 3: 'Mar', 4: 'Avr', 5: 'Mai', 6: 'Juin',
                   7: 'Juil', 8: 'Août', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Déc'}
    df['month_name'] = df['month'].map(month_names)

    # Get available years
    available_years = sorted(df['year'].unique())

    # Create subplot figure
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{'type': 'scatter'}, {'type': 'scatter'}],
               [{'type': 'scatter'}, {'type': 'scatter'}]],
        subplot_titles=('Par heure', 'Par jour de semaine', 'Par mois', 'Par année'),
        vertical_spacing=0.12,
        horizontal_spacing=0.08
    )

    # Create traces for each year for the first three subplots
    buttons = []
    for i, year in enumerate(available_years):
        year_data = df[df['year'] == year]
        visible = (i == 0)  # Only the first year is visible initially

        # 1. Par heure
        hour_counts = year_data.groupby('hour').size()
        fig.add_trace(
            go.Scatter(
                x=list(range(24)),
                y=[hour_counts.get(hour, 0) for hour in range(24)],
                mode='lines+markers',
                name=f'Par heure ({year})',
                line=dict(width=2, color='blue'),
                visible=visible
            ),
            row=1, col=1
        )

        # 2. Par jour de la semaine
        day_counts = year_data['day_of_week'].value_counts().sort_index()
        days = list(day_names.keys())
        fig.add_trace(
            go.Scatter(
                x=[day_names[d] for d in days],
                y=[day_counts.get(d, 0) for d in days],
                mode='lines+markers',
                name=f'Par jour ({year})',
                line=dict(width=2, color='red'),
                visible=visible
            ),
            row=1, col=2
        )

        # 3. Par mois
        month_counts = year_data['month'].value_counts().sort_index()
        months = list(month_names.keys())
        fig.add_trace(
            go.Scatter(
                x=[month_names[m] for m in months],
                y=[month_counts.get(m, 0) for m in months],
                mode='lines+markers',
                name=f'Par mois ({year})',
                line=dict(width=2, color='green'),
                visible=visible
            ),
            row=2, col=1
        )

        # Create button for year selection
        visibility = [False] * len(available_years) * 3
        visibility[i*3:(i+1)*3] = [True, True, True]
        buttons.append(dict(
            method='update',
            args=[{'visible': visibility + [True]},
                  {'title': f'Séries temporelles des accidents de la route - {year}'}],
            label=str(year)
        ))

    # 4. Par année - always visible
    year_counts = df['year'].value_counts().sort_index()
    fig.add_trace(
        go.Scatter(
            x=year_counts.index,
            y=year_counts.values,
            mode='lines+markers',
            name='Par année',
            line=dict(width=2, color='purple'),
            visible=True
        ),
        row=2, col=2
    )

    # Update layout
    fig.update_layout(
        title=f"Séries temporelles des accidents de la route - {available_years[0]}",
        height=800,
        width=1400,
        showlegend=False,
        margin=dict(l=50, r=50, t=100, b=50),
        updatemenus=[dict(
            buttons=buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.85,
            xanchor="right",
            y=1.15,
            yanchor="top"
        )]
    )

    # Add annotation for year selector
    fig.add_annotation(
        x=0.78,
        y=1.12,
        xref="paper",
        yref="paper",
        text="Année:",
        showarrow=False,
        font=dict(size=12),
        align="right"
    )

    # Update axes
    fig.update_xaxes(title_text="Heure", row=1, col=1)
    fig.update_yaxes(title_text="Nombre d'accidents", row=1, col=1)
    fig.update_xaxes(title_text="Jour de la semaine", row=1, col=2)
    fig.update_yaxes(title_text="Nombre d'accidents", row=1, col=2)
    fig.update_xaxes(title_text="Mois", row=2, col=1)
    fig.update_yaxes(title_text="Nombre d'accidents", row=2, col=1)
    fig.update_xaxes(title_text="Année", row=2, col=2)
    fig.update_yaxes(title_text="Nombre d'accidents", row=2, col=2)

    return fig