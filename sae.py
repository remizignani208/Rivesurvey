# Setup -------------------------------------------------------------------------------------------------------------------------------------------------------


### Dépendances
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from PIL import Image
import random
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt



# style -------------------------------------------------------------------------------------------------------------------------------------------------------



# Setup du style du tout le site
st.set_page_config(
    page_title="Comparaison de Villes",
    layout="wide",  
    initial_sidebar_state="expanded",
)

if 'page_actuelle' not in st.session_state:
    st.session_state['page_actuelle'] = 'accueil'


# Sidebar
# Chargez une image depuis un fichier
image = Image.open("style/images/logo.jpg")

# Affichez l'image dans la barre latérale
st.sidebar.image(image, use_column_width=True)

# Style
st.markdown("""
<style>

body {
    background-color: #E02C40;
}
            
.sidebar .sidebar-content {
    background-color: #F9F9F9 ;
}

/* Personnalise les boutons radio pour la navigation */
.stRadio > div {
    background-color: #F9F9F9 ;
    border-radius: 20px;
    color: white;
}

/* Change l'apparence du bouton lorsqu'il est sélectionné */
.css-1k0ckh2[aria-checked="true"] {
    background-color: #2C5F2D !important;
    color: white !important;
}

/* Personnalise l'apparence des boutons */
.stButton > button {
    border: 10px solid #EEAAAA ;
    border-radius: 20px;
    color: #EEAAAA ;
}

</style>
""", unsafe_allow_html=True)



# Préparations des données, listes, fonctions utilisées dans les pages du site ----------------------------------------------------------------------------------------------------------------------------



# Citations pour la citation du jour
citations = [
    "« La meilleure façon de prédire l'avenir est de le créer. » - Peter Drucker",
    "« L'innovation distingue le leader du suiveur. » - Steve Jobs",
    "« Les données sont un précieux bien qui ne se déprécie jamais. » - Inconnu",
    "« Le bonheur n'est pas quelque chose de prêt à l'emploi. Il vient de vos propres actions. » - Dalaï-Lama",
    "« Pour être heureux, il faut croire au possible. » - Hellen Keller",
    "« Le bonheur n'est pas dans la recherche de la perfection, mais dans la tolérance de l'imperfection. » - Yacine Bellik",
    "« Le bonheur, c'est de continuer à désirer ce que l'on possède. » - Saint Augustin",
    "« Le vrai bonheur ne dépend d'aucun être, d'aucun objet extérieur. Il ne dépend que de nous... » - Dalaï-Lama",
    "« La joie de regarder et de comprendre est le plus beau cadeau de la nature. » - Albert Einstein",
    "« Le secret du bonheur est la liberté... Et le secret de la liberté est le courage. » - Thucydide",
    "« Le bonheur est parfois caché dans l'inconnu. » - Victor Hugo",
    "« Le bonheur ne se réduit pas au plaisir, à l'absence de mal, mais il réside dans l'accomplissement. » - Aristote",
    "« Chaque minute de dépression vous prive de soixante secondes de bonheur. » - Ralph Waldo Emerson"
]

# Charger les fichiers de données
villes = pd.read_csv('donnees/cities.csv')
donnees_chiffrees = pd.read_csv('donnees/donnees_chiffrees.csv')
pop = pd.merge(left=villes, right=donnees_chiffrees, how='left', left_on='insee_code', right_on='insee_code')
pop = pop[pop['Population_totale'] > 4000]
insee_codes_filtered = pop['insee_code']
villes = villes[villes['insee_code'].isin(insee_codes_filtered)]

#Definition base Education
education_df = pd.read_csv('donnees/fr-en-annuaire-education.csv', sep=";", encoding='ISO-8859-1')
#Definition merge Ville et Education
Villes_Education = pd.merge(left=villes, right=education_df, how='left', left_on='insee_code', right_on='Code_commune')

culture_df = pd.read_csv('donnees/base-des-lieux-et-des-equipements-culturels.csv', sep=";")
# Données de la culture
Villes_Culture = pd.merge(villes, culture_df, left_on='insee_code', right_on='code_insee', how='left')

#données logement
logement_df = pd.read_csv('donnees/donnees_logement.csv', sep=",")
# Jointure
Villes_logement = pd.merge(villes, logement_df, left_on='insee_code', right_on='code_insee', how='left')
# Pour donnees de logement avancees
logement_avancees = pd.read_csv('donnees/donnees_logement_avancees.csv', sep=",")
# Jointure
Villes_logement_avancees = pd.merge(villes, logement_avancees, left_on='insee_code', right_on='code_insee', how='right')

#données transports
transports_df = pd.read_csv('donnees/Villes_transports.csv', sep=",")

# données crime
crime_df = pd.read_csv("donnees/Crime.csv", encoding="ISO-8859-1", sep=",", dtype={'Nom_de_la_colonne': str})
# Données de l'emploi
df = pd.read_csv('donnees/ci.csv', sep=';')
dfemploi = pd.read_csv('donnees/baseemploi.csv', sep=';')


# Convertir les colonnes sauf 'CODGEO' en int et 'CODGEO' en str
for column in dfemploi.columns:
    if column != 'CODGEO':
        dfemploi[column] = dfemploi[column].astype(int)
    else:
        dfemploi[column] = dfemploi[column].astype(str)
columns_to_convert = [col for col in df.columns if col not in ['longitude', 'latitude']]

# Convertir les colonnes sélectionnées en STR
for column in columns_to_convert:
    df[column] = df[column].astype(str)
# Effectuer la jointure des tables
donnees_emploi = pd.merge(df, dfemploi, left_on='insee_code', right_on='CODGEO', how='inner')

