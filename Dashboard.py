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
    page_title="Dashboard Spectroscopie Atomique",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé CORRIGÉ
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
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
        color: #333333;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2575FC;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

class AtomicSpectraDashboard:
    def __init__(self):
        self.elements_data = self.define_elements_data()
        self.series_data = self.define_series_data()
        self.transitions_data = self.define_transitions_data()
        self.spectral_lines = self.define_spectral_lines()
        
    def define_elements_data(self):
        """Définit les données des éléments pour l'analyse spectrale"""
        return [
            {
                'symbole': 'H',
                'nom': 'Hydrogène',
                'numero_atomique': 1,
                'masse_atomique': 1.008,
                'config_electronique': '1s¹',
                'niveaux_energie': [13.6, 3.4, 1.51, 0.85, 0.54],
                'couleur_spectre': '#FF6B6B',
                'description': 'Élément le plus simple, spectre caractéristique des séries'
            },
            {
                'symbole': 'He',
                'nom': 'Hélium',
                'numero_atomique': 2,
                'masse_atomique': 4.0026,
                'config_electronique': '1s²',
                'niveaux_energie': [24.6, 4.8, 2.2, 1.3, 0.9],
                'couleur_spectre': '#4ECDC4',
                'description': 'Gaz noble, spectre complexe dû aux deux électrons'
            },
            {
                'symbole': 'Na',
                'nom': 'Sodium',
                'numero_atomique': 11,
                'masse_atomique': 22.99,
                'config_electronique': '[Ne] 3s¹',
                'niveaux_energie': [5.14, 3.03, 1.95, 1.52, 1.26],
                'couleur_spectre': '#FFE66D',
                'description': 'Doublet jaune caractéristique à 589 nm'
            },
            {
                'symbole': 'Hg',
                'nom': 'Mercure',
                'numero_atomique': 80,
                'masse_atomique': 200.59,
                'config_electronique': '[Xe] 4f¹⁴ 5d¹⁰ 6s²',
                'niveaux_energie': [10.44, 6.7, 4.89, 3.71, 2.85],
                'couleur_spectre': '#95E1D3',
                'description': 'Spectre riche avec raies intenses dans le visible et UV'
            },
            {
                'symbole': 'Ne',
                'nom': 'Néon',
                'numero_atomique': 10,
                'masse_atomique': 20.18,
                'config_electronique': '[He] 2s² 2p⁶',
                'niveaux_energie': [21.6, 5.5, 3.2, 2.1, 1.5],
                'couleur_spectre': '#FF9A76',
                'description': 'Gaz noble utilisé dans les enseignes lumineuses'
            },
            {
                'symbole': 'Ca',
                'nom': 'Calcium',
                'numero_atomique': 20,
                'masse_atomique': 40.08,
                'config_electronique': '[Ar] 4s²',
                'niveaux_energie': [6.11, 3.15, 2.52, 1.94, 1.57],
                'couleur_spectre': '#A8E6CF',
                'description': 'Raies caractéristiques en astrophysique'
            }
        ]
    
    def define_series_data(self):
        """Définit les séries spectrales principales"""
        return [
            {
                'nom': 'Lyman',
                'element': 'H',
                'niveau_final': 1,
                'domaine': 'UV',
                'longueur_onde_min': 91.2,
                'longueur_onde_max': 121.6,
                'couleur': '#9C27B0',
                'description': 'Transitions vers le niveau fondamental n=1'
            },
            {
                'nom': 'Balmer',
                'element': 'H',
                'niveau_final': 2,
                'domaine': 'Visible',
                'longueur_onde_min': 365.0,
                'longueur_onde_max': 656.3,
                'couleur': '#4CAF50',
                'description': 'Transitions vers n=2, raies visibles caractéristiques'
            },
            {
                'nom': 'Paschen',
                'element': 'H',
                'niveau_final': 3,
                'domaine': 'IR',
                'longueur_onde_min': 820.4,
                'longueur_onde_max': 1875.1,
                'couleur': '#FF9800',
                'description': 'Transitions vers n=3, domaine infrarouge'
            },
            {
                'nom': 'Brackett',
                'element': 'H',
                'niveau_final': 4,
                'domaine': 'IR',
                'longueur_onde_min': 1458.4,
                'longueur_onde_max': 4051.2,
                'couleur': '#F44336',
                'description': 'Transitions vers n=4, IR lointain'
            },
            {
                'nom': 'Pfund',
                'element': 'H',
                'niveau_final': 5,
                'domaine': 'IR',
                'longueur_onde_min': 2278.8,
                'longueur_onde_max': 7457.8,
                'couleur': '#2196F3',
                'description': 'Transitions vers n=5, IR très lointain'
            }
        ]
    
    def define_transitions_data(self):
        """Définit les transitions spectrales importantes"""
        transitions = []
        
        # Transitions pour l'hydrogène
        for n2 in range(2, 7):
            for n1 in range(1, n2):
                # Formule de Rydberg pour l'hydrogène
                rydberg = 1.09677576e7  # m⁻¹
                longueur_onde = 1 / (rydberg * (1/n1**2 - 1/n2**2)) * 1e9  # en nm
                
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
                
                transitions.append({
                    'element': 'H',
                    'serie': serie,
                    'transition': f'{n1}→{n2}',
                    'niveau_depart': n2,
                    'niveau_arrivee': n1,
                    'longueur_onde_nm': longueur_onde,
                    'energie_eV': constants.h * constants.c / (longueur_onde * 1e-9) / constants.e,
                    'intensite_relative': 1.0 / (n2 - n1)**2
                })
        
        # Transitions pour d'autres éléments
        autres_transitions = [
            {'element': 'Na', 'transition': '3p→3s', 'longueur_onde_nm': 589.0, 'energie_eV': 2.11, 'intensite_relative': 0.9, 'serie': 'Principale'},
            {'element': 'Na', 'transition': '3p→3s', 'longueur_onde_nm': 589.6, 'energie_eV': 2.10, 'intensite_relative': 0.8, 'serie': 'Principale'},
            {'element': 'Hg', 'transition': '6³P₁→6¹S₀', 'longueur_onde_nm': 253.7, 'energie_eV': 4.89, 'intensite_relative': 0.95, 'serie': 'Résonnante'},
            {'element': 'Hg', 'transition': '7³S₁→6³P₀', 'longueur_onde_nm': 404.7, 'energie_eV': 3.06, 'intensite_relative': 0.7, 'serie': 'Visible'},
            {'element': 'He', 'transition': '2¹P→1¹S', 'longueur_onde_nm': 58.4, 'energie_eV': 21.2, 'intensite_relative': 0.6, 'serie': 'Résonnante'},
            {'element': 'Ne', 'transition': '3s→2p', 'longueur_onde_nm': 640.2, 'energie_eV': 1.94, 'intensite_relative': 0.8, 'serie': 'Visible'},
            {'element': 'Ca', 'transition': '4p→4s', 'longueur_onde_nm': 422.7, 'energie_eV': 2.93, 'intensite_relative': 0.7, 'serie': 'Résonnante'}
        ]
        
        for trans in autres_transitions:
            trans['niveau_depart'] = 0  # Non défini pour simplifier
            trans['niveau_arrivee'] = 0
            
        transitions.extend(autres_transitions)
        
        return pd.DataFrame(transitions)
    
    def define_spectral_lines(self):
        """Définit les raies spectrales avec leurs intensités simulées"""
        lines = []
        
        # Génération de spectres simulés
        for element in self.elements_data:
            element_lines = self.transitions_data[
                self.transitions_data['element'] == element['symbole']
            ]
            
            for _, line in element_lines.iterrows():
                # Simulation du profil spectral (raie gaussienne)
                lambda_centre = line['longueur_onde_nm']
                intensite = line['intensite_relative']
                
                # Largeur Doppler simulée
                largeur = 0.1 + 0.05 * np.random.random()  # nm
                
                lines.append({
                    'element': element['symbole'],
                    'longueur_onde': lambda_centre,
                    'intensite': intensite,
                    'largeur': largeur,
                    'serie': line.get('serie', 'Autre'),
                    'transition': line['transition']
                })
        
        return pd.DataFrame(lines)
    
    def calculate_rydberg_formula(self, n1, n2, z=1, rydberg_constant=1.09677576e7):
        """Calcule la longueur d'onde avec la formule de Rydberg"""
        return 1 / (rydberg_constant * z**2 * (1/n1**2 - 1/n2**2)) * 1e9  # nm
    
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">🔬 Dashboard Spectroscopie Atomique</h1>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("**<span style='color: #333333'>Analyse des spectres de classification atomique et transitions électroniques</span>", 
                       unsafe_allow_html=True)
        
        current_time = pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')
        st.sidebar.markdown(f"**🕐 Session active: {current_time}**")
    
    def display_theory_introduction(self):
        """Affiche la section théorie et introduction"""
        st.markdown('<h3 class="section-header">📚 THÉORIE DES SPECTRES ATOMIQUES</h3>', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div class="theory-box">
            <h4 style="color: #333333;">🎯 Principes Fondamentaux</h4>
            
            <span style="color: #333333;">
            <strong>Spectroscopie atomique</strong> : Étude des spectres électromagnétiques émis ou absorbés par les atomes.<br><br>
            
            <strong>Loi de Rydberg-Ritz</strong> :<br>
            <code>1/λ = R_H * Z² * (1/n₁² - 1/n₂²)</code><br><br>
            
            Où :<br>
            - λ : Longueur d'onde (m)<br>
            - R_H : Constante de Rydberg (1.097 × 10⁷ m⁻¹)<br>
            - Z : Numéro atomique<br>
            - n₁, n₂ : Nombres quantiques principaux (n₂ > n₁)<br><br>
            
            <strong>Séries spectrales de l'hydrogène</strong> :<br>
            - <strong>Lyman</strong> (n₁=1) : Ultraviolet<br>
            - <strong>Balmer</strong> (n₁=2) : Visible<br>
            - <strong>Paschen</strong> (n₁=3) : Infrarouge<br>
            - <strong>Brackett</strong> (n₁=4) : IR lointain<br>
            - <strong>Pfund</strong> (n₁=5) : IR très lointain
            </span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Constantes physiques
            st.markdown("""
            <div class="theory-box">
            <h4 style="color: #333333;">⚛️ Constantes Physiques</h4>
            
            <span style="color: #333333;">
            <strong>Constante de Rydberg</strong><br>
            R∞ = 1.0973731568160 × 10⁷ m⁻¹<br><br>
            
            <strong>Constante de Planck</strong><br>
            h = 6.62607015 × 10⁻³⁴ J·s<br><br>
            
            <strong>Vitesse de la lumière</strong><br>
            c = 2.99792458 × 10⁸ m/s<br><br>
            
            <strong>Charge élémentaire</strong><br>
            e = 1.602176634 × 10⁻¹⁹ C<br><br>
            
            <strong>Énergie de Rydberg</strong><br>
            E_R = 13.605693 eV
            </span>
            </div>
            """, unsafe_allow_html=True)
    
    def create_spectral_calculator(self):
        """Crée un calculateur spectral interactif"""
        st.markdown('<h3 class="section-header">🧮 CALCULATEUR SPECTRAL INTERACTIF</h3>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            element_calc = st.selectbox("Élément:", 
                                      [e['symbole'] for e in self.elements_data])
            z = next(e['numero_atomique'] for e in self.elements_data if e['symbole'] == element_calc)
        
        with col2:
            n1 = st.number_input("Niveau quantique initial n₁:", 
                               min_value=1, max_value=10, value=2)
            n2 = st.number_input("Niveau quantique final n₂:", 
                               min_value=n1+1, max_value=20, value=3)
        
        with col3:
            rydberg_custom = st.number_input("Constante de Rydberg (×10⁷ m⁻¹):", 
                                           value=1.09678, format="%.5f")
        
        # Calcul
        lambda_nm = self.calculate_rydberg_formula(n1, n2, z, rydberg_custom * 1e7)
        energie_ev = constants.h * constants.c / (lambda_nm * 1e-9) / constants.e
        frequence = constants.c / (lambda_nm * 1e-9)
        
        # Affichage des résultats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Longueur d'onde", f"{lambda_nm:.2f} nm")
        
        with col2:
            st.metric("Énergie de transition", f"{energie_ev:.3f} eV")
        
        with col3:
            st.metric("Fréquence", f"{frequence/1e12:.2f} THz")
        
        with col4:
            domaine = "UV" if lambda_nm < 400 else "Visible" if lambda_nm < 700 else "IR"
            st.metric("Domaine spectral", domaine)
        
        # Graphique de la transition
        fig = go.Figure()
        
        # Niveaux d'énergie
        niveaux = [13.6 / (n**2) for n in range(1, 7)]
        fig.add_trace(go.Scatter(
            x=[0, 1], y=[niveaux[n1-1], niveaux[n1-1]],
            mode='lines',
            line=dict(color='blue', width=3),
            name=f'n={n1}'
        ))
        fig.add_trace(go.Scatter(
            x=[0, 1], y=[niveaux[n2-1], niveaux[n2-1]],
            mode='lines',
            line=dict(color='red', width=3),
            name=f'n={n2}'
        ))
        
        # Transition
        fig.add_trace(go.Scatter(
            x=[0.5, 0.5], y=[niveaux[n2-1], niveaux[n1-1]],
            mode='lines+markers',
            line=dict(color='green', width=4, dash='dash'),
            marker=dict(size=10),
            name=f'Transition {n2}→{n1}'
        ))
        
        fig.update_layout(
            title=f"Diagramme des niveaux d'énergie - Transition {n2}→{n1}",
            xaxis=dict(showticklabels=False),
            yaxis=dict(title="Énergie (eV)", autorange='reversed'),
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_hydrogen_spectrum_analysis(self):
        """Analyse détaillée du spectre de l'hydrogène"""
        st.markdown('<h3 class="section-header">⚛️ SPECTRE DE L\'HYDROGÈNE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["Séries Spectrales", "Raies Caractéristiques", "Spectre Simulé", "Applications"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Graphique des séries spectrales
                fig = go.Figure()
                
                for serie in self.series_data:
                    transitions_serie = self.transitions_data[
                        (self.transitions_data['element'] == 'H') & 
                        (self.transitions_data['serie'] == serie['nom'])
                    ].sort_values('longueur_onde_nm')
                    
                    fig.add_trace(go.Scatter(
                        x=transitions_serie['longueur_onde_nm'],
                        y=transitions_serie['intensite_relative'],
                        mode='lines+markers',
                        name=serie['nom'],
                        line=dict(color=serie['couleur'], width=3),
                        marker=dict(size=8)
                    ))
                
                fig.update_layout(
                    title="Séries spectrales de l'atome d'hydrogène",
                    xaxis=dict(title="Longueur d'onde (nm)"),
                    yaxis=dict(title="Intensité relative"),
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Affichage des séries
                for serie in self.series_data:
                    st.markdown(f"""
                    <div class="series-card">
                    <h4 style="color: #333333;">📊 Série {serie['nom']}</h4>
                    <span style="color: #333333;">
                    <strong>Domaine:</strong> {serie['domaine']}<br>
                    <strong>Niveau final:</strong> n={serie['niveau_final']}<br>
                    <strong>Plage de longueurs d'onde:</strong> {serie['longueur_onde_min']} - {serie['longueur_onde_max']} nm<br>
                    <strong>Description:</strong> {serie['description']}
                    </span>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab2:
            # Raies caractéristiques de Balmer
            raies_balmer = self.transitions_data[
                (self.transitions_data['element'] == 'H') & 
                (self.transitions_data['serie'] == 'Balmer')
            ].sort_values('longueur_onde_nm')
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Raies de la série de Balmer")
                for _, raie in raies_balmer.iterrows():
                    couleur_texte = "wavelength-visible"
                    st.markdown(f"""
                    <div class="transition-card {couleur_texte}">
                    <strong style="color: #333333;">Raie {raie['transition']}</strong><br>
                    <span style="color: #333333;">
                    λ = {raie['longueur_onde_nm']:.1f} nm<br>
                    Énergie = {raie['energie_eV']:.3f} eV
                    </span>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                # Graphique des raies de Balmer
                fig = px.bar(raies_balmer, 
                            x='transition', 
                            y='longueur_onde_nm',
                            color='longueur_onde_nm',
                            title="Raies de la série de Balmer - Longueurs d'onde",
                            color_continuous_scale='Viridis')
                fig.update_layout(xaxis_title="Transition", yaxis_title="Longueur d'onde (nm)")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Spectre simulé de l'hydrogène
            st.subheader("Spectre simulé de l'atome d'hydrogène")
            
            # Génération du spectre simulé
            lambda_range = np.linspace(100, 1000, 2000)
            spectre_total = np.zeros_like(lambda_range)
            
            raies_h = self.spectral_lines[self.spectral_lines['element'] == 'H']
            
            for _, raie in raies_h.iterrows():
                # Profil gaussien pour chaque raie
                spectre_raie = raie['intensite'] * np.exp(-0.5 * ((lambda_range - raie['longueur_onde']) / raie['largeur'])**2)
                spectre_total += spectre_raie
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=lambda_range, y=spectre_total,
                mode='lines',
                line=dict(color='#FF6B6B', width=2),
                name='Spectre H'
            ))
            
            # Ajout des raies identifiées
            for _, raie in raies_h[raies_h['longueur_onde'] <= 1000].iterrows():
                fig.add_trace(go.Scatter(
                    x=[raie['longueur_onde'], raie['longueur_onde']],
                    y=[0, raie['intensite']],
                    mode='lines',
                    line=dict(color='black', width=1, dash='dash'),
                    showlegend=False
                ))
            
            fig.update_layout(
                title="Spectre d'émission simulé de l'hydrogène",
                xaxis=dict(title="Longueur d'onde (nm)"),
                yaxis=dict(title="Intensité relative"),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            st.subheader("Applications et Importance")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="theory-box">
                <h4 style="color: #333333;">🔭 Astrophysique</h4>
                
                <span style="color: #333333;">
                <strong>Classification stellaire</strong> :<br>
                Les raies de Balmer permettent de classifier les étoiles selon leur type spectral.<br><br>
                
                <strong>Cosmologie</strong> :<br>
                Décalage vers le rouge (redshift) des raies de l'hydrogène pour mesurer les distances.<br><br>
                
                <strong>Nébuleuses</strong> :<br>
                Raie Hα à 656.3 nm caractéristique des régions de formation d'étoiles.
                </span>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="theory-box">
                <h4 style="color: #333333;">🧪 Physique Atomique</h4>
                
                <span style="color: #333333;">
                <strong>Vérification de la mécanique quantique</strong> :<br>
                Le spectre de l'hydrogène a validé le modèle de Bohr.<br><br>
                
                <strong>Constantes fondamentales</strong> :<br>
                Détermination précise de la constante de Rydberg.<br><br>
                
                <strong>Spectroscopie de précision</strong> :<br>
                Tests des théories de l'électrodynamique quantique.
                </span>
                </div>
                """, unsafe_allow_html=True)
    
    def create_elements_comparison(self):
        """Comparaison des spectres de différents éléments"""
        st.markdown('<h3 class="section-header">⚡ COMPARAISON DES ÉLÉMENTS</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Spectres Multi-éléments", "Caractéristiques", "Analyse Quantitative"])
        
        with tab1:
            # Sélection des éléments à comparer
            elements_selectionnes = st.multiselect(
                "Sélectionnez les éléments à comparer:",
                [e['symbole'] for e in self.elements_data],
                default=['H', 'Na', 'Hg']
            )
            
            if elements_selectionnes:
                fig = go.Figure()
                
                for element_symb in elements_selectionnes:
                    element_data = next(e for e in self.elements_data if e['symbole'] == element_symb)
                    raies_element = self.spectral_lines[self.spectral_lines['element'] == element_symb]
                    
                    # Spectre simulé pour l'élément
                    lambda_range = np.linspace(200, 800, 1500)
                    spectre_element = np.zeros_like(lambda_range)
                    
                    for _, raie in raies_element.iterrows():
                        if 200 <= raie['longueur_onde'] <= 800:
                            spectre_raie = raie['intensite'] * np.exp(-0.5 * ((lambda_range - raie['longueur_onde']) / raie['largeur'])**2)
                            spectre_element += spectre_raie
                    
                    fig.add_trace(go.Scatter(
                        x=lambda_range, y=spectre_element,
                        mode='lines',
                        name=f'{element_symb} - {element_data["nom"]}',
                        line=dict(width=2)
                    ))
                
                fig.update_layout(
                    title="Comparaison des spectres d'émission",
                    xaxis=dict(title="Longueur d'onde (nm)"),
                    yaxis=dict(title="Intensité relative"),
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Tableau comparatif des éléments
            st.subheader("Caractéristiques des Éléments")
            
            for element in self.elements_data:
                if element['symbole'] in elements_selectionnes:
                    raies_element = self.transitions_data[
                        self.transitions_data['element'] == element['symbole']
                    ]
                    
                    col1, col2, col3 = st.columns([1, 2, 2])
                    
                    with col1:
                        st.markdown(f"""
                        <div class="element-card">
                        <h4 style="color: #333333;">{element['symbole']} - {element['nom']}</h4>
                        <span style="color: #333333;">
                        <strong>Z:</strong> {element['numero_atomique']}<br>
                        <strong>Masse:</strong> {element['masse_atomique']} u<br>
                        <strong>Configuration:</strong> {element['config_electronique']}
                        </span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        # Raies principales
                        raies_principales = raies_element.nlargest(3, 'intensite_relative')
                        st.markdown("**Raies principales:**")
                        for _, raie in raies_principales.iterrows():
                            domaine = "UV" if raie['longueur_onde_nm'] < 400 else "Visible" if raie['longueur_onde_nm'] < 700 else "IR"
                            st.write(f"- {raie['transition']}: {raie['longueur_onde_nm']:.1f} nm ({domaine})")
                    
                    with col3:
                        # Graphique des niveaux d'énergie
                        if len(element['niveaux_energie']) > 0:
                            fig = px.bar(
                                x=['n1', 'n2', 'n3', 'n4', 'n5'][:len(element['niveaux_energie'])],
                                y=element['niveaux_energie'],
                                title=f"Niveaux d'énergie - {element['symbole']}",
                                color=element['niveaux_energie'],
                                color_continuous_scale='Viridis'
                            )
                            fig.update_layout(xaxis_title="Niveau", yaxis_title="Énergie (eV)", height=200)
                            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("Analyse Quantitative des Spectres")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Statistiques des raies spectrales
                stats_raies = self.transitions_data.groupby('element').agg({
                    'longueur_onde_nm': ['count', 'min', 'max', 'mean'],
                    'energie_eV': ['min', 'max', 'mean']
                }).round(2)
                
                # Style le DataFrame pour une meilleure lisibilité
                st.dataframe(stats_raies.style.set_properties(**{
                    'background-color': '#f8f9fa',
                    'color': '#333333',
                    'border-color': '#dee2e6'
                }), use_container_width=True)
            
            with col2:
                # Distribution des longueurs d'onde
                fig = px.box(self.transitions_data, 
                            x='element', 
                            y='longueur_onde_nm',
                            title="Distribution des longueurs d'onde par élément",
                            color='element')
                st.plotly_chart(fig, use_container_width=True)
    
    def create_advanced_analysis(self):
        """Analyse avancée et outils spécialisés"""
        st.markdown('<h3 class="section-header">🔍 ANALYSE AVANCÉE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Modèle de Bohr", "Effets Spectraux", "Simulateur Quantique"])
        
        with tab1:
            st.subheader("Modèle Atomique de Bohr")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="theory-box">
                <h4 style="color: #333333;">🎯 Postulats de Bohr</h4>
                
                <span style="color: #333333;">
                1. <strong>Électrons en orbite stable</strong> :<br>
                Les électrons se déplacent sur des orbites circulaires sans rayonnement.<br><br>
                
                2. <strong>Quantification du moment angulaire</strong> :<br>
                L = nħ où n = 1, 2, 3...<br><br>
                
                3. <strong>Transitions quantiques</strong> :<br>
                Émission/absorption de photons lors des sauts entre orbites.<br><br>
                
                <strong>Énergie des niveaux</strong> :<br>
                Eₙ = - (mₑ e⁴) / (8ε₀² h²) × Z²/n²
                </span>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Diagramme des orbites de Bohr
                fig = go.Figure()
                
                # Orbites simulées
                for n in range(1, 6):
                    theta = np.linspace(0, 2*np.pi, 100)
                    r = n**2  # Rayon proportionnel à n²
                    x = r * np.cos(theta)
                    y = r * np.sin(theta)
                    
                    fig.add_trace(go.Scatter(
                        x=x, y=y,
                        mode='lines',
                        name=f'n={n}',
                        line=dict(width=2)
                    ))
                
                fig.update_layout(
                    title="Orbites du modèle de Bohr (échelle relative)",
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    showlegend=True,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.subheader("Effets Spectraux et Structure Fine")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="theory-box">
                <h4 style="color: #333333;">🌀 Structure Fine</h4>
                
                <span style="color: #333333;">
                <strong>Couplage spin-orbite</strong> :<br>
                Interaction entre le spin de l'électron et son mouvement orbital.<br><br>
                
                <strong>Constante de structure fine</strong> :<br>
                α = e²/(4πε₀ħc) ≈ 1/137<br><br>
                
                <strong>Déplacement des raies</strong> :<br>
                Séparation en composantes dues au moment angulaire total j = l ± 1/2<br><br>
                
                <strong>Exemple</strong> :<br>
                Doublet du sodium à 589.0 et 589.6 nm
                </span>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="theory-box">
                <h4 style="color: #333333;">⚡ Effet Stark et Zeeman</h4>
                
                <span style="color: #333333;">
                <strong>Effet Zeeman</strong> :<br>
                Dédoublement des raies sous champ magnétique.<br><br>
                
                <strong>Effet Stark</strong> :<br>
                Dédoublement sous champ électrique.<br><br>
                
                <strong>Applications</strong> :<br>
                - Magnétisme stellaire (taches solaires)<br>
                - Physique des plasmas<br>
                - Tests de symétrie
                </span>
                </div>
                """, unsafe_allow_html=True)
                
                # Simulation d'effet Zeeman
                st.subheader("Simulation d'effet Zeeman")
                champ_magnetique = st.slider("Champ magnétique (T):", 0.0, 5.0, 1.0)
                separation = champ_magnetique * 0.1  # Séparation simulée
                
                lambda_centre = 500  # nm
                lambda_composantes = [lambda_centre - separation, lambda_centre, lambda_centre + separation]
                intensites = [0.5, 1.0, 0.5]
                
                fig = px.bar(x=lambda_composantes, y=intensites,
                            title=f"Effet Zeeman simulé - B = {champ_magnetique} T")
                fig.update_layout(xaxis_title="Longueur d'onde (nm)", yaxis_title="Intensité relative")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("Simulateur de Transitions Quantiques")
            
            col1, col2 = st.columns(2)
            
            with col1:
                n_initial = st.selectbox("Niveau initial:", range(1, 11), index=2)
                l_initial = st.selectbox("Nombre quantique orbital initial:", range(0, n_initial))
                n_final = st.selectbox("Niveau final:", range(1, n_initial), index=0)
                l_final = st.selectbox("Nombre quantique orbital final:", range(0, n_final))
            
            with col2:
                # Règles de sélection
                delta_l = abs(l_initial - l_final)
                transition_permise = delta_l == 1
                
                st.markdown(f"""
                <div class="theory-box">
                <h4 style="color: #333333;">📋 Règles de Sélection</h4>
                
                <span style="color: #333333;">
                <strong>Δn</strong> : Quelconque<br>
                <strong>Δl</strong> = ±1 : {'✅ Permise' if transition_permise else '❌ Interdite'}<br>
                <strong>Δm</strong> = 0, ±1<br><br>
                
                <strong>Transition</strong> :<br>
                {n_initial}{self.get_orbital_letter(l_initial)} → {n_final}{self.get_orbital_letter(l_final)}
                </span>
                </div>
                """, unsafe_allow_html=True)
            
            if transition_permise:
                # Calcul de la longueur d'onde approximative
                energie_approx = 13.6 * (1/n_final**2 - 1/n_initial**2)
                lambda_approx = 1240 / energie_approx if energie_approx > 0 else 0
                
                st.metric("Longueur d'onde approximative", f"{lambda_approx:.1f} nm")
                st.metric("Énergie de transition", f"{energie_approx:.3f} eV")
    
    def get_orbital_letter(self, l):
        """Convertit le nombre quantique orbital en lettre"""
        letters = ['s', 'p', 'd', 'f', 'g', 'h', 'i']
        return letters[l] if l < len(letters) else f'({l})'
    
    def create_sidebar(self):
        """Crée la sidebar avec les contrôles"""
        st.sidebar.markdown("## 🎛️ CONTRÔLES D'ANALYSE")
        
        # Sélection du domaine spectral
        st.sidebar.markdown("### 🌈 Domaine Spectral")
        domaine = st.sidebar.selectbox("Filtrer par domaine:", 
                                     ['Tous', 'UV', 'Visible', 'IR'])
        
        # Sélection de l'élément principal
        st.sidebar.markdown("### ⚛️ Élément Principal")
        element_principal = st.sidebar.selectbox("Élément à analyser:", 
                                               [e['symbole'] for e in self.elements_data])
        
        # Options d'affichage
        st.sidebar.markdown("### ⚙️ Options d'Affichage")
        show_advanced = st.sidebar.checkbox("Afficher l'analyse avancée", value=False)
        show_simulations = st.sidebar.checkbox("Afficher les simulations", value=True)
        
        # Constantes physiques ajustables
        st.sidebar.markdown("### 🔧 Constantes Physiques")
        rydberg_value = st.sidebar.number_input("Constante de Rydberg (×10⁷ m⁻¹):", 
                                              value=1.09678, format="%.5f")
        
        return {
            'domaine': domaine,
            'element_principal': element_principal,
            'show_advanced': show_advanced,
            'show_simulations': show_simulations,
            'rydberg_value': rydberg_value
        }
    
    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Sidebar
        controls = self.create_sidebar()
        
        # Header
        self.display_header()
        
        # Navigation par onglets
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📚 Théorie", 
            "🧮 Calculateur", 
            "⚛️ Hydrogène", 
            "⚡ Éléments", 
            "🔍 Avancé"
        ])
        
        with tab1:
            self.display_theory_introduction()
        
        with tab2:
            self.create_spectral_calculator()
        
        with tab3:
            self.create_hydrogen_spectrum_analysis()
        
        with tab4:
            self.create_elements_comparison()
        
        with tab5:
            self.create_advanced_analysis()

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = AtomicSpectraDashboard()
    dashboard.run_dashboard()