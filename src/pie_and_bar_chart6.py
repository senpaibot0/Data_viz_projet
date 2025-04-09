import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import qualitative

# Injury columns
INJURY_COLS = [
    "injuries_no_indication",
    "injuries_non_incapacitating",
    "injuries_reported_not_evident",
    "injuries_incapacitating",
    "injuries_fatal"
]

def load_data(filepath):
    return pd.read_csv(filepath)

def prepare_pie_data(df, category_col):
    if category_col == "roadway_surface_cond":
        df = df.copy()
        others_categories = ["UNKNOWN", "SNOW OR SLUSH", "ICE", "OTHER", "SAND, MUD, DIRT"]
        df[category_col] = df[category_col].apply(
            lambda x: "OTHERS" if str(x).strip().upper() in others_categories else x
        )
    pie_df = df[category_col].value_counts().reset_index()
    pie_df.columns = [category_col, "Count"]
    return pie_df

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

def prepare_bar_data(df, category_col):
    if category_col == "roadway_surface_cond":
        df = df.copy()
        others_categories = ["UNKNOWN", "SNOW OR SLUSH", "ICE", "OTHER", "SAND, MUD, DIRT"]
        df[category_col] = df[category_col].apply(
            lambda x: "OTHERS" if str(x).strip().upper() in others_categories else x
        )
    grouped = df.groupby(category_col)[INJURY_COLS].sum().reset_index()
    melted = grouped.melt(id_vars=category_col, var_name="Injury Type", value_name="Count")
    melted["Count"] = melted["Count"].replace(0, 0.1)  # Avoid log scale issues
    return melted

def create_combined_figure(pie_data, bar_data, category_col, title, pie_title, bar_title):
    categories = pie_data[category_col].tolist()
    colors = qualitative.Plotly[:len(categories)]
    color_map = dict(zip(categories, colors))

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(pie_title, bar_title),
        specs=[[{'type': 'domain'}, {'type': 'xy'}]]
    )

    # Pie chart
    fig.add_trace(
        go.Pie(
            labels=pie_data[category_col],
            values=pie_data["Count"],
            marker=dict(colors=[color_map[val] for val in pie_data[category_col]]),
            showlegend=True,
            hovertemplate=custom_hover_template("pie"),
            textinfo='percent',
            textposition='inside'
        ),
        row=1, col=1
    )

    # Bar chart - legend traces
    for i, cat in enumerate(categories):
        fig.add_trace(
            go.Bar(
                x=[],
                y=[],
                name=cat,
                marker_color=color_map[cat],
                showlegend=True,
                visible=True,
                legendgroup=cat
            ),
            row=1, col=2
        )

    # Bar chart - data traces
    traces = []
    for j, injury in enumerate(INJURY_COLS):
        for i, cat in enumerate(categories):
            injury_data = bar_data[(bar_data[category_col] == cat) &
                                   (bar_data["Injury Type"] == injury)]
            fig.add_trace(
                go.Bar(
                    x=[injury.replace("_", " ").title()],
                    y=injury_data["Count"],
                    marker_color=color_map[cat],
                    showlegend=False,
                    visible=True,
                    legendgroup=cat,
                    hovertemplate=custom_hover_template(
                        "bar",
                        injury_type=injury,
                        category_name=cat
                    ),
                    width=0.1
                ),
                row=1, col=2
            )
            traces.append((cat, injury))

    # Dropdown menu
    buttons = []
    visible_all = [True] + [True] * len(categories) + [True] * len(traces)
    buttons.append(dict(
        label="See All",
        method="update",
        args=[{"visible": visible_all}, {"showlegend": True}]
    ))

    for i, injury in enumerate(INJURY_COLS):
        visibility = [True] + [True] * len(categories)
        visibility.extend([(inj == injury) for (cat, inj) in traces])
        buttons.append(dict(
            label=injury.replace("injuries_", "").replace("_", " ").title(),
            method="update",
            args=[{"visible": visibility}, {"showlegend": True}]
        ))

    # Update layout
    fig.update_xaxes(title_text="Type of Injury", row=1, col=2)
    fig.update_yaxes(title_text="Number of Accidents (log)", type="log", row=1, col=2)
    fig.update_layout(
        title_text=title,
        barmode="group",
        updatemenus=[dict(
            buttons=buttons,
            direction="down",
            showactive=True,
            active=0,
            x=0.5,
            xanchor="center",
            y=1.15,
            yanchor="top"
        )],
        legend_title_text="Pavement Condition",
        legend=dict(itemclick=False)
    )

    return fig

def plot_condition_vs_injury(df):
    category = "roadway_surface_cond"
    pie_data = prepare_pie_data(df, category)
    bar_data = prepare_bar_data(df, category)
    return create_combined_figure(
        pie_data, bar_data, category,
        title="Accidents by Roadway Condition and Injury Severity",
        pie_title="Distribution of Accidents",
        bar_title="Injury Types (Log Scale)"
    )