nouveaux_noms_colonnes = ['insee_code', 'city_code', 'zip_code', 'label', 'latitude', 'longitude', 'department_name',
                          'department_number', 'region_name', 'region_geojson_name', 'CODGEO', 'population_15-64',
                          'population_homme_15-64', 'population_femme_15-64', 'population_active_15-64',
                          'population_active_homme_15-64', 'population_active_femme_15-64', 'chomeurs_15-64',
                          'actifs_15-64', 'actifs_agriculteurs', 'actifs_artisants_commercants', 'actifs_cadres',
                          'actifs_prof_intermediare', 'actifs_employes', 'actifs_ouvriers', 'chomeurs', 'chomeuse']

donnees_emploi.columns = nouveaux_noms_colonnes

# Liste des colonnes à supprimer
colonnes_a_supprimer = ['zip_code', 'latitude', 'longitude', 'department_name',
                        'department_number', 'region_name', 'region_geojson_name', 'CODGEO']

# Supprimer les colonnes spécifiées
donnees_emploi = donnees_emploi.drop(columns=colonnes_a_supprimer)

dfsante = pd.read_csv('donnees/sante.csv', sep=';')
dfsante['code_postal'] = dfsante['Commune'].str.split().str[0]

for column in df.columns:
    if column == 'zip_code':
            df[column] = df[column].astype(int)
for column in dfsante.columns:
    if column == 'code_postal':
            dfsante[column] = dfsante[column].astype(int)
            
resultsante = pd.merge(df, dfsante, left_on='zip_code', right_on='code_postal', how='inner')


colonnes_a_supprimer = ['label', 'zip_code', 'latitude', 'longitude', 'department_name',
                        'department_number', 'region_name', 'region_geojson_name', 'A','Z','Unnamed: 5','Commune' ]

resultsante = resultsante.drop(columns=colonnes_a_supprimer)




# Mettre des noms plus lisibles
villes = villes.rename(columns={
    'zip_code': 'Code postal',
    'label': 'Libellé',
    'latitude': 'Latitude',
    'longitude': 'Longitude',
    'department_name': 'Nom du département',
    'department_number': 'Numéro du département',
    'region_name': 'Nom de la région',
    'region_geojson_name': 'Nom de la région (GeoJSON)'
})

# Pour la map
def add_marker_group(m, ville_selection, df):
    for city_code in ville_selection:
        city_row = df[df['city_code'] == city_code]
        lon = city_row['Longitude'].iloc[0]
        lat = city_row['Latitude'].iloc[0]
        name = city_row['Libellé'].iloc[0]
        
        if pd.notnull(lon) and pd.notnull(lat):
            try:
                lon = float(lon)
                lat = float(lat)
                folium.Marker(
                    location=[lat, lon],
                    popup=name,
                    icon=folium.Icon(color="red", prefix="fa"),
                ).add_to(m)
            except ValueError:
                print(f"Error converting latitude/longitude for city: {name}")
                st.error(f"Erreur lors de la conversion des coordonnées pour la ville: {name}")
        else:
            print(f"Latitude or longitude missing for city: {name}")
            st.error(f"Coordonnées géographiques manquantes pour la ville: {name}")

    return m
# Afficher la map
def display_map(ville_selection, df):
    st.markdown("Carte de visualisation des emplacements des villes de France.")
    st.write("\n")
    st.write("\n")
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)
    m = add_marker_group(m, ville_selection, df)
   
    return m

# Histogramme
def tracer_histogramme(ville_selection, Villes_Logement_select_av, data_column, title):
    plt.figure(figsize=(10, 6))
    for ville_code in ville_selection:
        data = Villes_Logement_select_av[Villes_Logement_select_av['city_code'] == ville_code]
        plt.plot(data['Annee'], data[data_column], marker='o', label=f'{ville_code}')
    
    plt.xlabel('Année')
    plt.ylabel(title)
    plt.xlim(2010, 2025)  
    plt.legend()
    st.pyplot(plt)
    plt.clf()


# préparer les données transports par année :
def preparer_donnees_longues(df, colonnes_annees, nom_variable):
    """
    Transforme les colonnes spécifiées en lignes.
    
    Args:
        df (pd.DataFrame): DataFrame original.
        colonnes_annees (dict): Dictionnaire avec le format {'nom_colonne_année': 'année'}.
        nom_variable (str): Nom de la variable pour la colonne de valeur (ex: 'total_voyageurs' ou 'satisfaction').
    
    Returns:
        pd.DataFrame: DataFrame transformé.
    """
    # Sélectionne les colonnes non-année et les transforme en long format.
    df_long = pd.melt(df, id_vars=['city_code', 'label', 'department_name', 'nom_gare'],
                      value_vars=colonnes_annees.keys(),
                      var_name='Annee',
                      value_name=nom_variable)
    
    # Remplace les noms des colonnes année par les années réelles.
    df_long['Annee'] = df_long['Annee'].map(colonnes_annees)
    
    return df_long

# fonction pour les transports
def find_max_voyageurs_index(df):
    if df.empty or df['total_voyageurs_2022'].isnull().all():
        return None
    else:
        return df['total_voyageurs_2022'].idxmax()



# Les pages importantes -------------------------------------------------------------------------------------------------------------------------------------------------------



