'''
    Contains some functions related to the creation of the heatmap.
'''
import plotly.express as px
import hover_template
import pandas as pd

import plotly.io as pio


'''
    Contains some functions related to the creation of the heatmap.
'''
import plotly.express as px
import hover_template
import pandas as pd
import plotly.io as pio


def get_figure(data: pd.DataFrame):
    '''
        Generates the heatmap from the given dataset.

        Make sure to set the title of the color bar to 'Trees'
        and to display each year as an x-tick. The x and y axes should
        be titled "Year" and "Neighborhood". 

        Args:
            data: The data to display
        Returns:
            The figure to be displayed.
    '''
 
    fig = px.imshow(data, template='custom_theme')  # Changed from pio.templates['default'] to 'custom_theme'
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Neighborhood",
        coloraxis_colorbar=dict(
            title="Trees"
        ),
        dragmode=False  
    )

    fig.update_xaxes(tickvals=data.columns)

    fig.update_traces(hovertemplate=hover_template.get_heatmap_hover_template())

    return fig