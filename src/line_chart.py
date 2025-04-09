'''
    Contains some functions related to the creation of the line chart.
'''
import plotly.express as px
import hover_template

from template import THEME


def get_empty_figure(height=400):
    '''
    Returns the figure to display when there is no data to show.

    The text to display is : 'No data to display. Select a cell
    in the heatmap for more information.

    '''

    fig = px.scatter()

    fig.add_annotation(
        x=0.5,
        y=0.5,  
        text="No data to display. Select a cell in the heatmap for more information.",
        showarrow=False,
        font=dict(
            family="Arial",
            size=14,
            color="black"
        ),
        xref="paper",  
        yref="paper",  
    )

    fig.update_layout(
        dragmode=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=height,
        showlegend=False
    )

    return fig


def add_rectangle_shape(fig):
    '''
        Adds a rectangle to the figure displayed
        behind the informational text. The color
        is the 'pale_color' in the THEME dictionary.

        The rectangle's width takes up the entire
        paper of the figure. The height goes from
        0.25% to 0.75% the height of the figure.
    '''
    # TODO : Draw the rectangle
    layout = fig.layout

    fig_height = layout.height
    rect_height = [0.25 * fig_height, 0.75 * fig_height]

    pale_color = THEME['pale_color'] 

    fig.add_shape(
        type="rect",
        x0=0,
        y0=rect_height[0],
        x1=1,
        y1=rect_height[1],
        line=dict(width=0),
        fillcolor=pale_color,
        layer="below"
    )

    return fig


def get_figure(line_data, arrond, year):
    '''
        Generates the line chart using the given data.

        The ticks must show the zero-padded day and
        abbreviated month. The y-axis title should be 'Trees'
        and the title should indicated the displayed
        neighborhood and year.

        In the case that there is only one data point,
        the trace should be displayed as a single
        point instead of a line.

        Args:
            line_data: The data to display in the
            line chart
            arrond: The selected neighborhood
            year: The selected year
        Returns:
            The figure to be displayed
    '''
    # TODO : Construct the required figure. Don't forget to include the hover template
    fig = px.line(
        line_data,
        x='Date_Plantation', y='Trees',
        labels={'Date_Plantation': 'Date_Plantation', 'Trees': 'Trees'},
        title=f'Trees planted in {arrond} in {year}',
        template='custom_theme'
    )

    if len(line_data) == 1:
        fig.update_traces(mode='markers')

    fig.update_layout(
        xaxis=dict(
            tickformat='%d %b',
            title=''
        ),
        yaxis=dict(
            title='Trees'
        )
    )

    fig.update_traces(hovertemplate=hover_template.get_linechart_hover_template())

    return fig

