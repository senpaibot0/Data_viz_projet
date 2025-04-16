import plotly.express as px

def create_treemap(dataframe):
    """
    Create a treemap where each type of lighting condition contains every type of weather condition.
    The percentages are determined by the number of accidents corresponding to the conditions.
    """
    # Group data by lighting and weather conditions, and count the number of accidents
    grouped_data = dataframe.groupby(['lighting_condition', 'weather_condition']).size().reset_index(name='Accident Count')
    print(dataframe['weather_condition'].unique())
    # Create the treemap
    fig = px.treemap(
        grouped_data,
        path=['lighting_condition', 'weather_condition'],
        values='Accident Count',
        color='weather_condition',
        color_discrete_map={
            'lighting_condition': 'green',
            'DAYLIGHT': 'white',
            'CLEAR': 'powderblue',
            'RAIN': 'deepskyblue',
            'SNOW': 'snow',
            'CLOUDY/OVERCAST': 'lightgray',
            'SUNLIGHT': 'yellow',
            'FOG/SMOKE/HAZE': 'gray',
            'BLOWING SNOW': 'whitesmoke',
            'FREEZING RAIN/DRIZZLE': 'steelblue',
            'SLEET/HAIL': 'Turquoise',
            'SEVERE CROSS WIND GATE': 'lightgreen',
            'BLOWING SAND, SOIL, DIRT': 'tan',
            'UNKNOWN': 'darkgray',
            'OTHER': 'black',
        },
        width=1000,
        height=700,
    )

        # Make the background transparent
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)'   # Transparent plot area
    )
    return fig