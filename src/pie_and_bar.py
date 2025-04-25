import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import qualitative
import numpy as np

INJURY_COLS = [
    "injuries_no_indication",
    "injuries_non_incapacitating",
    "injuries_reported_not_evident",
    "injuries_incapacitating",
    "injuries_fatal"
]

INJURY_TRANSLATIONS = {
    "injuries_no_indication": "Aucune blessure",
    "injuries_non_incapacitating": "Non incapacitante",
    "injuries_reported_not_evident": "Déclarée, non visible",
    "injuries_incapacitating": "Incapacitante",
    "injuries_fatal": "Mortelle"
}

ROAD_COND_TRANSLATIONS = {
    "DRY": "Sec",
    "WET": "Mouillé",
    "SNOW OR SLUSH": "Neige ou gadoue",
    "ICE": "Verglas",
    "SAND, MUD, DIRT": "Sable, boue ou terre",
    "OTHER": "Autre",
    "UNKNOWN": "Inconnu",
    "OTHERS": "Autres"
}

INTERSECTION_TRANSLATIONS = {
    "Y": "Oui",
    "N": "Non",
    "UNKNOWN": "Inconnu"
}


def load_data(filepath):
    return pd.read_csv(filepath)

def prepare_pie_data(df, category_col):
    if category_col == "roadway_surface_cond":
        df = df.copy()
        others_categories = [
            "UNKNOWN", 
            "SNOW OR SLUSH", 
            "ICE", 
            "OTHER", 
            "SAND, MUD, DIRT"
        ]
        df[category_col] = df[category_col].apply(
            lambda x: "OTHERS" if str(x).strip().upper() in others_categories else x
        )
    
    pie_df = df[category_col].value_counts().reset_index()
    pie_df.columns = [category_col, "Count"]
    return pie_df

def custom_hover_template(chart_type, **kwargs):
    """Génère des templates de tooltip personnalisés"""
    if chart_type == "pie":
        return (
            "<b>%{label}</b><br>"
            "%{value:,} accidents<br>"
            "<extra></extra>"
        )
    elif chart_type == "bar":
        return (
        f"<b>{kwargs.get('category_name', '')}</b><br>"
        f"Blessure : {INJURY_TRANSLATIONS.get(kwargs.get('injury_type', ''), '').title()}<br>"
        "%{y} accidents<br>"
        "<extra></extra>"
    )
    return ""

def prepare_bar_data(df, category_col):
    if category_col == "roadway_surface_cond":
        df = df.copy()
        others_categories = [
            "UNKNOWN", 
            "SNOW OR SLUSH", 
            "ICE", 
            "OTHER", 
            "SAND, MUD, DIRT"
        ]
        df[category_col] = df[category_col].apply(
            lambda x: "OTHERS" if str(x).strip().upper() in others_categories else x
        )
    
    grouped = df.groupby(category_col)[INJURY_COLS].sum().reset_index()
    melted = grouped.melt(id_vars=category_col, var_name="Injury Type", value_name="Count")
    melted["Count"] = melted["Count"].replace(0, 0.1)
    return melted