# Page : Bienvenue
def page_accueil():

    st.write("""
         <style>
         :root {
             --primary-color: #EA4454;
             --background-color: #EA4454;
             --secondary-background-color: #EA4454;
             --text-color: #000000;
             --font: "Helvetica Neue", Helvetica, Arial, sans-serif;
         }
         </style>
         """, unsafe_allow_html=True)
    # Contenu de la page d'accueil
    st.title("Bienvenue sur notre site de comparaison de villes !")
    st.write("---")
    st.write(f"### Citation du jour\n{random.choice(citations)}")
    st.write("### À quoi sert ce site ?")
    # Utilisation de containers pour une structure plus flexible
    with st.container():
        col1, col2 = st.columns([2, 1])  # Crée deux colonnes avec des largeurs différentes

        with col1:  # Première colonne pour le texte principal
            st.write("""
                     Ce site vous permet de comparer différentes données socio-économiques 
                     et éducatives de différentes villes.
                     """)
            st.write("Allez choisir les deux villes qui vous intéressent !")

        with col2:  # Seconde colonne pour un élément visuel ou supplémentaire
            st.info("Indice : Commencez par sélectionner les villes dans le menu 'comparaison des villes' à gauche.")

    # Utilisation d'un expander pour des informations supplémentaires ou des instructions
    with st.expander("En savoir plus"):
        st.write("""
                 Bienvenue sur notre plateforme dédiée à la comparaison de villes en France, un outil conçu pour vous aider à explorer et comparer une variété de données socio-économiques et éducatives à travers différentes villes. Que vous envisagiez de déménager, de voyager, ou simplement d'en apprendre davantage sur diverses localités françaises, notre site offre une fenêtre unique sur les caractéristiques qui rendent chaque ville unique.
                 
                 Comment ça marche ?

                 Notre plateforme est alimentée par des données précises sur les villes françaises, couvrant des aspects variés tels que la démographie, l'économie, l'éducation, le logement, et bien plus encore. En sélectionnant deux villes pour la comparaison, vous obtiendrez une analyse comparative détaillée qui couvre :

                 Données Démographiques : Obtenez un aperçu de la population, de la structure d'âge, et d'autres statistiques clés. \n
                 Économie et Emploi : Comparez le taux de chômage, les secteurs d'activité principaux, et d'autres indicateurs économiques. \n
                 Éducation : Examinez le niveau d'accès à l'éducation, les performances des établissements scolaires, et plus encore. \n
                 Logement : Découvrez des informations sur le marché immobilier, le coût de la vie, et les types de logements disponibles. \n
                 Santé et Services : Comparez l'accès aux soins de santé et à d'autres services essentiels. \n
                 Transports : Explorez la facilité de déplacement, les options de transport public, et la connectivité des villes. \n
                 Sécurité : Comparez les statistiques de sécurité, y compris les taux de criminalité et la présence de services de police. \n
                 Loisirs et Culture : Découvrez les activités de loisirs, les événements culturels, et les attractions touristiques. \n

                 Fonctionnalités Interactives :

                 Notre site intègre des cartes interactives permettant de visualiser géographiquement les villes sélectionnées, enrichissant votre compréhension de leur emplacement et proximité. De plus, grâce à une interface intuitive, naviguez facilement entre différentes sections pour une expérience utilisateur optimale.

                 Engagement envers la Qualité de Données :

                 Nous nous engageons à fournir des informations actualisées et précises, en collaborant avec des sources de données fiables et en mettant régulièrement à jour notre base de données pour refléter les changements les plus récents.

                 Pourquoi Nous Utiliser ?

                 Que vous soyez un futur résident cherchant à prendre une décision éclairée sur votre prochain lieu de vie, un chercheur, un étudiant, ou simplement un curieux, notre plateforme offre une perspective enrichissante sur les villes de France. En mettant à votre disposition une mine d'informations, nous espérons faciliter vos recherches et soutenir vos décisions avec des données de qualité.

                 Nous vous invitons à explorer, comparer, et découvrir ce que chaque ville a à offrir. Commencez votre voyage dès maintenant en sélectionnant les villes qui vous intéressent et plongez dans l'univers unique de chacune. Merci de choisir notre plateforme pour accompagner votre exploration urbaine !
                 """)

    # Ajout d'un espace supplémentaire en bas de la page
    st.write("---")
    st.caption("Merci de visiter notre site de comparaison de villes !")

