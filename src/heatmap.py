'''
    Fichier contenant les fonctions pour créer la matrice de chaleur (heatmap)
    montrant la relation entre les types de collision et la sévérité des blessures.
'''
import pandas as pd
import plotly.graph_objects as go

# Définition des types de collision et de blessure spécifiés dans le projet
COLLISION_TYPES = ['Turning', 'Angle', 'Rear end', 'Sideswipe (same direction)', 'Pedestrian']
INJURY_TYPES = ['No indication of injury', 'Non-incapacitating injury', 'Reported, not evident', 
                'Incapacitating injury', 'Fatal']

def prepare_heatmap_data(df):
    '''
    Prépare les données pour la heatmap en comptant le nombre d'accidents 
    par type de collision et type de blessure.
    '''
    # Filtrer les types de collision spécifiés
    df = df.copy()
    # Convertir en majuscules pour la correspondance
    df['first_crash_type'] = df['first_crash_type'].str.upper()
    
    # Créer un dictionnaire pour la correspondance entre les valeurs dans le dataset 
    # et les catégories spécifiées pour l'axe Y
    collision_mapping = {
        'TURNING': 'Turning',
        'ANGLE': 'Angle',
        'REAR END': 'Rear end',
        'SIDESWIPE SAME DIRECTION': 'Sideswipe (same direction)',
        'PEDESTRIAN': 'Pedestrian'
    }
    
    # Appliquer le mapping et filtrer pour ne garder que les types spécifiés
    df['collision_type'] = df['first_crash_type'].map(collision_mapping)
    df = df[df['collision_type'].isin(COLLISION_TYPES)]
    
    # Déterminer le type de blessure le plus grave pour chaque accident
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
    
    # Comptez le nombre d'accidents pour chaque combinaison
    heatmap_data = df.groupby(['collision_type', 'injury_type']).size().reset_index(name='count')
    
    # Créer un DataFrame pivot pour la heatmap
    pivot_data = heatmap_data.pivot(index='collision_type', columns='injury_type', values='count')
    
    # S'assurer que toutes les colonnes spécifiées sont présentes
    for injury in INJURY_TYPES:
        if injury not in pivot_data.columns:
            pivot_data[injury] = 0
    
    # Réordonner les colonnes selon l'ordre spécifié
    pivot_data = pivot_data[INJURY_TYPES]
    
    # S'assurer que toutes les lignes spécifiées sont présentes
    for collision in COLLISION_TYPES:
        if collision not in pivot_data.index:
            pivot_data.loc[collision] = [0] * len(INJURY_TYPES)
    
    # Réordonner les lignes selon l'ordre spécifié
    pivot_data = pivot_data.reindex(COLLISION_TYPES)
    
    # Remplir les valeurs NaN par 0
    pivot_data = pivot_data.fillna(0)
    
    return pivot_data

def create_heatmap(df):
    '''
    Crée une matrice de chaleur (heatmap) montrant le nombre d'accidents 
    par type de collision et type de blessure.
    '''
    # Préparer les données
    heatmap_data = prepare_heatmap_data(df)
    
    # Créer la figure
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=INJURY_TYPES,
        y=COLLISION_TYPES,
        colorscale='Blues',
        hovertemplate='Type de collision: %{y}<br>Type de blessure: %{x}<br>Nombre d\'accidents: %{z}<extra></extra>'
    ))
    
    # Mettre à jour la mise en page avec des options simplifiées
    fig.update_layout(
        title="Matrice de chaleur des accidents par type de collision et gravité des blessures",
        xaxis_title="Type de blessure",
        yaxis_title="Type de collision",
        xaxis_tickangle=-45,
        height=600,
        width=1000
    )
    
    return fig

def get_figure(df):
    '''
    Fonction principale qui renvoie la figure de la heatmap.
    Compatible avec l'API utilisée dans les autres visualisations.
    '''
    return create_heatmap(df)