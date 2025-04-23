# import pandas as pd
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

# def create_day_type_histogram(df):
#     df['crash_date'] = pd.to_datetime(df['crash_date'])
#     df['month'] = df['crash_date'].dt.month
#     df['day'] = df['crash_date'].dt.day
#     df['day_of_week'] = df['crash_date'].dt.dayofweek + 1

#     day_type_mapping = {1: 'Jour ordinaire', 2: 'Jour ordinaire', 3: 'Jour ordinaire',
#                         4: 'Jour ordinaire', 5: 'Jour ordinaire', 6: 'Fin de semaine', 7: 'Fin de semaine'}
#     df['jour_type'] = df['day_of_week'].map(day_type_mapping)
#     df.loc[((df['month'] == 12) & (df['day'] == 25)) | ((df['month'] == 1) & (df['day'] == 1)), 'jour_type'] = 'Jour férié'

#     min_date = df['crash_date'].min()
#     max_date = df['crash_date'].max()
#     date_range = pd.date_range(start=min_date, end=max_date)
#     date_df = pd.DataFrame({'date': date_range})
#     date_df['month'] = date_df['date'].dt.month
#     date_df['day'] = date_df['date'].dt.day
#     date_df['day_of_week'] = date_df['date'].dt.dayofweek + 1

#     date_df['type'] = 'Jour ordinaire'
#     date_df.loc[date_df['day_of_week'].isin([6, 7]), 'type'] = 'Fin de semaine'
#     date_df.loc[((date_df['month'] == 12) & (date_df['day'] == 25)) | 
#                 ((date_df['month'] == 1) & (date_df['day'] == 1)), 'type'] = 'Jour férié'

#     days_count = date_df['type'].value_counts()
#     accidents_by_type = df['jour_type'].value_counts()

#     normalized_data = {}
#     for day_type in accidents_by_type.index:
#         if day_type in days_count:
#             normalized_data[day_type] = accidents_by_type[day_type] / days_count[day_type]
#         else:
#             normalized_data[day_type] = 0

#     fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'bar'}]], subplot_titles=[""])

#     trace = go.Bar(
#         x=list(normalized_data.keys()),
#         y=list(normalized_data.values()),
#         marker_color='rgba(50, 171, 96, 0.7)',
#         text=[f"{v:.2f}" for v in normalized_data.values()],
#         textposition='auto'
#     )

#     fig.add_trace(trace, row=1, col=1)
#     fig.update_xaxes(title_text="Type de jour")
#     fig.update_yaxes(title_text="Moyenne d'accidents par jour")

#     fig.update_layout(
#         title="",
#         height=500,
#         width=800,
#         showlegend=False,
#         margin=dict(l=50, r=50, t=100, b=50)
#     )

#     return fig
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import uuid