# Page: Comparaison
def compare_villes():
    st.title("Choisissez deux villes à comparer !")
    st.write("Vous pourrez ensuite explorer les informations de chaque ville !")
    ville_selection = st.multiselect('Sélectionnez les villes:', villes['city_code'].unique())
    st.session_state['ville_selection'] = ville_selection
    
    if len(ville_selection) == 2:
        ville1, ville2 = ville_selection
        
        st.title(f"Comparaison entre {ville1} et {ville2}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("## Carte d'identité de ", ville1, " :")
            st.write("\n")
            ville1_data = villes[villes['city_code'] == ville1].squeeze()
            if isinstance(ville1_data, pd.DataFrame):
                if len(ville1_data['Libellé']) > 1:
                    ville1_data = ville1_data.drop_duplicates(subset=['insee_code'], keep='first')
                st.write(ville1_data[['insee_code', 'Libellé', 'Latitude', 'Longitude', 'Nom du département', 'Numéro du département', 'Nom de la région']].T)
                st.write("source : data.gouv")
            elif isinstance(ville1_data, pd.Series):
                ville1_data_df = ville1_data.to_frame().T
                st.write(ville1_data_df[['insee_code', 'Libellé', 'Latitude', 'Longitude', 'Nom du département', 'Numéro du département', 'Nom de la région']].T)
                st.write("source : data.gouv")
            else:
                # Gérez les cas inattendus
                st.write("Une erreur inattendue est survenue.")        
        with col2:
            st.write("## Carte d'identité de ", ville2, " :")
            st.write("\n")
            ville2_data = villes[villes['city_code'] == ville2].squeeze()
            if isinstance(ville2_data, pd.DataFrame):
                if len(ville2_data['Libellé']) > 1:
                    ville2_data = ville2_data.drop_duplicates(subset=['insee_code'], keep='first')
                st.write(ville2_data[['insee_code', 'Libellé', 'Latitude', 'Longitude', 'Nom du département', 'Numéro du département', 'Nom de la région']].T)
                st.write("source : data.gouv")
            elif isinstance(ville2_data, pd.Series):
                ville2_data_df = ville2_data.to_frame().T
                st.write(ville2_data_df[['insee_code', 'Libellé', 'Latitude', 'Longitude', 'Nom du département', 'Numéro du département', 'Nom de la région']].T)
                st.write("source : data.gouv")
            else:
                # Gérez les cas inattendus
                st.write("Une erreur inattendue est survenue.")
        with col3:
            st.write("## Données chiffrées :")
            st.write("Est-ce qu'il y a des étudiants ? Allez-vous y trouver l'amour ?")
            cols_to_keep = ['insee_code', 'label', 'Population_totale', 'Population_homme', 'Population_femme', 'Population_etudiante', 'Population_celibataire', 'Population_marie']
            donnees_chiffrees_filtered = pop[pop['city_code'].isin(ville_selection)][cols_to_keep]
    
            # Filtrer pour garder une ligne par label unique
            donnees_chiffrees_unique_label = donnees_chiffrees_filtered.drop_duplicates(subset=['insee_code'], keep='first')
    
            # Transposer les données
            donnees_transposees = donnees_chiffrees_unique_label.T
    
            st.table(donnees_transposees)
            st.write("source : data.gouv")
        
        map_to_display = display_map(ville_selection, villes)
        with col1:
            st.write("\n")
            st.write("## Localisation des villes choisies :")
            folium_static(map_to_display)  
            st.write("\n")  
        with col3:
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.info("""
            **Avertissement sur l'exhaustivité des données :**

            Veuillez noter que les données présentées ici ne sont pas exhaustives et ne représentent qu'une partie des informations disponibles. Ces données sont issues de sources publiques et peuvent ne pas être complètes ou à jour. Il est important de garder à l'esprit les points suivants lors de l'analyse des données :

            - Les données disponibles peuvent être sujettes à des erreurs, des omissions ou des inexactitudes.
            - La qualité et la fiabilité des données peuvent varier en fonction de la source.
            - Certaines données peuvent être manquantes ou non disponibles pour certaines périodes de temps ou certaines régions géographiques.
            - Les informations présentées ici sont fournies à titre indicatif uniquement et ne doivent pas être utilisées comme seule source d'information pour prendre des décisions importantes.

            Veuillez utiliser ces données avec prudence et prendre en compte d'autres sources d'information et de contexte pour une analyse complète et précise.

            """)

    else:
        if len(ville_selection) > 2:
            st.warning("Veuillez sélectionner exactement deux villes.")

    if st.button("Accéder aux statistiques avancées"):
            statistiques_avancees()
   

# Page: Statistiques avancées
def statistiques_avancees():
    st.title("Statistiques Avancées")
    st.info("Chaque onglet vous permet de choisir le type d'information que vous voulez sur  chaque ville !")

    # Listedes noms des onglets
    tab_names = ["Éducation", "Travail", "Logement", "Santé", "Transports", "Sécurité", "Loisirs"]
    
    # Création des onglets
    tabs = st.tabs(tab_names)

    with tabs[0]:
        st.header("Éducation")

        if 'ville_selection' in st.session_state and len(st.session_state['ville_selection']) == 2:
            ville_selection = st.session_state['ville_selection']
            Villes_Education_select = Villes_Education[Villes_Education['city_code'].isin(ville_selection)]
            
            # Affichage nombre établissement privé et public par Villes
            grouped_df = Villes_Education_select.groupby(['Type_etablissement', 'Statut_public_prive', 'city_code']).size().reset_index(name='count')
            pivot_df = grouped_df.pivot_table(index=['Type_etablissement', 'Statut_public_prive'], columns='city_code', values='count', fill_value=0)
            pivot_df.reset_index(inplace=True)
            
            # Création de trois colonnes
            col1, col2, col3 = st.columns(3)

            with col1:
                # Affichage du DataFrame dans la première colonne
                st.write("### Tableau des établissements scolaires en fonction des villes")
                st.dataframe(pivot_df)
                st.write("source : Ministère de l'Éducation")

            with col2:
                # Traiter et afficher le premier graphique dans la deuxième colonne
                city_data_1 = Villes_Education_select[Villes_Education_select['city_code'] == ville_selection[0]]
                type_counts_1 = city_data_1['Type_etablissement'].value_counts()
                plot_data_1 = pd.DataFrame({'Type établissement': type_counts_1.index, 'Nombre': type_counts_1.values})
                fig_1 = px.pie(plot_data_1, values='Nombre', names='Type établissement', title=f'Répartition des types d\'établissements pour la ville {ville_selection[0]}')
                st.plotly_chart(fig_1)
                st.write("source : Ministère de l'Éducation")
            
            with col3:
                # Traiter et afficher le deuxième graphique dans la troisième colonne
                city_data_2 = Villes_Education_select[Villes_Education_select['city_code'] == ville_selection[1]]
                type_counts_2 = city_data_2['Type_etablissement'].value_counts()
                plot_data_2 = pd.DataFrame({'Type établissement': type_counts_2.index, 'Nombre': type_counts_2.values})
                fig_2 = px.pie(plot_data_2, values='Nombre', names='Type établissement', title=f'Répartition des types d\'établissements pour la ville {ville_selection[1]}')
                st.plotly_chart(fig_2)
                st.write("source : Ministère de l'Éducation")
        else:
            st.error("Veuillez d'abord sélectionner deux villes dans la page de comparaison.")

    with tabs[1]:
        st.header("Travail")

        if 'ville_selection' in st.session_state and len(st.session_state['ville_selection']) == 2:
            ville_selection = st.session_state['ville_selection']
            donnees_emploi_select = donnees_emploi[donnees_emploi['city_code'].isin(ville_selection)]

            # Assurez-vous de réinitialiser l'index
            donnees_emploi_select.reset_index(drop=True, inplace=True)
    
            # Création d'un DataFrame vide
            comparison_df = pd.DataFrame(donnees_emploi_select)
            col1, col2, col3 = st.columns(3)

            with col1:
            # Remplissage du DataFrame avec les données des villes sélectionnées
                st.write("### Tableau descriptif de la population des deux villes (actifs, chômeurs)")
                data_to_display = {}
                for ville_code in ville_selection:
                    ville_data = donnees_emploi_select[donnees_emploi_select['city_code'] == ville_code]
                    if not ville_data.empty:
                        ville_data = ville_data.iloc[0]  # Prendre la première ligne correspondant à la ville
                        # Ajouter les données de chaque ville sous forme de colonne dans data_to_display
                        data_to_display[ville_code] = ville_data

                # Convertir le dictionnaire en DataFrame pour l'affichage
                if data_to_display:
                    comparison_df = pd.DataFrame(data_to_display)  # Transpose pour avoir les villes en colonnes
                    # Affichage du DataFrame comparatif
                    st.write(comparison_df)
                    st.write("source : insee")
            
            with col2:
                for index, ville_code in enumerate(ville_selection):
                    # Extraction des données pour la ville actuelle
                    ville_data = donnees_emploi_select[donnees_emploi_select['city_code'] == ville_code]
            
                    if not ville_data.empty:
                        ville_data = ville_data.iloc[0]  # Prendre la première ligne correspondant à la ville
                        data_for_pie = {
                            'Catégories': ['Actifs Agriculteurs', 'Actifs Artisants Commerçants', 'Actifs Cadres', 'Actifs Prof Intermediare', 'Actifs Employés', 'Actifs Ouvriers', 'Chômeurs', 'Chômeuse'],
                            'Valeurs': [
                                ville_data['actifs_agriculteurs'], 
                                ville_data['actifs_artisants_commercants'], 
                                ville_data['actifs_cadres'], 
                                ville_data['actifs_prof_intermediare'], 
                                ville_data['actifs_employes'], 
                                ville_data['actifs_ouvriers'], 
                                ville_data['chomeurs'], 
                                ville_data['chomeuse']
                            ]
                        }
                        df_pie = pd.DataFrame(data_for_pie)
                        fig = px.pie(df_pie, values='Valeurs', names='Catégories', title=f"Répartition des effectifs des classes socio-professionnelles pour {ville_code}")
                        st.plotly_chart(fig)
                        
                    else:
                        st.error(f"Données non trouvées pour la ville {ville_code}.")
            with col3:
                st.write("\n")
                st.write("\n")
                st.info("#### Définitions :")
                st.write("\n")
                st.write("\n")
                st.write("\n")
                st.write("#### Population active")
                st.write("\n")
                st.write("La population active regroupe l'ensemble des personnes exerçant ou cherchant à exercer une activité professionnelle rémunérée. On regroupe dans la population active occupée uniquement les personnes déclarant exercer une activité professionnelle rémunérée. La population active inoccupée regroupe les chômeurs.")
                st.write("\n")
                st.write("\n")
                st.write("\n")
                st.write("\n")
                st.write("#### Classe Socie-Professionnelle (CSP)")
                st.write("\n")
                st.write("Ensemble de personnes occupant une même position sociale et partageant une communauté de destin et d'intérêt, sans forcément en avoir conscience (catégorie socioprofessionnelle).")
        else:
            st.error("Veuillez d'abord sélectionner deux villes dans la page de comparaison svp.")

    with tabs[2]:
        st.header("Logement")

        if 'ville_selection' in st.session_state and len(st.session_state['ville_selection']) == 2:
            ville_selection = st.session_state['ville_selection']
            # Base 2022
            Villes_Logement_select = Villes_logement[Villes_logement['city_code'].isin(ville_selection)]
            Villes_Logement_select = Villes_Logement_select.drop_duplicates(subset=['insee_code'], keep='first')
            # Base 2014-2022
            Villes_Logement_select_av = Villes_logement_avancees[Villes_logement_avancees['city_code'].isin(ville_selection)]

            col1, col2, col3 = st.columns(3)

            with col1:
                Villes_Logement_filtered = Villes_Logement_select[['insee_code', 'label', 'Nombre_de_Maisons_en_vente', 'Nombre_Apparts_en_vente', 'Prix_Moyen', 'Prix_au_m2_Moyen', 'Surface_Moyenne']]
                Villes_Logement_filtered_T = Villes_Logement_filtered.T
                st.write("### Tableau des données logement 2021")
                st.dataframe(Villes_Logement_filtered_T)
                st.write("source : insee")

            with col2:
                # Histogramme pour 'Prix_Moyen' par 'Annee'
                st.write("### Évolution du Prix Moyen du Logement par Année")
                tracer_histogramme(ville_selection, Villes_Logement_select_av, 'Prix_Moyen', 'Prix Moyen (€)')
                st.write("source : insee")

            with col3:
                # Histogramme pour 'Prix_au_m2_Moyen' par 'Annee'
                st.write("### Évolution du Prix Moyen du Logement au m2 par Année")
                tracer_histogramme(ville_selection, Villes_Logement_select_av, 'Prix_au_m2_Moyen', 'Prix au m² Moyen (€)')
                st.write("source : insee")

        else:
            st.error("Veuillez d'abord sélectionner deux villes dans la page de comparaison svp.")

    with tabs[3]:
        st.header("Santé")

        if 'ville_selection' in st.session_state and len(st.session_state['ville_selection']) == 2:
            ville_selection = st.session_state['ville_selection']

            Villes_sante_select = resultsante[resultsante['city_code'].isin(ville_selection)]
            
            pivot_df2 = Villes_sante_select.pivot_table(index='Type d\'etablissement', columns='city_code', aggfunc='size', fill_value=0)
            
            col1, col2 = st.columns(2)
            
            with col1:
                            
                if not pivot_df2.empty:
                    st.write("### Tableau de tous les établissements de santé par ville")
                    st.dataframe(pivot_df2)
                    st.write("source : onisep")
        
            with col2:
                # Grouper par ville et compter le nombre d'établissements
                total_etablissements_par_ville = Villes_sante_select.groupby('city_code').size().reset_index(name='Etablissement')
                # Créer le graphique avec Plotly
                fig = px.bar(total_etablissements_par_ville, x='city_code', y='Etablissement', 
                            title=' ',
                            labels={'city_code': 'Ville', 'Etablissement': 'Nombre d\'établissements'})

                # Personnaliser le style du graphique
                fig.update_traces(text=total_etablissements_par_ville['Etablissement'],  # Valeurs à afficher
                  textposition='outside',  # Position des étiquettes de données
                  marker_color='#CC394A',  # Couleur des barres
                  marker_line_color='#080000',  # Couleur des contours des barres
                  marker_line_width=1.5)  # Largeur des contours des barres

                fig.update_layout(font=dict(size=12),  # Taille de la police
                    xaxis_title='Ville',  # Titre de l'axe des x
                    yaxis_title='Nombre d\'établissements',  # Titre de l'axe des y
                    title_font=dict(size=18),  # Taille du titre
                    title_x=0.5,  # Position du titre
                    margin=dict(l=40, r=40, t=80, b=40))  # Marges intérieures

                # Afficher le graphique
                st.write("### Nombre total d'établissements par ville")
                st.plotly_chart(fig)
                st.write("source : onisep")
            
        else:
            st.error("Veuillez d'abord sélectionner deux villes dans la page de comparaison.")

    with tabs[4]:
        st.header("Transports")

        if 'ville_selection' in st.session_state and len(st.session_state['ville_selection']) == 2:
            ville_selection = st.session_state['ville_selection']
            # Filtrer la base pour les villes sélectionnées
            Villes_transports_df = transports_df[transports_df['city_code'].isin(ville_selection)]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write("### Tableau de la fréquentation et satisfaction des gares 2022")
                for ville in ville_selection:
                    Villes_transports_filtered = Villes_transports_df[Villes_transports_df['city_code'] == ville][['insee_code', 'label', 'department_name', 'nom_gare', 'total_voyageurs_2022', 'Satisfaction/10 2022']]
                    Villes_transports_filtered_T = Villes_transports_filtered.T
                    st.write(f"### {ville}")
                    st.dataframe(Villes_transports_filtered_T)
                    st.write("source : sncf")
                st.info("La chute de fréquentation des transports en 2020 : Le Covid-19 !")
            with col2:
                for ville in ville_selection:
                    df_ville = Villes_transports_df[Villes_transports_df['city_code'] == ville]
                    idx_max_voyageurs = find_max_voyageurs_index(df_ville)
                    if idx_max_voyageurs is not None:
                        df_gare_max_voyageurs = df_ville.loc[[idx_max_voyageurs]]                    
        
                        # Préparer les données pour le graphique, en se limitant à la gare avec le maximum de voyageurs
                        colonnes_voyageurs = {f'total_voyageurs_{annee}': annee for annee in range(2015, 2023)}
                        df_voyageurs_long = preparer_donnees_longues(df_gare_max_voyageurs, colonnes_voyageurs, 'total_voyageurs')
                        st.write(f"### Évolution du nombre total de passagers par Année pour la gare la plus fréquentée de {ville}")
                        tracer_histogramme([ville], df_voyageurs_long, 'total_voyageurs', 'Total des Voyageurs')
                        st.write("source : sncf")

                    else:
                        st.error(f"Pas de données pour {ville} ! Dommage !")

            with col3:
                dfs_satisfaction_filtrées = []
                colonnes_satisfaction = {f'Satisfaction/10 {annee}': annee for annee in range(2017, 2023)}
                for ville in ville_selection:
                    df_ville = Villes_transports_df[Villes_transports_df['city_code'] == ville]
                    idx_max_voyageurs = find_max_voyageurs_index(df_ville)
                    if idx_max_voyageurs is not None:
                        gare_max_voyageurs = df_ville.loc[idx_max_voyageurs, 'nom_gare']         
                        df_satisfaction_gare = df_ville[df_ville['nom_gare'] == gare_max_voyageurs]
                        dfs_satisfaction_filtrées.append(df_satisfaction_gare)

                if idx_max_voyageurs is not None:
                        # Concaténation des DataFrames filtrés pour obtenir un seul DataFrame pour tracer le graphique
                    df_satisfaction_final = pd.concat(dfs_satisfaction_filtrées)
                    df_satisfaction_long = preparer_donnees_longues(df_satisfaction_final, colonnes_satisfaction, 'satisfaction')

                    st.write(f"### Évolution de la satisfaction en gare (noté /10) pour la gare la plus fréquentée")
                    tracer_histogramme(ville_selection, df_satisfaction_long, 'satisfaction', 'Satisfaction')
                    st.write("source : sncf")
                    satisfaction_manquante = False
                    for ville in ville_selection:
                        df_ville_satisfaction = df_satisfaction_long[df_satisfaction_long['city_code'] == ville]
                        if df_ville_satisfaction['satisfaction'].isnull().all():
                            satisfaction_manquante = True
                        if satisfaction_manquante:
                            st.warning(f"### Données de satisfaction non disponibles pour {ville}")
                else:
                    st.error(f"Toujours pas de données...")

        else:
            st.error("Veuillez d'abord sélectionner deux villes dans la page de comparaison svp.")
    with tabs[5]:
        st.header("Sécurité")

        if 'ville_selection' in st.session_state and len(st.session_state['ville_selection']) == 2:
            ville_selection = st.session_state['ville_selection']
            villes_bis = villes.copy()
            villes_bis['insee_code'] = villes_bis['insee_code'].astype(str)
            crime_df['CODGEO'] = crime_df['CODGEO'].astype(str)
            villes_tres = villes_bis[villes_bis['city_code'].isin(ville_selection)]
            villes_tres = villes_tres.drop_duplicates(subset=['insee_code'], keep='first')
            Villes_Crime = pd.merge(villes_tres, crime_df, left_on='insee_code', right_on='CODGEO', how='right')
            Villes_Crime_selected = Villes_Crime[Villes_Crime['city_code'].isin(ville_selection)]
            Villes_Crime_selected['faits'] = Villes_Crime_selected['faits'].astype(int)

            # Grouper par année et calculer la somme des faits
            grouped_data = Villes_Crime_selected.groupby(['city_code', 'Annee']).sum()['faits'].reset_index()
            grouped_data2 = Villes_Crime_selected.groupby(['city_code', 'classe']).sum()['faits'].reset_index()
            sorted_data = grouped_data2.sort_values(by=['city_code', 'faits'], ascending=[True, False])
            # Sélectionner les données pour la première ville sélectionnée
            top_crimes_city1 = sorted_data[sorted_data['city_code'] == ville_selection[0]]


            # Sélectionner les données pour la deuxième ville sélectionnée
            top_crimes_city2 = sorted_data[sorted_data['city_code'] == ville_selection[1]]
            
            # Création de trois colonnes
            col1, col2, col3= st.columns(3)

            with col1:
               # Afficher les classes de délits triées par ordre décroissant pour la première ville sélectionnée
                st.write(f"Tous les crimes et  délits à {ville_selection[0]}:")
                st.write(top_crimes_city1)
                st.write("source : Ministère de l''Intérieur et des Outre-Mer")
            with col2:
                # Afficher les classes de délits triées par ordre décroissant pour la deuxième ville sélectionnée
                st.write(f"\nTous les crimes et  délits à {ville_selection[1]}:")
                st.write(top_crimes_city2)
                st.write("source : Ministère de l''Intérieur et des Outre-Mer")

            with col3:
                st.info("La ville de Nice n'est pas encore compatible avec l'onglet Sécurité ! Nous sommes en maintenance.")

                # Création du graphique
                fig = go.Figure()

                # Ajout des courbes pour chaque ville
                for city_code in ville_selection:
                    data = grouped_data[grouped_data['city_code'] == city_code]
                    fig.add_trace(go.Scatter(x=data['Annee'], y=data['faits'], mode='lines', name=city_code))

                # Configuration du layout
                st.write("### Total des délits et crimes commis par année et par ville")
                fig.update_layout(title='',
                            xaxis_title='Année',
                            yaxis_title='Nombre de faits')

                # Affichage du graphique
                st.plotly_chart(fig)
                st.write("source : Ministère de l''Intérieur et des Outre-Mer")
                st.write("###### Remarque : la majorité des faits considérés dans cette figure sont des délits.")
                

        else:
            st.error("Veuillez d'abord sélectionner deux villes dans la page de comparaison svp.")
    
    with tabs[6]:
        st.header("Culture")

        if 'ville_selection' in st.session_state and len(st.session_state['ville_selection']) == 2:
            ville_selection = st.session_state['ville_selection']
            Villes_Culture_select = Villes_Culture[Villes_Culture['city_code'].isin(ville_selection)].copy()
            col1, col2, col3 = st.columns(3)

            with col1:
                Villes_Culture_filtered = Villes_Culture_select[['insee_code', 'label', 'nom', 'adresse', 'label_et_appellation']]
                st.write("### Tableau des données générales sur les établissements culturels des deux villes (voir label)")
                st.dataframe(Villes_Culture_filtered)
                st.write("source : Ministère de la Culture")
            with col2:
                city_data_1_bis = Villes_Culture_select[Villes_Culture_select['label'] == ville_selection[0]]
                type_counts_1_bis = city_data_1_bis['type_equipement_ou_lieu'].value_counts()
                plot_data_1_bis = pd.DataFrame({'Type de Lieu': type_counts_1_bis.index, 'Nombre': type_counts_1_bis.values})
                fig_1_bis = px.pie(plot_data_1_bis, values='Nombre', names='Type de Lieu', title=f"Répartition des types de Lieu Culturel pour la ville {ville_selection[0]}")
                st.plotly_chart(fig_1_bis)
                st.write("source : Ministère de la Culture")

            with col3:
                # Traiter et afficher le deuxième graphique dans la troisième colonne
                city_data_2_bis = Villes_Culture_select[Villes_Culture_select['label'] == ville_selection[1]]
                type_counts_2_bis = city_data_2_bis['type_equipement_ou_lieu'].value_counts()
                plot_data_2_bis = pd.DataFrame({'Type de Lieu': type_counts_2_bis.index, 'Nombre': type_counts_2_bis.values})
                fig_2_bis = px.pie(plot_data_2_bis, values='Nombre', names='Type de Lieu', title=f"Répartition des types de Lieu Culturel pour la ville {ville_selection[1]}")
                st.plotly_chart(fig_2_bis) 
                st.write("source : Ministère de la Culture")

        else:
            st.error("Veuillez d'abord sélectionner deux villes dans la page de comparaison svp.")



# Les pages immersives  -------------------------------------------------------------------------------------------------------------------------------------------------------



# Page: Mention légale
def mention_legale():
    st.title("Mentions Légales Et CGU")
    st.info("Ceci est un exemple de Mentions Légales et CGU !")
    # Contenu des mentions légales en HTML
    mentions_legales_html = '''
    <h2>Informations sur l'entreprise</h2>
    <p>Nom de l'entreprise : Rivesurvey </p>
    <p>Adresse : 143 Avenue de Versailles, 75015, France</p>
    <p>Numéro de téléphone : +33 1 23 45 67 89</p>
    <p>Adresse e-mail : contact@rivesurvey.com</p>
    <br><br><br><br><br>
    <h2>Directeurs de la publication</h2>
    <p>Nom des directeurs de la publication : Jibril Ben Dhaou, Walid Bahri, Rémi Zignani</p>
    <br><br>
    <h2>Propriété intellectuelle</h2>
    <p>Tous les contenus de ce site web, y compris mais sans s'y limiter, les textes, les graphiques, les logos, les icônes, les images et le code source, sont lde propriété publique ou de ses fournisseurs de contenu, et sont protégés par les lois françaises et internationales sur le droit d'auteur.</p>
    <br><br>
    <h2>Utilisation des données personnelles</h2>
    <p>Nous collectons et utilisons les données personnelles des utilisateurs conformément à notre politique de confidentialité. Par exemple, nous pouvons collecter l'adresse e-mail des utilisateurs qui s'inscrivent à notre newsletter.</p>
    <br><br>
    <h2>Limitation de responsabilité</h2>
    <p>Nous ne sommes pas responsables des dommages résultant de l'utilisation de notre site web. Par exemple, nous ne pouvons pas être tenus responsables des pertes financières résultant de décisions prises sur la base des informations fournies sur notre site.</p>
    <br><br>
    <h2>Modification des conditions d'utilisation</h2>
    <p>Nous nous réservons le droit de modifier les conditions d'utilisation à tout moment. Les utilisateurs sont responsables de consulter régulièrement ces conditions pour prendre connaissance des éventuelles modifications.</p>

    <h2>Loi applicable et juridiction compétente</h2>
    <p>Ces conditions d'utilisation sont régies et interprétées conformément aux lois françaises. Tout litige découlant de ces conditions d'utilisation sera soumis à la compétence exclusive des tribunaux français.</p>
    <br><br>
    
    <h1>Conditions générales d'utilisation du site<h1>
    <p> Les présentes « conditions générales d'utilisation » ont pour objet l'encadrement juridique de l'utilisation du site [votre site] et de ses services.Ce contrat est conclu entre :Le gérant du site internet, ci-après désigné « l'Éditeur »,Toute personne physique ou morale souhaitant accéder au site et à ses services, ci-après appelé « l'Utilisateur ». Les conditions générales d'utilisation doivent être acceptées par tout Utilisateur, et son accès au site vaut acceptation de ces conditions. <p>
    <br>
    <p>L'Utilisateur est responsable des risques liés à l'utilisation de son identifiant de connexion et de son mot de passe. Le mot de passe de l'Utilisateur doit rester secret. En cas de divulgation de mot de passe, l'Éditeur décline toute responsabilité. Tout usage du service par l'Utilisateur ayant directement ou indirectement pour conséquence des dommages doit faire l'objet d'une indemnisation au profit du site. 
    <br>
    <p>...
    '''
    st.markdown(mentions_legales_html, unsafe_allow_html=True)

# Fonction pour le footer
def footer():
    st.markdown("---")
    # Style pour le pied de page
    st.markdown(
        '''
        <style>
            .footer {
                position: fixed;
                bottom: 0;
                width: 100%;
                background-color: #f8f9fa;
                padding: 10px;
                text-align: center;
            }
            .footer img {
                margin: 0 10px;
                height: 20px;
            }
        </style>
        ''',
        unsafe_allow_html=True
    )

    # Pied de page avec liens vers les réseaux sociaux
    st.markdown(
        """
        <div class="footer">
            <span>Suivez-nous sur les réseaux sociaux :</span>
            <a href="https://instagram.com" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Instagram"></a>
            <a href="https://linkedin.com" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn"></a>
            <a href="https://youtube.com" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg" alt="YouTube"></a>
        </div>
        """,
        unsafe_allow_html=True
    )

# Page: Contact
def contact():
    st.title("Où nous retrouver ? Comment nous contacter ?")
    st.write("## Remplissez le formulaire ci-dessous :")
    
    # Section pour saisir un message
    with st.form(key='contact_form'):
        st.write("### Envoyez-nous un message")
        name = st.text_input("Nom")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submit_button = st.form_submit_button("Envoyer")
        
        if submit_button:
            st.success("Merci, votre message a été envoyé.")
            # Ici, vous pouvez ajouter le code pour traiter le message,
            # comme l'envoyer par email ou le stocker dans une base de données.
    
    # Liens vers les réseaux sociaux
    st.write("## Nous suivre sur les réseaux sociaux")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("[![Facebook](https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://facebook.com/votrepage)")
    with col2:
        st.markdown("[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/votrecompte)")
    with col3:
        st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/votreprofil)")
    
    # Information de contact par email
    st.write("## Contactez-nous par email")
    st.markdown("Envoyez-nous un email à : [contact@rivesurvey.com](mailto:remizedd@gmail.com)")
    
    # Remerciement de visite
    st.write("---")
    st.caption("Merci de visiter notre site de comparaison de villes !")



# La mise en place -------------------------------------------------------------------------------------------------------------------------------------------------------



# Définitions de toutes les pages
pages = {
    "Bienvenue" : page_accueil,
    "Comparaisons des villes" : compare_villes,
    "Mentions Légales": mention_legale,
    "Nous contacter": contact
}

st.sidebar.write("Rivesurvey vous remercie !")

# Ajout d'espaces pour pousser le contenu vers le bas
for _ in range(3):
    st.sidebar.write("\n")

# barre de navigation
selection = st.sidebar.radio("Navigation", list(pages.keys()))
pages[selection]()

# Ajout d'espaces pour pousser le contenu vers le bas
for _ in range(35): 
    st.sidebar.write("\n")

# Le contenu que vous voulez en bas
st.sidebar.markdown("### Contactez-nous")
st.sidebar.markdown("Email: contact@rivesurvey.com")

# Initié le footer
footer()



# Fin du code de Rivesurvey  -------------------------------------------------------------------------------------------------------------------------------------------------------