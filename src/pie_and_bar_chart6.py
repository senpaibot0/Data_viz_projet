import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Injury columns
INJURY_COLS = [
    "injuries_no_indication",
    "injuries_non_incapacitating",
    "injuries_reported_not_evident",
    "injuries_incapacitating",
    "injuries_fatal"
]

# Mapping injury columns to readable labels
INJURY_LABELS = {
    "injuries_no_indication": "No Indication of Injury",
    "injuries_non_incapacitating": "Non-Incapacitating Injury",
    "injuries_reported_not_evident": "Reported, Not Evident",
    "injuries_incapacitating": "Incapacitating Injury",
    "injuries_fatal": "Fatal"
}

def prepare_pie_data(df, category_col):
    '''
    Prepares data for the pie chart by aggregating counts by roadway condition.
    '''
    df = df.copy()
    # Standardize category values
    df[category_col] = df[category_col].str.strip().str.upper()
    others_categories = ["UNKNOWN", "SNOW OR SLUSH", "ICE", "OTHER", "SAND, MUD, DIRT"]
    df[category_col] = df[category_col].apply(
        lambda x: "OTHERS" if x in others_categories else x
    )
    # Ensure only expected categories remain
    valid_categories = ["WET", "DRY", "OTHERS"]
    df = df[df[category_col].isin(valid_categories)]
    pie_df = df[category_col].value_counts().reset_index()
    pie_df.columns = [category_col, "Count"]
    return pie_df

def prepare_bar_data(df, category_col):
    '''
    Prepares data for the bar chart by aggregating injury counts by roadway condition.
    '''
    df = df.copy()
    # Standardize category values
    df[category_col] = df[category_col].str.strip().str.upper()
    others_categories = ["UNKNOWN", "SNOW OR SLUSH", "ICE", "OTHER", "SAND, MUD, DIRT"]
    df[category_col] = df[category_col].apply(
        lambda x: "OTHERS" if x in others_categories else x
    )
    # Ensure only expected categories remain
    valid_categories = ["WET", "DRY", "OTHERS"]
    df = df[df[category_col].isin(valid_categories)]
    grouped = df.groupby(category_col)[INJURY_COLS].sum().reset_index()
    melted = grouped.melt(id_vars=category_col, var_name="Injury Type", value_name="Count")
    return melted

def custom_hover_template(chart_type, **kwargs):
    if chart_type == "pie":
        return (
            "<b>%{label}</b><br>"
            "Count: %{value:,}<br>"
            "Percentage: %{percent:.1%}"
            "<extra></extra>"
        )
    elif chart_type == "bar":
        return (
            f"<b>{kwargs.get('injury_type', '').replace('_', ' ').title()}</b><br>"
            "Count: %{y:,}<br>"
            f"Category: {kwargs.get('category_name', '')}"
            "<extra></extra>"
        )
    return ""

def create_combined_figure(pie_data, bar_data, category_col, title, pie_title, bar_title):
    '''
    Creates a combined figure with a pie chart and a bar chart.
    '''
    # Define categories and colors
    categories = ["WET", "DRY", "OTHERS"]
    color_map = {
        "WET": "#FF9999",      # Reddish
        "DRY": "#66B2FF",      # Bluish
        "OTHERS": "#99FF99"    # Greenish
    }

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(pie_title, bar_title),
        specs=[[{'type': 'domain'}, {'type': 'xy'}]],
        column_widths=[0.35, 0.65],
        horizontal_spacing=0.2  # Further increased gap
    )

    # Pie chart
    pie_data = pie_data[pie_data[category_col].isin(categories)]
    fig.add_trace(
        go.Pie(
            labels=pie_data[category_col],
            values=pie_data["Count"],
            marker=dict(colors=[color_map[val] for val in pie_data[category_col]]),
            showlegend=True,
            hovertemplate=custom_hover_template("pie"),
            textinfo='label+percent',
            textposition='inside',
            insidetextorientation='radial',
            textfont=dict(size=14)
        ),
        row=1, col=1
    )

    # Bar chart
    for cat in categories:
        cat_data = bar_data[bar_data[category_col] == cat]
        x_values = [INJURY_LABELS[injury] for injury in cat_data["Injury Type"]]
        y_values = cat_data["Count"].tolist()
        fig.add_trace(
            go.Bar(
                x=x_values,
                y=y_values,
                name=cat,
                marker_color=color_map[cat],
                hovertemplate=custom_hover_template(
                    "bar",
                    injury_type="%{x}",
                    category_name=cat
                ),
                width=0.5
            ),
            row=1, col=2
        )

    # Update layout
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20),
            x=0.5,
            xanchor='center'
        ),
        barmode="group",
        height=600,
        width=1200,  # Reduced width to minimize empty space
        margin=dict(l=60, r=60, t=100, b=200),  # Increased bottom margin for legend and labels
        legend_title_text="Pavement Condition",
        legend=dict(
            font=dict(size=14),
            orientation="h",
            yanchor="bottom",
            y=-0.5,  # Further adjusted to ensure space
            xanchor="center",
            x=0.5
        )
    )

    # Update bar chart axes
    fig.update_xaxes(
        title_text="Type de blessure",
        title_font=dict(size=16),
        tickangle=-45,
        tickfont=dict(size=12),
        automargin=True,  # Automatically adjust margins for labels
        row=1, col=2
    )
    fig.update_yaxes(
        title_text="Nombre d'accidents",
        title_font=dict(size=16),
        tickfont=dict(size=14),
        row=1, col=2
    )

    # Update subplot titles font size
    fig.update_annotations(
        font=dict(size=16)
    )

    return fig

def plot_condition_vs_injury(df):
    '''
    Main function to create the combined pie and bar chart.
    '''
    category = "roadway_surface_cond"
    pie_data = prepare_pie_data(df, category)
    bar_data = prepare_bar_data(df, category)
    return create_combined_figure(
        pie_data, bar_data, category,
        title="Accidents by Roadway Condition and Injury Severity",
        pie_title="Distribution of Accidents",
        bar_title="Injury Types"
    )