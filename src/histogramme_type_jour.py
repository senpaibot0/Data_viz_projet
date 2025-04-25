def create_day_type_histogram(df):
    import pandas as pd
    import plotly.graph_objects as go

    df['crash_date'] = pd.to_datetime(df['crash_date'])
    df['month'] = df['crash_date'].dt.month
    df['day'] = df['crash_date'].dt.day
    df['day_of_week'] = df['crash_date'].dt.dayofweek + 1
    df['year'] = df['crash_date'].dt.year

    day_type_mapping = {1: 'Jour ordinaire', 2: 'Jour ordinaire', 3: 'Jour ordinaire',
                        4: 'Jour ordinaire', 5: 'Jour ordinaire', 6: 'Fin de semaine', 7: 'Fin de semaine'}
    df['jour_type'] = df['day_of_week'].map(day_type_mapping)
    df.loc[((df['month'] == 12) & (df['day'] == 25)) |
           ((df['month'] == 1) & (df['day'] == 1)), 'jour_type'] = 'Jour férié'

    available_years = sorted(df['year'].unique())

    def get_normalized_data(year=None):
        year_df = df[df['year'] == year] if year is not None else df
        start_date = pd.Timestamp(year=year, month=1, day=1) if year else df['crash_date'].min()
        end_date = pd.Timestamp(year=year, month=12, day=31) if year else df['crash_date'].max()

        date_range = pd.date_range(start=start_date, end=end_date)
        date_df = pd.DataFrame({'date': date_range})
        date_df['month'] = date_df['date'].dt.month
        date_df['day'] = date_df['date'].dt.day
        date_df['day_of_week'] = date_df['date'].dt.dayofweek + 1

        date_df['type'] = 'Jour ordinaire'
        date_df.loc[date_df['day_of_week'].isin([6, 7]), 'type'] = 'Fin de semaine'
        date_df.loc[((date_df['month'] == 12) & (date_df['day'] == 25)) |
                    ((date_df['month'] == 1) & (date_df['day'] == 1)), 'type'] = 'Jour férié'

        days_count = date_df['type'].value_counts()
        accidents_by_type = year_df['jour_type'].value_counts()

        normalized_data = {}
        for day_type in ['Jour ordinaire', 'Fin de semaine', 'Jour férié']:
            normalized_data[day_type] = (accidents_by_type[day_type] / days_count[day_type]
                                         if day_type in accidents_by_type.index and day_type in days_count else 0)
        return normalized_data

    colors = {
        'Jour ordinaire': '#1f77b4',
        'Fin de semaine': '#d62728',
        'Jour férié': '#2ca02c'
    }

    fig = go.Figure()

    for year in ['Toutes les années'] + available_years:
        data = get_normalized_data() if year == 'Toutes les années' else get_normalized_data(year)
        visible = year == 'Toutes les années'
        moyenne_globale = sum(data.values()) / len(data) if data else 0

        fig.add_trace(
            go.Bar(
                x=list(data.keys()),
                y=list(data.values()),
                name=str(year),
                marker=dict(
                    color=[colors[k] for k in data.keys()],
                    line=dict(width=0)
                ),
                text=[f"{v:.2f}" for v in data.values()],
                textposition='auto',
                textfont=dict(color='white'),
                width=0.6,
                opacity=1,
                visible=visible,
                hovertemplate='<b>%{x}</b><br>%{y:.2f} accidents<extra></extra>',
                hoverlabel=dict(
                    font=dict(color="white", family="Lato, sans-serif"),
                    bordercolor="white",
                    bgcolor=[colors[k] for k in data.keys()],
                )
            )
        )

        fig.add_shape(
            type="line",
            x0=-0.5, y0=moyenne_globale, x1=2.5, y1=moyenne_globale,
            line=dict(color="black", width=1.5, dash="dash"),
            visible=visible
        )

        fig.add_annotation(
            x=2.5, y=moyenne_globale,
            text="Moyenne globale",
            showarrow=True,
            arrowhead=2, ax=50, ay=-20,
            visible=visible
        )

    buttons = []
    for i, year in enumerate(['Toutes les années'] + available_years):
        vis = [False] * len(fig.data)
        vis[i] = True
        buttons.append(dict(method="update", label=str(year), args=[{"visible": vis}]))

    fig.update_layout(
        updatemenus=[dict(
            buttons=buttons,
            direction="down",
            showactive=True,
            active=0,
            x=0.45,
            xanchor="center",
            y=1.2,
            yanchor="top",
            bgcolor="white",
            bordercolor="lightgrey",
            borderwidth=1,
            font=dict(
                family="Lato, sans-serif",
            ),
        )],
        title_text="",
        height=350,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=20, t=20, b=80),
        font=dict(
            family="Lato, sans-serif", 
            size=12, 
            color="#031732",
        ),
    )

    fig.update_xaxes(title_text="Type de jour", title_font=dict(size=14))
    fig.update_yaxes(title_text="Nombre moyen d'accidents", title_font=dict(size=14))

    return fig
