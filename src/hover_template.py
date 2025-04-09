'''
    Provides the templates for the tooltips.
'''


def get_heatmap_hover_template():
    '''
        Sets the template for the hover tooltips in the heatmap.

        Contains three labels, followed by their corresponding
        value, separated by a colon: neighborhood, year and
        trees planted.

        The labels are font 'Roboto Slab' and bold. The values
        are font 'Roboto' and regular weight.
    '''
    hover_template = (
        "<b><span style='font-family: Roboto Slab; font-size: 16px; color: black;'>Neighborhood: %{customdata[0]}</span></b><br>" +
        "<b><span style='font-family: Roboto Slab; font-size: 16px; color: black;'>Year: %{customdata[1]}</span></b><br>" +
        "<b><span style='font-family: Roboto Slab; font-size: 16px; color: black;'>Trees Planted: %{customdata[2]}</span></b><br>"
    )
    return hover_template



def get_linechart_hover_template():
    '''
        Sets the template for the hover tooltips in the line chart.

        Contains two labels, followed by their corresponding
        value, separated by a colon: date and trees planted.

        The labels are font 'Roboto Slab' and bold. The values
        are font 'Roboto' and regular weight.
    '''
    hover_template = (
        "<b><span style='font-family: Roboto Slab; font-size: 16px; color: black;'>Date: %{x}</span></b><br>" +
        "<b><span style='font-family: Roboto Slab; font-size: 16px; color: black;'>Trees Planted: %{y}</span></b><br>"
    )
    return hover_template



