import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import qualitative
import numpy as np

# Colonnes de blessures
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
            "Nombre : %{value:,}<br>"
            "Pourcentage : %{percent:.1%}"
            "<extra></extra>"
        )
    elif chart_type == "bar":
        return (
        f"<b>{INJURY_TRANSLATIONS.get(kwargs.get('injury_type', ''), '').title()}</b><br>"
        "Nombre : %{y:,}<br>"
        f"Catégorie : {kwargs.get('category_name', '')}"
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

    # Définir les palettes de couleurs spécifiques pour chaque graphique
    if category_col == "roadway_surface_cond":
        # Graphique 1: Conditions de la chaussée
        color_map = {
            "Sec": "#FF8C00",
            "Mouillé": "blue",
            "Autres": "grey"
        }
        # Appliquer gris à toutes les autres catégories
        default_color = "grey"
    elif category_col == "intersection_related_i":
        # Graphique 2: Intersection
        color_map = {
            "Oui": "blue",
            "Non": "#FF8C00",  # Vous pouvez changer cette couleur si besoin
            "Inconnu": "grey"
        }
        default_color = "grey"
    else:
        # Palette par défaut pour les autres cas
        color_map = dict(zip(translated_categories, qualitative.Plotly[:len(translated_categories)]))
        default_color = "#CCCCCC"

    # Remplir les couleurs manquantes avec la couleur par défaut
    for cat in translated_categories:
        if cat not in color_map:
            color_map[cat] = default_color

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(pie_title, bar_title),
        specs=[[{'type': 'domain'}, {'type': 'xy'}]]
    )

    # PIE chart
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
            marker=dict(colors=[color_map.get(val, default_color) for val in translated_labels]),
            showlegend=True,
            hovertemplate=custom_hover_template("pie"),
            name="",
            textinfo='percent',
            textposition='inside'
        ),
        row=1, col=1
    )

    # BAR chart - légendes
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
    
    # BAR chart - données
    traces = []
    for j, injury in enumerate(INJURY_COLS):
        for i, cat in enumerate(translated_categories):
            injury_data = bar_data[(bar_data[category_col] == cat) &
                               (bar_data["Injury Type"] == injury)]
            fig.add_trace(
                go.Bar(
                x=[INJURY_TRANSLATIONS[injury]],
                y=injury_data["Count"],
                marker_color=color_map.get(cat, default_color),
                showlegend=False,
                visible=True,
                legendgroup=cat,
                hovertemplate=custom_hover_template(
                    "bar",
                    injury_type=injury,
                    category_name=translated_categories[i]
                ),
                width=0.1
            ),
            row=1, col=2
        )
            traces.append((cat, injury))

    # Menu déroulant
    buttons = []

    visible_all = [True] + [True] * len(translated_categories) + [True] * len(traces)
    buttons.append(dict(
        label="See All",
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
    fig.update_xaxes(title_text="Type de blessure", row=1, col=2)
    fig.update_yaxes(title_text="Nombre d'accidents (logarithmique)", type="log", row=1, col=2)

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
        legend_title_text="Intersection" if category_col == "intersection_related_i" 
                 else "Condition de la chaussée" if category_col == "roadway_surface_cond" 
                 else category_col.replace("_", " ").title(),
        legend=dict(
        itemclick=False)
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
        pie_title="", #Répartition des accidents Ajouté le titre si besoin
        bar_title="" # Types de blessures (échelle log)
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
        pie_title="", #Répartition des accidents Ajouté le titre si besoin
        bar_title="" #Types de blessures (échelle log)
    )

