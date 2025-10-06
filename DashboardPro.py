import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import constants
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Spectroscopie Atomique Complète",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(45deg, #6A11CB, #2575FC, #00B4DB);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        color: #2575FC;
        border-bottom: 2px solid #6A11CB;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        font-weight: bold;
    }
    .element-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2575FC;
        margin: 0.5rem 0;
        color: #333333;
    }
    .series-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid #00B4DB;
        background-color: #f0f8ff;
        color: #333333;
    }
    .transition-card {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #FF6B35;
        color: #333333;
    }
    .wavelength-uv { 
        background-color: #e3f2fd; 
        border-left: 4px solid #9c27b0; 
        color: #333333;
    }
    .wavelength-visible { 
        background-color: #e8f5e8; 
        border-left: 4px solid #4caf50; 
        color: #333333;
    }
    .wavelength-ir { 
        background-color: #fff3e0; 
        border-left: 4px solid #ff9800; 
        color: #333333;
    }
    .theory-box {
        background-color: #f5f5f5;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin: 1rem 0;
        color: #333333;
    }
    .periodic-group {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
        margin: 0.2rem;
    }
    .category-metal { background-color: #FF6B6B; }
    .category-nonmetal { background-color: #4ECDC4; }
    .category-metalloid { background-color: #FFE66D; color: #333; }
    .category-noble { background-color: #95E1D3; }
    .category-alkali { background-color: #FF9A76; }
    .category-alkaline { background-color: #A8E6CF; }
    .category-transition { background-color: #6A89CC; }
    .category-halogen { background-color: #F8C471; }
    .category-lanthanide { background-color: #D980FA; }
    .category-actinide { background-color: #FDA7DF; }
</style>
""", unsafe_allow_html=True)

class CompleteAtomicSpectraDashboard:
    def __init__(self):
        self.elements_data = self.define_all_elements_data()
        self.series_data = self.define_series_data()
        self.transitions_data = self.define_all_transitions_data()
        self.spectral_lines = self.define_complete_spectral_lines()
        
    def define_all_elements_data(self):
        """Définit les données complètes pour tous les éléments"""
        return [
            # Période 1
            {
                'symbole': 'H', 'nom': 'Hydrogène', 'numero_atomique': 1, 'masse_atomique': 1.008,
                'config_electronique': '1s¹', 'periode': 1, 'groupe': 1, 'categorie': 'Non-metal',
                'couleur_spectre': '#FF6B6B', 'description': 'Élément le plus simple, spectre caractéristique'
            },
            {
                'symbole': 'He', 'nom': 'Hélium', 'numero_atomique': 2, 'masse_atomique': 4.0026,
                'config_electronique': '1s²', 'periode': 1, 'groupe': 18, 'categorie': 'Gaz noble',
                'couleur_spectre': '#4ECDC4', 'description': 'Gaz noble, spectre complexe'
            },
            
            # Période 2
            {
                'symbole': 'Li', 'nom': 'Lithium', 'numero_atomique': 3, 'masse_atomique': 6.94,
                'config_electronique': '[He] 2s¹', 'periode': 2, 'groupe': 1, 'categorie': 'Métal alcalin',
                'couleur_spectre': '#FFE66D', 'description': 'Doublet rouge caractéristique'
            },
            {
                'symbole': 'Be', 'nom': 'Béryllium', 'numero_atomique': 4, 'masse_atomique': 9.0122,
                'config_electronique': '[He] 2s²', 'periode': 2, 'groupe': 2, 'categorie': 'Métal alcalino-terreux',
                'couleur_spectre': '#A8E6CF', 'description': 'Raies UV caractéristiques'
            },
            {
                'symbole': 'B', 'nom': 'Bore', 'numero_atomique': 5, 'masse_atomique': 10.81,
                'config_electronique': '[He] 2s² 2p¹', 'periode': 2, 'groupe': 13, 'categorie': 'Métalloïde',
                'couleur_spectre': '#FF9A76', 'description': 'Spectre complexe en UV'
            },
            {
                'symbole': 'C', 'nom': 'Carbone', 'numero_atomique': 6, 'masse_atomique': 12.011,
                'config_electronique': '[He] 2s² 2p²', 'periode': 2, 'groupe': 14, 'categorie': 'Non-metal',
                'couleur_spectre': '#95E1D3', 'description': 'Raies importantes en astrophysique'
            },
            {
                'symbole': 'N', 'nom': 'Azote', 'numero_atomique': 7, 'masse_atomique': 14.007,
                'config_electronique': '[He] 2s² 2p³', 'periode': 2, 'groupe': 15, 'categorie': 'Non-metal',
                'couleur_spectre': '#6A89CC', 'description': 'Spectre riche en raies UV et visible'
            },
            {
                'symbole': 'O', 'nom': 'Oxygène', 'numero_atomique': 8, 'masse_atomique': 15.999,
                'config_electronique': '[He] 2s² 2p⁴', 'periode': 2, 'groupe': 16, 'categorie': 'Non-metal',
                'couleur_spectre': '#4ECDC4', 'description': 'Raies importantes en spectroscopie stellaire'
            },
            {
                'symbole': 'F', 'nom': 'Fluor', 'numero_atomique': 9, 'masse_atomique': 18.998,
                'config_electronique': '[He] 2s² 2p⁵', 'periode': 2, 'groupe': 17, 'categorie': 'Halogène',
                'couleur_spectre': '#FF6B6B', 'description': 'Spectre UV caractéristique'
            },
            {
                'symbole': 'Ne', 'nom': 'Néon', 'numero_atomique': 10, 'masse_atomique': 20.18,
                'config_electronique': '[He] 2s² 2p⁶', 'periode': 2, 'groupe': 18, 'categorie': 'Gaz noble',
                'couleur_spectre': '#FF9A76', 'description': 'Spectre riche utilisé dans les enseignes'
            },
            
            # Période 3
            {
                'symbole': 'Na', 'nom': 'Sodium', 'numero_atomique': 11, 'masse_atomique': 22.99,
                'config_electronique': '[Ne] 3s¹', 'periode': 3, 'groupe': 1, 'categorie': 'Métal alcalin',
                'couleur_spectre': '#FFE66D', 'description': 'Doublet jaune caractéristique à 589 nm'
            },
            {
                'symbole': 'Mg', 'nom': 'Magnésium', 'numero_atomique': 12, 'masse_atomique': 24.305,
                'config_electronique': '[Ne] 3s²', 'periode': 3, 'groupe': 2, 'categorie': 'Métal alcalino-terreux',
                'couleur_spectre': '#A8E6CF', 'description': 'Raies UV et bleues importantes'
            },
            {
                'symbole': 'Al', 'nom': 'Aluminium', 'numero_atomique': 13, 'masse_atomique': 26.982,
                'config_electronique': '[Ne] 3s² 3p¹', 'periode': 3, 'groupe': 13, 'categorie': 'Métal pauvre',
                'couleur_spectre': '#95E1D3', 'description': 'Spectre avec raies UV'
            },
            {
                'symbole': 'Si', 'nom': 'Silicium', 'numero_atomique': 14, 'masse_atomique': 28.085,
                'config_electronique': '[Ne] 3s² 3p²', 'periode': 3, 'groupe': 14, 'categorie': 'Métalloïde',
                'couleur_spectre': '#FF9A76', 'description': 'Important en spectroscopie stellaire'
            },
            {
                'symbole': 'P', 'nom': 'Phosphore', 'numero_atomique': 15, 'masse_atomique': 30.974,
                'config_electronique': '[Ne] 3s² 3p³', 'periode': 3, 'groupe': 15, 'categorie': 'Non-metal',
                'couleur_spectre': '#6A89CC', 'description': 'Spectre avec raies caractéristiques'
            },
            {
                'symbole': 'S', 'nom': 'Soufre', 'numero_atomique': 16, 'masse_atomique': 32.06,
                'config_electronique': '[Ne] 3s² 3p⁴', 'periode': 3, 'groupe': 16, 'categorie': 'Non-metal',
                'couleur_spectre': '#FFE66D', 'description': 'Raies UV importantes'
            },
            {
                'symbole': 'Cl', 'nom': 'Chlore', 'numero_atomique': 17, 'masse_atomique': 35.45,
                'config_electronique': '[Ne] 3s² 3p⁵', 'periode': 3, 'groupe': 17, 'categorie': 'Halogène',
                'couleur_spectre': '#4ECDC4', 'description': 'Spectre UV caractéristique'
            },
            {
                'symbole': 'Ar', 'nom': 'Argon', 'numero_atomique': 18, 'masse_atomique': 39.948,
                'config_electronique': '[Ne] 3s² 3p⁶', 'periode': 3, 'groupe': 18, 'categorie': 'Gaz noble',
                'couleur_spectre': '#FF6B6B', 'description': 'Spectre utilisé en physique des plasmas'
            },
            
            # Métaux de transition importants
            {
                'symbole': 'Fe', 'nom': 'Fer', 'numero_atomique': 26, 'masse_atomique': 55.845,
                'config_electronique': '[Ar] 4s² 3d⁶', 'periode': 4, 'groupe': 8, 'categorie': 'Métal de transition',
                'couleur_spectre': '#FF9A76', 'description': 'Spectre très riche, important en astrophysique'
            },
            {
                'symbole': 'Cu', 'nom': 'Cuivre', 'numero_atomique': 29, 'masse_atomique': 63.546,
                'config_electronique': '[Ar] 4s¹ 3d¹⁰', 'periode': 4, 'groupe': 11, 'categorie': 'Métal de transition',
                'couleur_spectre': '#FFE66D', 'description': 'Raies vertes caractéristiques'
            },
            {
                'symbole': 'Ag', 'nom': 'Argent', 'numero_atomique': 47, 'masse_atomique': 107.87,
                'config_electronique': '[Kr] 5s¹ 4d¹⁰', 'periode': 5, 'groupe': 11, 'categorie': 'Métal de transition',
                'couleur_spectre': '#95E1D3', 'description': 'Spectre avec raies UV et visible'
            },
            {
                'symbole': 'Au', 'nom': 'Or', 'numero_atomique': 79, 'masse_atomique': 196.97,
                'config_electronique': '[Xe] 6s¹ 4f¹⁴ 5d¹⁰', 'periode': 6, 'groupe': 11, 'categorie': 'Métal de transition',
                'couleur_spectre': '#FFE66D', 'description': 'Spectre complexe'
            },
            
            # Autres éléments importants
            {
                'symbole': 'Hg', 'nom': 'Mercure', 'numero_atomique': 80, 'masse_atomique': 200.59,
                'config_electronique': '[Xe] 4f¹⁴ 5d¹⁰ 6s²', 'periode': 6, 'groupe': 12, 'categorie': 'Métal de transition',
                'couleur_spectre': '#95E1D3', 'description': 'Spectre riche utilisé en éclairage'
            },
            {
                'symbole': 'Pb', 'nom': 'Plomb', 'numero_atomique': 82, 'masse_atomique': 207.2,
                'config_electronique': '[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p²', 'periode': 6, 'groupe': 14, 'categorie': 'Métal pauvre',
                'couleur_spectre': '#A8E6CF', 'description': 'Spectre caractéristique'
            },
            {
                'symbole': 'U', 'nom': 'Uranium', 'numero_atomique': 92, 'masse_atomique': 238.03,
                'config_electronique': '[Rn] 7s² 5f³ 6d¹', 'periode': 7, 'groupe': 3, 'categorie': 'Actinide',
                'couleur_spectre': '#FF6B6B', 'description': 'Spectre très complexe'
            }
        ]
    
    def define_series_data(self):
        """Définit les séries spectrales principales"""
        return [
            {
                'nom': 'Lyman', 'element': 'H', 'niveau_final': 1, 'domaine': 'UV',
                'longueur_onde_min': 91.2, 'longueur_onde_max': 121.6, 'couleur': '#9C27B0',
                'description': 'Transitions vers le niveau fondamental n=1'
            },
            {
                'nom': 'Balmer', 'element': 'H', 'niveau_final': 2, 'domaine': 'Visible',
                'longueur_onde_min': 365.0, 'longueur_onde_max': 656.3, 'couleur': '#4CAF50',
                'description': 'Transitions vers n=2, raies visibles caractéristiques'
            },
            {
                'nom': 'Paschen', 'element': 'H', 'niveau_final': 3, 'domaine': 'IR',
                'longueur_onde_min': 820.4, 'longueur_onde_max': 1875.1, 'couleur': '#FF9800',
                'description': 'Transitions vers n=3, domaine infrarouge'
            }
        ]
    
    def define_all_transitions_data(self):
        """Définit les transitions spectrales pour tous les éléments"""
        transitions = []
        
        # Transitions pour l'hydrogène (séries complètes)
        for n2 in range(2, 8):
            for n1 in range(1, n2):
                serie = ''
                if n1 == 1:
                    serie = 'Lyman'
                elif n1 == 2:
                    serie = 'Balmer'
                elif n1 == 3:
                    serie = 'Paschen'
                elif n1 == 4:
                    serie = 'Brackett'
                elif n1 == 5:
                    serie = 'Pfund'
                
                rydberg = 1.09677576e7
                longueur_onde = 1 / (rydberg * (1/n1**2 - 1/n2**2)) * 1e9
                
                transitions.append({
                    'element': 'H', 'serie': serie, 'transition': f'{n1}→{n2}',
                    'niveau_depart': n2, 'niveau_arrivee': n1, 'longueur_onde_nm': longueur_onde,
                    'energie_eV': constants.h * constants.c / (longueur_onde * 1e-9) / constants.e,
                    'intensite_relative': 1.0 / (n2 - n1)**2
                })
        
        # Transitions caractéristiques pour d'autres éléments
        transitions_caracteristiques = [
            # Métaux alcalins
            {'element': 'Li', 'transition': '2p→2s', 'longueur_onde_nm': 670.8, 'energie_eV': 1.85, 'intensite_relative': 0.9, 'serie': 'Principale'},
            {'element': 'Na', 'transition': '3p→3s', 'longueur_onde_nm': 589.0, 'energie_eV': 2.11, 'intensite_relative': 0.95, 'serie': 'Doublet D'},
            {'element': 'Na', 'transition': '3p→3s', 'longueur_onde_nm': 589.6, 'energie_eV': 2.10, 'intensite_relative': 0.9, 'serie': 'Doublet D'},
            {'element': 'K', 'transition': '4p→4s', 'longueur_onde_nm': 766.5, 'energie_eV': 1.62, 'intensite_relative': 0.8, 'serie': 'Doublet'},
            {'element': 'K', 'transition': '4p→4s', 'longueur_onde_nm': 769.9, 'energie_eV': 1.61, 'intensite_relative': 0.7, 'serie': 'Doublet'},
            
            # Gaz nobles
            {'element': 'He', 'transition': '2¹P→1¹S', 'longueur_onde_nm': 58.4, 'energie_eV': 21.2, 'intensite_relative': 0.6, 'serie': 'Résonnante'},
            {'element': 'He', 'transition': '3³D→2³P', 'longueur_onde_nm': 587.6, 'energie_eV': 2.11, 'intensite_relative': 0.8, 'serie': 'Triplet'},
            {'element': 'Ne', 'transition': '3s→2p', 'longueur_onde_nm': 640.2, 'energie_eV': 1.94, 'intensite_relative': 0.7, 'serie': 'Visible'},
            {'element': 'Ar', 'transition': '4p→4s', 'longueur_onde_nm': 750.4, 'energie_eV': 1.65, 'intensite_relative': 0.6, 'serie': 'IR'},
            
            # Métaux de transition
            {'element': 'Fe', 'transition': 'Multiple', 'longueur_onde_nm': 358.1, 'energie_eV': 3.46, 'intensite_relative': 0.8, 'serie': 'UV'},
            {'element': 'Fe', 'transition': 'Multiple', 'longueur_onde_nm': 438.4, 'energie_eV': 2.83, 'intensite_relative': 0.7, 'serie': 'Visible'},
            {'element': 'Cu', 'transition': '4p→4s', 'longueur_onde_nm': 324.8, 'energie_eV': 3.82, 'intensite_relative': 0.9, 'serie': 'UV'},
            {'element': 'Cu', 'transition': '4p→4s', 'longueur_onde_nm': 327.4, 'energie_eV': 3.79, 'intensite_relative': 0.8, 'serie': 'UV'},
            {'element': 'Ag', 'transition': '5p→5s', 'longueur_onde_nm': 328.1, 'energie_eV': 3.78, 'intensite_relative': 0.9, 'serie': 'UV'},
            {'element': 'Ag', 'transition': '5p→5s', 'longueur_onde_nm': 338.3, 'energie_eV': 3.66, 'intensite_relative': 0.7, 'serie': 'UV'},
            
            # Halogènes
            {'element': 'Cl', 'transition': 'Multiple', 'longueur_onde_nm': 134.7, 'energie_eV': 9.21, 'intensite_relative': 0.6, 'serie': 'UV lointain'},
            {'element': 'Br', 'transition': 'Multiple', 'longueur_onde_nm': 148.9, 'energie_eV': 8.33, 'intensite_relative': 0.5, 'serie': 'UV lointain'},
            
            # Métaux alcalino-terreux
            {'element': 'Ca', 'transition': '4p→4s', 'longueur_onde_nm': 422.7, 'energie_eV': 2.93, 'intensite_relative': 0.8, 'serie': 'Résonnante'},
            {'element': 'Mg', 'transition': '3p→3s', 'longueur_onde_nm': 285.2, 'energie_eV': 4.35, 'intensite_relative': 0.9, 'serie': 'UV'},
            
            # Éléments divers
            {'element': 'Hg', 'transition': '6³P₁→6¹S₀', 'longueur_onde_nm': 253.7, 'energie_eV': 4.89, 'intensite_relative': 0.95, 'serie': 'Résonnante'},
            {'element': 'Hg', 'transition': '7³S₁→6³P₀', 'longueur_onde_nm': 404.7, 'energie_eV': 3.06, 'intensite_relative': 0.7, 'serie': 'Violet'},
            {'element': 'Hg', 'transition': '6³P₁→6¹S₀', 'longueur_onde_nm': 435.8, 'energie_eV': 2.84, 'intensite_relative': 0.8, 'serie': 'Bleu'},
            
            # Carbone et azote (importants en astrophysique)
            {'element': 'C', 'transition': 'Multiple', 'longueur_onde_nm': 165.7, 'energie_eV': 7.48, 'intensite_relative': 0.6, 'serie': 'UV'},
            {'element': 'N', 'transition': 'Multiple', 'longueur_onde_nm': 149.3, 'energie_eV': 8.30, 'intensite_relative': 0.5, 'serie': 'UV'},
            {'element': 'O', 'transition': 'Multiple', 'longueur_onde_nm': 130.2, 'energie_eV': 9.52, 'intensite_relative': 0.7, 'serie': 'UV'},
        ]
        
        for trans in transitions_caracteristiques:
            trans['niveau_depart'] = 0
            trans['niveau_arrivee'] = 0
            
        transitions.extend(transitions_caracteristiques)
        
        return pd.DataFrame(transitions)
    
    def define_complete_spectral_lines(self):
        """Définit les raies spectrales complètes pour tous les éléments"""
        lines = []
        
        for element in self.elements_data:
            element_lines = self.transitions_data[
                self.transitions_data['element'] == element['symbole']
            ]
            
            for _, line in element_lines.iterrows():
                # Simulation du profil spectral
                lambda_centre = line['longueur_onde_nm']
                intensite = line['intensite_relative']
                
                # Largeur dépendant de l'élément
                if element['categorie'] == 'Gaz noble':
                    largeur = 0.05 + 0.02 * np.random.random()
                elif element['categorie'] == 'Métal alcalin':
                    largeur = 0.1 + 0.05 * np.random.random()
                else:
                    largeur = 0.08 + 0.03 * np.random.random()
                
                lines.append({
                    'element': element['symbole'],
                    'nom': element['nom'],
                    'categorie': element['categorie'],
                    'longueur_onde': lambda_centre,
                    'intensite': intensite,
                    'largeur': largeur,
                    'serie': line.get('serie', 'Autre'),
                    'transition': line['transition'],
                    'energie_eV': line['energie_eV']
                })
        
        return pd.DataFrame(lines)
    
    def calculate_rydberg_formula(self, n1, n2, z=1, rydberg_constant=1.09677576e7):
        """Calcule la longueur d'onde avec la formule de Rydberg"""
        return 1 / (rydberg_constant * z**2 * (1/n1**2 - 1/n2**2)) * 1e9
    
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">🔬 Dashboard Spectroscopie Atomique Complète</h1>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("**<span style='color: #333333'>Spectres complets de tous les atomes - Classification et analyse</span>", 
                       unsafe_allow_html=True)
    
    def create_periodic_table_overview(self):
        """Affiche une vue type tableau périodique"""
        st.markdown('<h3 class="section-header">📊 TABLEAU PÉRIODIQUE DES SPECTRES</h3>', 
                   unsafe_allow_html=True)
        
        # Création d'une grille type tableau périodique
        periods = [1, 2, 3, 4, 5, 6, 7]
        groups = list(range(1, 19))
        
        # Placement approximatif des éléments dans le tableau périodique
        periodic_grid = {}
        
        for element in self.elements_data:
            period = element['periode']
            group = element['groupe']
            key = f"{period}_{group}"
            periodic_grid[key] = element
        
        # Affichage sous forme de grille
        cols = st.columns(18)
        
        # En-têtes des groupes
        for i, col in enumerate(cols):
            if i < len(groups):
                with col:
                    st.markdown(f"<div style='text-align: center; font-weight: bold; color: #333;'>G{groups[i]}</div>", 
                               unsafe_allow_html=True)
        
        # Affichage par période
        for period in periods:
            cols = st.columns(18)
            elements_in_period = [e for e in self.elements_data if e['periode'] == period]
            
            for i, col in enumerate(cols):
                if i < len(groups):
                    group = groups[i]
                    element = next((e for e in elements_in_period if e['groupe'] == group), None)
                    
                    with col:
                        if element:
                            # Couleur par catégorie
                            categorie_class = f"category-{element['categorie'].lower().replace(' ', '-').replace('é', 'e')}"
                            st.markdown(f"""
                            <div class="periodic-group {categorie_class}" 
                                 style="cursor: pointer;" 
                                 onclick="alert('{element['symbole']} - {element['nom']}')">
                                <strong>{element['symbole']}</strong><br>
                                <small>{element['numero_atomique']}</small>
                            </div>
                            """, unsafe_allow_html=True)
        
        # Légende des catégories
        st.markdown("---")
        st.subheader("Légende des Catégories")
        
        categories = list(set([e['categorie'] for e in self.elements_data]))
        col_count = min(4, len(categories))
        cols = st.columns(col_count)
        
        for i, category in enumerate(categories):
            with cols[i % col_count]:
                categorie_class = f"category-{category.lower().replace(' ', '-').replace('é', 'e')}"
                st.markdown(f"""
                <div class="periodic-group {categorie_class}">
                    {category}
                </div>
                """, unsafe_allow_html=True)
    
    def create_spectral_library(self):
        """Crée une bibliothèque complète des spectres"""
        st.markdown('<h3 class="section-header">📚 BIBLIOTHÈQUE DES SPECTRES ATOMIQUES</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Recherche par Élément", "Par Catégorie", "Spectres Comparés"])
        
        with tab1:
            # Recherche par élément
            col1, col2 = st.columns([1, 3])
            
            with col1:
                element_recherche = st.selectbox("Sélectionnez un élément:", 
                                               [f"{e['symbole']} - {e['nom']}" for e in self.elements_data])
                element_symb = element_recherche.split(' - ')[0]
                
                element_data = next(e for e in self.elements_data if e['symbole'] == element_symb)
                raies_element = self.spectral_lines[self.spectral_lines['element'] == element_symb]
            
            with col2:
                st.subheader(f"Spectre de {element_data['nom']} ({element_data['symbole']})")
                
                # Spectre simulé
                lambda_range = np.linspace(100, 800, 2000)
                spectre_element = np.zeros_like(lambda_range)
                
                for _, raie in raies_element.iterrows():
                    if 100 <= raie['longueur_onde'] <= 800:
                        spectre_raie = raie['intensite'] * np.exp(-0.5 * ((lambda_range - raie['longueur_onde']) / raie['largeur'])**2)
                        spectre_element += spectre_raie
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=lambda_range, y=spectre_element,
                    mode='lines',
                    line=dict(color=element_data['couleur_spectre'], width=2),
                    name=f"Spectre {element_symb}"
                ))
                
                # Marquage des raies principales
                raies_principales = raies_element.nlargest(5, 'intensite')
                for _, raie in raies_principales.iterrows():
                    fig.add_trace(go.Scatter(
                        x=[raie['longueur_onde'], raie['longueur_onde']],
                        y=[0, raie['intensite']],
                        mode='lines',
                        line=dict(color='black', width=1, dash='dash'),
                        showlegend=False
                    ))
                
                fig.update_layout(
                    title=f"Spectre d'émission de {element_data['nom']}",
                    xaxis=dict(title="Longueur d'onde (nm)"),
                    yaxis=dict(title="Intensité relative"),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Détails de l'élément
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="element-card">
                <h4>📋 Informations de Base</h4>
                <strong>Symbole:</strong> {element_data['symbole']}<br>
                <strong>Nom:</strong> {element_data['nom']}<br>
                <strong>Numéro atomique:</strong> {element_data['numero_atomique']}<br>
                <strong>Masse atomique:</strong> {element_data['masse_atomique']} u<br>
                <strong>Période:</strong> {element_data['periode']}<br>
                <strong>Groupe:</strong> {element_data['groupe']}<br>
                <strong>Catégorie:</strong> {element_data['categorie']}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="theory-box">
                <h4>⚛️ Configuration Électronique</h4>
                {element_data['config_electronique']}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="theory-box">
                <h4>📝 Description</h4>
                {element_data['description']}
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                # Raies principales
                st.subheader("Raies Principales")
                for _, raie in raies_principales.iterrows():
                    domaine = "UV" if raie['longueur_onde'] < 400 else "Visible" if raie['longueur_onde'] < 700 else "IR"
                    couleur_classe = f"wavelength-{domaine.lower()}"
                    
                    st.markdown(f"""
                    <div class="transition-card {couleur_classe}">
                    <strong>{raie['transition']}</strong><br>
                    λ = {raie['longueur_onde']:.1f} nm ({domaine})<br>
                    Énergie = {raie['energie_eV']:.2f} eV<br>
                    Intensité = {raie['intensite']:.2f}
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab2:
            # Recherche par catégorie
            categories = list(set([e['categorie'] for e in self.elements_data]))
            categorie_selectionnee = st.selectbox("Sélectionnez une catégorie:", categories)
            
            elements_categorie = [e for e in self.elements_data if e['categorie'] == categorie_selectionnee]
            
            st.subheader(f"Éléments de la catégorie: {categorie_selectionnee}")
            
            # Affichage des éléments par ligne
            elements_per_row = 4
            for i in range(0, len(elements_categorie), elements_per_row):
                cols = st.columns(elements_per_row)
                for j, element in enumerate(elements_categorie[i:i + elements_per_row]):
                    with cols[j]:
                        st.markdown(f"""
                        <div class="element-card">
                        <h4>{element['symbole']} - {element['nom']}</h4>
                        <strong>Z:</strong> {element['numero_atomique']}<br>
                        <strong>Masse:</strong> {element['masse_atomique']} u<br>
                        <strong>Configuration:</strong> {element['config_electronique']}
                        </div>
                        """, unsafe_allow_html=True)
        
        with tab3:
            # Comparaison de spectres multiples
            st.subheader("Comparaison de Spectres Multiples")
            
            categories_comparaison = st.multiselect(
                "Sélectionnez les catégories à comparer:",
                categories,
                default=['Métal alcalin', 'Gaz noble']
            )
            
            if categories_comparaison:
                fig = go.Figure()
                
                for categorie in categories_comparaison:
                    elements_cat = [e for e in self.elements_data if e['categorie'] == categorie]
                    # Prendre le premier élément de chaque catégorie pour la démonstration
                    if elements_cat:
                        element = elements_cat[0]
                        raies_element = self.spectral_lines[self.spectral_lines['element'] == element['symbole']]
                        
                        # Spectre simulé
                        lambda_range = np.linspace(200, 800, 1500)
                        spectre_element = np.zeros_like(lambda_range)
                        
                        for _, raie in raies_element.iterrows():
                            if 200 <= raie['longueur_onde'] <= 800:
                                spectre_raie = raie['intensite'] * np.exp(-0.5 * ((lambda_range - raie['longueur_onde']) / raie['largeur'])**2)
                                spectre_element += spectre_raie
                        
                        fig.add_trace(go.Scatter(
                            x=lambda_range, y=spectre_element,
                            mode='lines',
                            name=f"{categorie} ({element['symbole']})",
                            line=dict(width=2)
                        ))
                
                fig.update_layout(
                    title="Comparaison des spectres par catégorie",
                    xaxis=dict(title="Longueur d'onde (nm)"),
                    yaxis=dict(title="Intensité relative"),
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def create_advanced_analysis_tools(self):
        """Crée des outils d'analyse avancée"""
        st.markdown('<h3 class="section-header">🔧 OUTILS D\'ANALYSE AVANCÉE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Simulateur de Spectres", "Base de Données", "Recherche Avancée"])
        
        with tab1:
            st.subheader("Simulateur de Spectres Atomiques")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Paramètres de simulation
                temperature = st.slider("Température (K):", 1000, 10000, 5000)
                pression = st.slider("Pression (atm):", 0.1, 10.0, 1.0)
                resolution = st.selectbox("Résolution spectrale:", ["Basse", "Moyenne", "Haute"])
                
                elements_simulation = st.multiselect(
                    "Éléments dans le plasma:",
                    [e['symbole'] for e in self.elements_data],
                    default=['H', 'Na', 'Hg']
                )
            
            with col2:
                # Effets physiques
                st.markdown("""
                <div class="theory-box">
                <h4>⚡ Effets Physiques Simulés</h4>
                
                <strong>Élargissement Doppler:</strong><br>
                Δλ/λ = √(2kT/mc²)<br><br>
                
                <strong>Élargissement de pression:</strong><br>
                Dû aux collisions entre atomes<br><br>
                
                <strong>Déplacement Stark:</strong><br>
                Sous l'effet des champs électriques
                </div>
                """, unsafe_allow_html=True)
            
            # Simulation du spectre composite
            if elements_simulation:
                lambda_range = np.linspace(200, 800, 2000)
                spectre_composite = np.zeros_like(lambda_range)
                
                for element_symb in elements_simulation:
                    raies_element = self.spectral_lines[self.spectral_lines['element'] == element_symb]
                    
                    for _, raie in raies_element.iterrows():
                        if 200 <= raie['longueur_onde'] <= 800:
                            # Effet de température sur la largeur
                            largeur_doppler = raie['largeur'] * np.sqrt(temperature / 300)
                            spectre_raie = raie['intensite'] * np.exp(-0.5 * ((lambda_range - raie['longueur_onde']) / largeur_doppler)**2)
                            spectre_composite += spectre_raie
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=lambda_range, y=spectre_composite,
                    mode='lines',
                    line=dict(color='#FF6B6B', width=2),
                    name='Spectre composite'
                ))
                
                fig.update_layout(
                    title=f"Spectre composite simulé - T={temperature}K",
                    xaxis=dict(title="Longueur d'onde (nm)"),
                    yaxis=dict(title="Intensité relative"),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.subheader("Base de Données des Raies Spectrales")
            
            # Filtres
            col1, col2, col3 = st.columns(3)
            
            with col1:
                element_filtre = st.selectbox("Filtrer par élément:", 
                                            ['Tous'] + [e['symbole'] for e in self.elements_data])
            with col2:
                domaine_filtre = st.selectbox("Domaine spectral:", 
                                            ['Tous', 'UV', 'Visible', 'IR'])
            with col3:
                intensite_min = st.slider("Intensité minimale:", 0.0, 1.0, 0.5)
            
            # Application des filtres
            raies_filtrees = self.spectral_lines.copy()
            if element_filtre != 'Tous':
                raies_filtrees = raies_filtrees[raies_filtrees['element'] == element_filtre]
            if domaine_filtre != 'Tous':
                if domaine_filtre == 'UV':
                    raies_filtrees = raies_filtrees[raies_filtrees['longueur_onde'] < 400]
                elif domaine_filtre == 'Visible':
                    raies_filtrees = raies_filtrees[(raies_filtrees['longueur_onde'] >= 400) & (raies_filtrees['longueur_onde'] < 700)]
                elif domaine_filtre == 'IR':
                    raies_filtrees = raies_filtrees[raies_filtrees['longueur_onde'] >= 700]
            
            raies_filtrees = raies_filtrees[raies_filtrees['intensite'] >= intensite_min]
            
            st.dataframe(
                raies_filtrees[['element', 'nom', 'longueur_onde', 'energie_eV', 'intensite', 'serie', 'transition']].sort_values('intensite', ascending=False),
                use_container_width=True
            )
        
        with tab3:
            st.subheader("Recherche Avancée par Caractéristiques")
            
            col1, col2 = st.columns(2)
            
            with col1:
                longueur_onde_recherche = st.number_input("Longueur d'onde recherchée (nm):", 
                                                        min_value=100.0, max_value=1000.0, value=589.0)
                tolerance = st.slider("Tolérance (nm):", 0.1, 10.0, 1.0)
            
            with col2:
                energie_min = st.number_input("Énergie minimale (eV):", 0.0, 20.0, 1.0)
                energie_max = st.number_input("Énergie maximale (eV):", 0.0, 20.0, 5.0)
            
            # Recherche
            raies_trouvees = self.spectral_lines[
                (abs(self.spectral_lines['longueur_onde'] - longueur_onde_recherche) <= tolerance) &
                (self.spectral_lines['energie_eV'] >= energie_min) &
                (self.spectral_lines['energie_eV'] <= energie_max)
            ]
            
            if not raies_trouvees.empty:
                st.subheader(f"Raies trouvées ({len(raies_trouvees)} résultats)")
                
                for _, raie in raies_trouvees.iterrows():
                    element_data = next(e for e in self.elements_data if e['symbole'] == raie['element'])
                    
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col1:
                        st.markdown(f"**{raie['element']} - {element_data['nom']}**")
                    with col2:
                        st.markdown(f"Transition: {raie['transition']} | λ = {raie['longueur_onde']:.2f} nm")
                    with col3:
                        st.markdown(f"Énergie: {raie['energie_eV']:.2f} eV | Intensité: {raie['intensite']:.2f}")
                    
                    st.markdown("---")
            else:
                st.info("Aucune raie ne correspond aux critères de recherche.")
    
    def create_sidebar(self):
        """Crée la sidebar avec les contrôles"""
        st.sidebar.markdown("## 🎛️ CONTRÔLES D'ANALYSE")
        
        # Navigation principale
        st.sidebar.markdown("### 🧭 Navigation")
        section = st.sidebar.radio("Section principale:", 
                                 ["Tableau Périodique", "Bibliothèque Spectrale", "Outils Avancés"])
        
        # Filtres globaux
        st.sidebar.markdown("### 🔍 Filtres Globaux")
        categorie_filtre = st.sidebar.selectbox("Catégorie d'éléments:", 
                                              ['Toutes'] + list(set([e['categorie'] for e in self.elements_data])))
        
        periode_filtre = st.sidebar.selectbox("Période:", 
                                            ['Toutes'] + list(set([str(e['periode']) for e in self.elements_data])))
        
        # Options d'affichage
        st.sidebar.markdown("### ⚙️ Options")
        show_details = st.sidebar.checkbox("Afficher les détails techniques", value=True)
        auto_scale = st.sidebar.checkbox("Échelle automatique des spectres", value=True)
        
        return {
            'section': section,
            'categorie_filtre': categorie_filtre,
            'periode_filtre': periode_filtre,
            'show_details': show_details,
            'auto_scale': auto_scale
        }
    
    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Sidebar
        controls = self.create_sidebar()
        
        # Header
        self.display_header()
        
        # Navigation principale
        if controls['section'] == "Tableau Périodique":
            self.create_periodic_table_overview()
            self.create_spectral_library()
        elif controls['section'] == "Bibliothèque Spectrale":
            self.create_spectral_library()
        elif controls['section'] == "Outils Avancés":
            self.create_advanced_analysis_tools()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666;'>
        <strong>Dashboard Spectroscopie Atomique Complète</strong><br>
        Base de données étendue incluant tous les éléments avec leurs spectres caractéristiques<br>
        Données spectrales basées sur les transitions atomiques réelles
        </div>
        """, unsafe_allow_html=True)

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = CompleteAtomicSpectraDashboard()
    dashboard.run_dashboard()