def create_combined_figure(pie_data, bar_data, category_col, title, pie_title, bar_title):
    categories = pie_data[category_col].tolist()
    if category_col == "roadway_surface_cond":
        translated_categories = [ROAD_COND_TRANSLATIONS.get(str(cat).strip().upper(), str(cat)) for cat in categories]
    elif category_col == "intersection_related_i":
        translated_categories = [INTERSECTION_TRANSLATIONS.get(str(cat).strip().upper(), str(cat)) for cat in categories]
    else:
        translated_categories = [str(cat) for cat in categories]

    if category_col == "roadway_surface_cond":
        color_map = {
            "Sec": "#dd6700",
            "Mouillé": "#1f77b4",
            "Autres": "grey",
        }
        default_color = "grey"
    elif category_col == "intersection_related_i":
        color_map = {
            "Oui": "#d62728",
            "Non": "#2ca02c",
            "Inconnu": "#D3D3D3"
        }
        default_color = "grey"
    else:
        color_map = dict(zip(translated_categories, qualitative.Plotly[:len(translated_categories)]))
        default_color = "#CCCCCC"

    for cat in translated_categories:
        if cat not in color_map:
            color_map[cat] = default_color

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(pie_title, bar_title),
        specs=[[{'type': 'domain'}, {'type': 'xy'}]],
        column_widths=[0.35, 0.65],
        horizontal_spacing=0.13,
    )

    if category_col == "roadway_surface_cond":
        translated_labels = [ROAD_COND_TRANSLATIONS.get(val.upper(), val) for val in pie_data[category_col]]
    elif category_col == "intersection_related_i":
        translated_labels = [INTERSECTION_TRANSLATIONS.get(val.upper(), val) for val in pie_data[category_col]]
    else:
        translated_labels = pie_data[category_col]
    
    fig.add_trace(
        go.Pie(
            labels=translated_labels,
            values=pie_data["Count"],
            marker=dict(
                colors=[color_map.get(val, default_color) for val in translated_labels],
                line=dict(color="white", width=1),
            ),
            showlegend=True,
            hovertemplate=custom_hover_template("pie"),
            name="",
            textinfo='percent',
            textposition='inside',
            textfont=dict(color="white", family="Lato, sans-serif"),
            hoverlabel=dict(
                bgcolor=[color_map.get(val, default_color) for val in translated_labels],
                font=dict(color="white", family="Lato, sans-serif"),
                bordercolor="white",
            ),
        ),
        row=1, col=1
    )

    for i, cat in enumerate(translated_categories):
        fig.add_trace(
            go.Bar(
                x=[],
                y=[],
                name=cat,
                marker_color=color_map.get(cat, default_color),
                showlegend=True,
                visible=True,
                legendgroup=cat
            ),
            row=1, col=2
        )
    
    traces = []
    for j, injury in enumerate(INJURY_COLS):
        for i, cat in enumerate(translated_categories):
            injury_data = bar_data[(bar_data[category_col] == cat) & (bar_data["Injury Type"] == injury)]
            fig.add_trace(
                go.Bar(
                x=[INJURY_TRANSLATIONS[injury]],
                y=injury_data["Count"],
                marker_color=color_map.get(cat, default_color),
                marker=dict(
                    line=dict(
                        color='white',
                        width=0.5
                    )
                ),
                showlegend=False,
                visible=True,
                legendgroup=cat,
                hovertemplate=custom_hover_template(
                    "bar",
                    injury_type=injury,
                    category_name=translated_categories[i]
                ),
                hoverlabel=dict(
                    bgcolor=color_map.get(cat, default_color),
                    font=dict(color="white", family="Lato, sans-serif"),
                    bordercolor="white",
                ),
                width=0.1,
            ),
            row=1, col=2
        )
            traces.append((cat, injury))

    # Menu déroulant
    buttons = []

    visible_all = [True] + [True] * len(translated_categories) + [True] * len(traces)
    buttons.append(dict(
        label="Tous les types de blessures",
        method="update",
        args=[{"visible": visible_all},
              {"showlegend": True}]
    ))

    for i, injury in enumerate(INJURY_COLS):
        visibility = [True]
        visibility.extend([True] * len(translated_categories))
        visibility.extend([(inj == injury) for (cat, inj) in traces])
        
        buttons.append(dict(
            label=INJURY_TRANSLATIONS[injury],
            method="update",
            args=[{"visible": visibility},
                  {"showlegend": True}]
        ))

    # Configuration des axes
    fig.update_xaxes(title_text="Type de blessure", row=1, col=2, title_font=dict(family="Lato, sans-serif"))
    fig.update_yaxes(title_text="Nombre d'accidents (logarithmique)", type="log", row=1, col=2, title_font=dict(family="Lato, sans-serif"))

    fig.update_layout(
        title_text=title,
        title_font=dict(family="Lato, sans-serif"),
        barmode="group",
        updatemenus=[dict(
            buttons=buttons,
            direction="down",
            showactive=True,
            active=0,
            x=0.145,
            xanchor="center",
            y=1.1,
            yanchor="top",
            bgcolor="white",
            bordercolor="lightgrey",
            borderwidth=1,
            font=dict(
                family="Lato, sans-serif", 
                color="#031732",
            ),
        )],
        legend_title_text="Intersection" if category_col == "intersection_related_i" 
                 else "Condition de<br>la chaussée" if category_col == "roadway_surface_cond" 
                 else category_col.replace("_", " ").title(),
        legend=dict(itemclick=False, y=0.8, itemwidth=40, font=dict(family="Lato, sans-serif"),),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, b=100, l=10, r=0),
        height=400,
        width=900,
    )

    return fig


# Fonctions spécifiques

def plot_intersection_vs_injury(df):
    category = "intersection_related_i"
    pie_data = prepare_pie_data(df, category)
    bar_data = prepare_bar_data(df, category)
    if category == "intersection_related_i":
        bar_data[category] = bar_data[category].apply(lambda x: INTERSECTION_TRANSLATIONS.get(str(x).upper(), x))
    return create_combined_figure(
        pie_data, bar_data, category,
        title="",
        pie_title="",
        bar_title=""
    )

def plot_condition_vs_injury(df):
    category = "roadway_surface_cond"
    pie_data = prepare_pie_data(df, category)
    bar_data = prepare_bar_data(df, category)
    if category == "roadway_surface_cond":
        bar_data[category] = bar_data[category].apply(lambda x: ROAD_COND_TRANSLATIONS.get(x.upper(), x))
    return create_combined_figure(
        pie_data, bar_data, category,
        title="",
        pie_title="",
        bar_title="",
    )
