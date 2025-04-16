import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_day_type_histogram(df):
    df['crash_date'] = pd.to_datetime(df['crash_date'])
    df['month'] = df['crash_date'].dt.month
    df['day'] = df['crash_date'].dt.day
    df['day_of_week'] = df['crash_date'].dt.dayofweek + 1

    day_type_mapping = {1: 'Jour ordinaire', 2: 'Jour ordinaire', 3: 'Jour ordinaire',
                        4: 'Jour ordinaire', 5: 'Jour ordinaire', 6: 'Fin de semaine', 7: 'Fin de semaine'}
    df['jour_type'] = df['day_of_week'].map(day_type_mapping)
    df.loc[((df['month'] == 12) & (df['day'] == 25)) | ((df['month'] == 1) & (df['day'] == 1)), 'jour_type'] = 'Jour férié'

    min_date = df['crash_date'].min()
    max_date = df['crash_date'].max()
    date_range = pd.date_range(start=min_date, end=max_date)
    date_df = pd.DataFrame({'date': date_range})
    date_df['month'] = date_df['date'].dt.month
    date_df['day'] = date_df['date'].dt.day
    date_df['day_of_week'] = date_df['date'].dt.dayofweek + 1

    date_df['type'] = 'Jour ordinaire'
    date_df.loc[date_df['day_of_week'].isin([6, 7]), 'type'] = 'Fin de semaine'
    date_df.loc[((date_df['month'] == 12) & (date_df['day'] == 25)) | 
                ((date_df['month'] == 1) & (date_df['day'] == 1)), 'type'] = 'Jour férié'

    days_count = date_df['type'].value_counts()
    accidents_by_type = df['jour_type'].value_counts()

    normalized_data = {}
    for day_type in accidents_by_type.index:
        if day_type in days_count:
            normalized_data[day_type] = accidents_by_type[day_type] / days_count[day_type]
        else:
            normalized_data[day_type] = 0

    fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'bar'}]], subplot_titles=[""])

    trace = go.Bar(
        x=list(normalized_data.keys()),
        y=list(normalized_data.values()),
        marker_color='rgba(50, 171, 96, 0.7)',
        text=[f"{v:.2f}" for v in normalized_data.values()],
        textposition='auto'
    )

    fig.add_trace(trace, row=1, col=1)
    fig.update_xaxes(title_text="Type de jour")
    fig.update_yaxes(title_text="Moyenne d'accidents par jour")

    fig.update_layout(
        title="",
        height=500,
        width=800,
        showlegend=False,
        margin=dict(l=50, r=50, t=100, b=50)
    )

    return fig