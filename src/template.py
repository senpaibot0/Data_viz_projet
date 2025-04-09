'''
    Contains the template to use in the data visualization.
'''
import plotly.graph_objects as go
import plotly.io as pio

THEME = {
    'background_color': '#ffffff',
    'font_family': 'Roboto',
    'accent_font_family': 'Roboto Slab',
    'dark_color': '#2A2B2E',
    'pale_color': '#DFD9E2',
    'line_chart_color': 'black',
    'label_font_size': 14,
    'label_background_color': '#ffffff',
    'colorscale': 'Bluyl'
}

def create_custom_theme():
    '''
        Adds a new layout template to pio's templates.
    '''
    template = go.layout.Template()
    template.layout = go.Layout(
        font=dict(
            family=THEME['font_family'],
            color=THEME['dark_color']
        ),
        paper_bgcolor=THEME['background_color'],
        plot_bgcolor=THEME['background_color'],
        hoverlabel=dict(
            font=dict(
                family=THEME['font_family'],
                color=THEME['dark_color'],
                size=THEME['label_font_size']
            ),
            bgcolor=THEME['label_background_color']
        ),
        hovermode='closest',
        xaxis=dict(
            tickangle=45
        ),
        coloraxis_colorbar=dict(
            title=dict(
                font=dict(
                    family=THEME['font_family'],
                    color=THEME['dark_color']
                )
            )
        )
    )
    template.data.scatter = [go.Scatter(line=dict(color=THEME['line_chart_color']))]
    template.layout.colorscale.sequential = THEME['colorscale']
    pio.templates['custom_theme'] = template
    return template 

def set_default_theme():
    '''
        Sets the default theme to be a combination of the 'plotly_white' theme and our custom theme.
    '''
    combined_template = pio.templates['plotly_white']
    pio.templates['custom_theme'] = combined_template
    pio.templates['custom_theme'].layout = create_custom_theme().layout
    pio.templates.default = 'custom_theme'