def create_day_type_histogram(df):
    # Preprocessing
    df['crash_date'] = pd.to_datetime(df['crash_date'])
    df['month'] = df['crash_date'].dt.month
    df['day'] = df['crash_date'].dt.day
    df['day_of_week'] = df['crash_date'].dt.dayofweek + 1  # 1=Monday
    df['year'] = df['crash_date'].dt.year

    # Day type mapping
    day_type_mapping = {
        1: 'Jour ordinaire',
        2: 'Jour ordinaire',
        3: 'Jour ordinaire',
        4: 'Jour ordinaire',
        5: 'Jour ordinaire',
        6: 'Fin de semaine',
        7: 'Fin de semaine',
    }
    df['jour_type'] = df['day_of_week'].map(day_type_mapping)
    df.loc[((df['month'] == 12) & (df['day'] == 25)) |
           ((df['month'] == 1) & (df['day'] == 1)), 'jour_type'] = 'Jour férié'

    # Get available years
    available_years = sorted(df['year'].unique())

    # Function to create normalized data
    def get_normalized_data(year=None):
        # Filter by year if specified
        year_df = df[df['year'] == year] if year is not None else df
        
        # Set date range
        start_date = pd.Timestamp(year=year, month=1, day=1) if year else df['crash_date'].min()
        end_date = pd.Timestamp(year=year, month=12, day=31) if year else df['crash_date'].max()
        
        # Create reference date range
        date_range = pd.date_range(start=start_date, end=end_date)
        date_df = pd.DataFrame({'date': date_range})
        date_df['month'] = date_df['date'].dt.month
        date_df['day'] = date_df['date'].dt.day
        date_df['day_of_week'] = date_df['date'].dt.dayofweek + 1
        
        # Classify day types
        date_df['type'] = 'Jour ordinaire'
        date_df.loc[date_df['day_of_week'].isin([6, 7]), 'type'] = 'Fin de semaine'
        date_df.loc[((date_df['month'] == 12) & (date_df['day'] == 25)) |
                    ((date_df['month'] == 1) & (date_df['day'] == 1)), 'type'] = 'Jour férié'
        
        # Count days and accidents
        days_count = date_df['type'].value_counts()
        accidents_by_type = year_df['jour_type'].value_counts()
        
        # Normalize data
        normalized_data = {}
        for day_type in ['Jour ordinaire', 'Fin de semaine', 'Jour férié']:
            normalized_data[day_type] = (accidents_by_type[day_type] / days_count[day_type]
                                       if day_type in accidents_by_type.index and day_type in days_count
                                       else 0)
        return normalized_data

    # Colors for day types
    colors = {
        'Jour ordinaire': '#3498db',
        'Fin de semaine': '#e74c3c',
        'Jour férié': '#2ecc71'
    }

    # Create figure
    fig = go.Figure()

    # Add traces for all years and individual years
    for year in ['Toutes les années'] + available_years:
        data = get_normalized_data() if year == 'Toutes les années' else get_normalized_data(year)
        visible = year == 'Toutes les années'
        
        # Calculate global average
        moyenne_globale = sum(data.values()) / len(data) if data else 0
        
        # Add bar trace
        fig.add_trace(
            go.Bar(
                x=list(data.keys()),
                y=list(data.values()),
                name=str(year),
                marker=dict(
                    color=[colors[day_type] for day_type in data.keys()],
                    line=dict(width=1.5, color='rgba(0,0,0,0.3)')
                ),
                text=[f"{v:.2f}" for v in data.values()],
                textposition='auto',
                width=0.6,
                opacity=0.85,
                visible=visible
            )
        )
        
        # Add average line
        fig.add_shape(
            type="line",
            x0=-0.5, y0=moyenne_globale, x1=len(data)-0.5, y1=moyenne_globale,
            line=dict(color="black", width=1.5, dash="dash"),
            visible=visible
        )
        
        # Add average annotation
        fig.add_annotation(
            x=len(data)-0.5,
            y=moyenne_globale,
            xref="x",
            yref="y",
            text="Moyenne globale",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1.5,
            ax=50,
            ay=-20,
            visible=visible
        )

    # Create dropdown buttons
    buttons = []
    for i, year in enumerate(['Toutes les années'] + available_years):
        visible_array = [False] * len(fig.data)
        visible_array[i] = True
        
        buttons.append(
            dict(
                method="update",
                label=str(year),
                args=[
                    {"visible": visible_array},
                    {
                        f"shapes[{i}].visible": True,
                        f"annotations[{i}].visible": True
                    }
                ]
            )
        )

    # Update layout
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.8,
                xanchor="left",
                y=1.15,
                yanchor="top",
                font=dict(size=12)
            )
        ],
        annotations=[
            dict(
                text="Année:",
                x=0.78,
                y=1.12,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=14)
            )
        ],
        title={
            'text': "Histogramme normalisé des accidents selon le type de jour",
            'font': {'size': 20, 'family': 'Arial', 'color': '#333'},
            'y': 0.95
        },
        height=700,
        width=800,
        paper_bgcolor='rgba(240,240,240,0.2)',
        plot_bgcolor='rgba(240,240,240,0.2)',
        showlegend=False,
        margin=dict(l=50, r=50, t=120, b=70),
        bargap=0.15,
        font=dict(family="Arial", size=14)
    )

    # Update axes
    fig.update_xaxes(
        title_text="Type de jour",
        title_font=dict(size=16),
        tickfont=dict(size=14)
    )
    fig.update_yaxes(
        title_text="Moyenne d'accidents par jour",
        title_font=dict(size=16),
        tickfont=dict(size=14),
        gridcolor='rgba(200,200,200,0.4)'
    )

    return fig