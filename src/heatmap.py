'''
    Fichier contenant les fonctions pour créer la matrice de chaleur (heatmap)
    montrant la relation entre les types de collision et la sévérité des blessures.
'''
import pandas as pd
import plotly.graph_objects as go

COLLISION_TYPES = ['Turning', 'Angle', 'Rear end', 'Sideswipe (same direction)', 'Pedestrian']
INJURY_TYPES = ['No indication of injury', 'Non-incapacitating injury', 'Reported, not evident', 
                'Incapacitating injury', 'Fatal']

COLLISION_TRANSLATIONS = {
    'Turning': 'En tournant',
    'Angle': 'En angle',
    'Rear end': 'Arrière',
    'Sideswipe (same direction)': 'Latérale',
    'Pedestrian': 'Piétonne'
}

INJURY_TRANSLATIONS = {
    'No indication of injury': 'Aucune blessure',
    'Non-incapacitating injury': 'Non incapacitante',
    'Reported, not evident': 'Déclarée, non visible',
    'Incapacitating injury': 'Incapacitante',
    'Fatal': 'Mortelle'
}


def prepare_heatmap_data(df):
    '''
    Prépare les données pour la heatmap en comptant le nombre d'accidents 
    par type de collision et type de blessure.
    '''
    df = df.copy()
    df['first_crash_type'] = df['first_crash_type'].str.upper()
    
    collision_mapping = {
        'TURNING': 'Turning',
        'ANGLE': 'Angle',
        'REAR END': 'Rear end',
        'SIDESWIPE SAME DIRECTION': 'Sideswipe (same direction)',
        'PEDESTRIAN': 'Pedestrian'
    }
    
    df['collision_type'] = df['first_crash_type'].map(collision_mapping)
    df = df[df['collision_type'].isin(COLLISION_TYPES)]
    
    def get_injury_type(row):
        if row['injuries_fatal'] > 0:
            return 'Fatal'
        elif row['injuries_incapacitating'] > 0:
            return 'Incapacitating injury'
        elif row['injuries_non_incapacitating'] > 0:
            return 'Non-incapacitating injury'
        elif row['injuries_reported_not_evident'] > 0:
            return 'Reported, not evident'
        else:
            return 'No indication of injury'
    
    df['injury_type'] = df.apply(get_injury_type, axis=1)
    
    heatmap_data = df.groupby(['collision_type', 'injury_type']).size().reset_index(name='count')
    
    pivot_data = heatmap_data.pivot(index='collision_type', columns='injury_type', values='count')
    
    for injury in INJURY_TYPES:
        if injury not in pivot_data.columns:
            pivot_data[injury] = 0
    
    pivot_data = pivot_data[INJURY_TYPES]
    
    for collision in COLLISION_TYPES:
        if collision not in pivot_data.index:
            pivot_data.loc[collision] = [0] * len(INJURY_TYPES)
    
    pivot_data = pivot_data.reindex(COLLISION_TYPES)
    
    pivot_data = pivot_data.fillna(0)
    
    return pivot_data

def create_heatmap(df):
    '''
    Crée une matrice de chaleur (heatmap) montrant le nombre d'accidents 
    par type de collision et type de blessure.
    '''
    heatmap_data = prepare_heatmap_data(df)

    translated_x = [INJURY_TRANSLATIONS[x] for x in heatmap_data.columns]
    translated_y = [COLLISION_TRANSLATIONS[y] for y in heatmap_data.index]

    fig = go.Figure(
        data=go.Heatmap(
            z=heatmap_data.values,
            x=translated_x,
            y=translated_y,
            colorscale='Blues',
            hovertemplate='Collision : <b>%{y}</b><br>Blessure : %{x}<br>%{z} accidents<extra></extra>',
            hoverlabel=dict(
                bgcolor="#E6F0FF",
                font=dict(color="#031732", family="Lato, sans-serif"),
                bordercolor="black"
            ),
        ),
    )

    for i, y in enumerate(heatmap_data.index):
        for j, x in enumerate(heatmap_data.columns):
            fig.add_shape(
                type="rect",
                x0=j - 0.5,
                y0=i - 0.5,
                x1=j + 0.5,
                y1=i + 0.5,
                line=dict(color="white", width=1),
            )
            
    fig.update_layout(
        title="",
        xaxis_title="Type de blessure",
        yaxis_title="Type de collision",
        xaxis_tickangle=-45,
        margin=dict(l=100, r=20, t=20, b=50), 
        yaxis=dict(
            automargin=True, 
            tickfont=dict(size=10),
        ),
        xaxis=dict(
            tickfont=dict(size=9),
        ),
        height=400,
        width=850,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Lato, sans-serif", 
            color="#031732",
        )
    )

    return fig

def get_figure(df):
    '''
    Fonction principale qui renvoie la figure de la heatmap.
    Compatible avec l'API utilisée dans les autres visualisations.
    '''
    return create_heatmap(df)