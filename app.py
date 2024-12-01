import streamlit as st  # Importation de Streamlit pour créer l'interface utilisateur
from search_engine import SearchEngine  # Importation du moteur de recherche
from huffman import calculate_frequency, build_huffman_tree, generate_codes, compress, decompress  # Importation des fonctions de compression Huffman
from dij_app import dijkstra, draw_graph, generate_random_graph  # Importation de l'algorithme de Dijkstra et de la fonction pour dessiner le graphe
import tempfile  # Pour créer un fichier temporaire
import matplotlib.pyplot as plt  # Pour dessiner le graphe avec matplotlib
import time  # Pour mesurer le temps d'exécution de l'algorithme

st.sidebar.image('logo1.jpeg', width=100)
st.markdown(
    """
    <style>
    .css-1d391kg {
        padding-top: 0px;
    }
    .sidebar .sidebar-content {
        padding-top: 0px;
    }
    .css-1y4v71h image {
        display: block;
        margin-left: 0;
        margin-right: auto;
        margin-top: 0;
        position: absolute;
    }
    </style>
    """, unsafe_allow_html=True)
# --- Interface Streamlit ---
st.sidebar.title("Choisissez une fonction")  # Titre de la barre latérale
option = st.sidebar.selectbox("Options", ["Page d'accueil", "Moteur de Recherche", "Compression de Fichiers", "Algorithme de Dijkstra"])  # Choix entre différentes options

# --- Page d'accueil ---
if option == "Page d'accueil":
    st.image("logo_algo.jpg", use_container_width=False, width=3000, caption=None)

# Titre sur la même ligne, avec ALGOFUSION en rouge et en gras
    st.markdown("""
    <h1 style="font-size: 50px;">Bienvenue dans  <span style="font-weight: bold; color: #9b111e;">ALGOFUSION</span></h1>
""", unsafe_allow_html=True)
  
    st.markdown("""
    Explorez l'innovation, découvrez des algorithmes puissants et laissez-vous inspirer par la simplicité de nos solutions. Choisissez un projet et plongez dans l'univers de la technologie à portée de main.
    """)
    

    # Description de chaque programme
    st.subheader("**Compression de Données avec l'Algorithme de Huffman**")
    st.markdown("""
    Explorez l'art de réduire la taille des fichiers sans perdre d'information. Grâce à l'algorithme de Huffman, ce projet compresse des fichiers texte en optimisant la représentation des caractères, rendant les fichiers plus légers et faciles à stocker ou transmettre.
    """)

    st.subheader("**Moteur de Recherche Simplifié**")
    st.markdown("""
    Trouvez ce que vous cherchez instantanément ! Ce moteur de recherche indexe des documents texte et vous permet de rechercher des mots-clés rapidement, en utilisant des opérateurs comme **ET** et **OU** pour affiner vos résultats, rendant l'exploration de grandes quantités de données simple et efficace.
    """)

    st.subheader("**Algorithme de Dijkstra Optimisé**")
    st.markdown("""
    Découvrez le chemin le plus court dans un réseau complexe ! Ce projet utilise l’algorithme de Dijkstra pour optimiser le calcul des itinéraires, avec la possibilité de générer des distances aléatoires ou de les personnaliser, pour une expérience fluide et rapide.
    """)


# --- Moteur de Recherche ---
elif option == "Moteur de Recherche":
    st.title("**Moteur de Recherche Simplifié**")  # Titre en gras
    st.markdown("""
    Trouvez ce que vous cherchez instantanément ! Ce moteur de recherche indexe des documents texte et vous permet de rechercher des mots-clés rapidement, en utilisant des opérateurs comme **ET** et **OU** pour affiner vos résultats, rendant l'exploration de grandes quantités de données simple et efficace.
    """)

    uploaded_files = st.file_uploader("Téléchargez vos fichiers texte (.txt)", type=["txt"], accept_multiple_files=True)  # Permet à l'utilisateur de télécharger plusieurs fichiers texte
    search_engine = SearchEngine()  # Initialisation du moteur de recherche

    if uploaded_files:  # Si des fichiers sont téléchargés
        for uploaded_file in uploaded_files:
            content = uploaded_file.read().decode("utf-8")  # Lire le contenu du fichier et le décoder en texte
            search_engine.index_document(uploaded_file.name, content)  # Indexer le contenu du fichier
        st.success(f"{len(uploaded_files)} fichier(s) indexé(s).")  # Afficher un message de succès

    query = st.text_input("Entrez votre requête :")  # Demander à l'utilisateur de saisir une requête
    operator = st.radio("Choisissez un opérateur :", ["ET", "OU"])  # Choisir entre les opérateurs "ET" ou "OU" pour la recherche
    fuzzy = st.checkbox("Activer la recherche floue")  # Choisir si la recherche floue doit être activée

    if st.button("Rechercher"):  # Si l'utilisateur appuie sur le bouton de recherche
        if query:  # Si une requête a été saisie
            results = search_engine.search(query, operator=operator, fuzzy=fuzzy)  # Effectuer la recherche
            if results:  # Si des résultats sont trouvés
                st.write("Documents trouvés :")
                for result in results:
                    st.write(f"- {result}")  # Afficher les résultats trouvés
            else:
                st.write("Aucun document trouvé pour votre recherche.")  # Afficher si aucun document n'a été trouvé

# --- Compression Huffman ---
elif option == "Compression de Fichiers":
    st.title("**Compression de Données avec l'Algorithme de Huffman**")  # Titre en gras
    st.markdown("""
    Explorez l'art de réduire la taille des fichiers sans perdre d'information. Grâce à l'algorithme de Huffman, ce projet compresse des fichiers texte en optimisant la représentation des caractères, rendant les fichiers plus légers et faciles à stocker ou transmettre.
    """)

    uploaded_file = st.file_uploader("Téléchargez un fichier texte", type=["txt"])  # Permet à l'utilisateur de télécharger un fichier texte
    if uploaded_file:  # Si un fichier est téléchargé
        text = uploaded_file.read().decode("utf-8")  # Lire le contenu du fichier et le décoder
        st.write("Contenu du fichier :")  # Afficher le texte brut du fichier
        st.text_area("Texte brut", text, height=200)  # Afficher le texte dans une zone de texte

        # Compression Huffman
        frequencies = calculate_frequency(text)  # Calculer la fréquence des caractères
        huffman_tree = build_huffman_tree(frequencies)  # Construire l'arbre Huffman
        codes = generate_codes(huffman_tree)  # Générer les codes Huffman
        compressed_data = compress(text, codes)  # Compresser les données avec les codes Huffman

        st.write("Taille compressée :", len(compressed_data))  # Afficher la taille du fichier compressé
        st.write("Taux de compression :", len(compressed_data) / (len(text) * 8))  # Calculer et afficher le taux de compression

        # Visualiser le fichier compressé sous forme binaire
        st.write("Contenu compressé :")
        st.text_area("Données compressées (binaire)", compressed_data, height=200)  # Afficher les données compressées

        # Créer un fichier temporaire pour le téléchargement
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix=".bin") as temp_file:
            temp_file.write(compressed_data)  # Écrire les données compressées dans un fichier temporaire
            temp_file_path = temp_file.name  # Sauvegarder le chemin du fichier temporaire
        
        # Bouton de téléchargement
        st.download_button(
            label="Télécharger le fichier compressé",  # Étiquette du bouton
            data=compressed_data,  # Les données compressées à télécharger
            file_name=f"{uploaded_file.name}.bin",  # Nom du fichier compressé
            mime="application/octet-stream"  # Type MIME du fichier
        )

        # Décompression
        if st.button("Décompresser"):  # Si l'utilisateur appuie sur le bouton de décompression
            decompressed_text = decompress(compressed_data, huffman_tree)  # Décompresser les données
            st.text_area("Texte décompressé", decompressed_text, height=200)  # Afficher le texte décompressé


# --- Algorithme de Dijkstra ---
elif option == "Algorithme de Dijkstra":
    st.title("Application Dijkstra avec Tas Binaire et Graphe Dynamique")  # Titre de la page
    
    # Choix du mode de création du graphe
    choix = st.radio(
        "Comment souhaitez-vous définir les nœuds et les distances ?",
        ("Générer aléatoirement", "Entrer manuellement")
    )  # Choisir entre générer un graphe aléatoire ou entrer les données manuellement
    
    # Initialisation du graphe et des nœuds
    graph = {}
    node_names = []
    
    if choix == "Générer aléatoirement":  # Si l'utilisateur choisit de générer un graphe aléatoire
        num_nodes = st.number_input("Nombre de nœuds", min_value=2, step=1, key="num_nodes_random")  # Demander le nombre de nœuds
        
        if num_nodes:  # Si un nombre de nœuds est saisi
            node_names, graph = generate_random_graph(num_nodes)  # Générer le graphe aléatoire
            st.success(f"Un graphe avec {num_nodes} nœuds a été généré aléatoirement.")  # Afficher un message de succès
            draw_graph(graph)  # Afficher le graphe

    else:  # Si l'utilisateur choisit de définir les distances manuellement
        num_nodes = st.number_input("Nombre de nœuds", min_value=2, step=1, key="num_nodes_manual")  # Demander le nombre de nœuds
        
        if num_nodes:  # Si un nombre de nœuds est saisi
            for i in range(num_nodes):
                node_name = st.text_input(f"Nom du nœud {i+1}", f"Node{i+1}", key=f"node_name_{i}")  # Saisir le nom des nœuds
                node_names.append(node_name)  # Ajouter les noms des nœuds à la liste
            graph = {node: {} for node in node_names}  # Créer un graphe vide avec les nœuds comme clés
            
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    distance = st.number_input(
                        f"Distance entre {node_names[i]} et {node_names[j]} (0 = pas de connexion)", 
                        min_value=0, step=1, key=f"distance_{i}_{j}"
                    )  # Demander la distance entre chaque paire de nœuds
                    if distance > 0:  # Si la distance est supérieure à 0
                        graph[node_names[i]][node_names[j]] = distance  # Ajouter la distance dans le graphe
                        graph[node_names[j]][node_names[i]] = distance  # Ajouter la distance dans l'autre sens
            draw_graph(graph)  # Afficher le graphe

    # Choisir un nœud de départ et d'arrivée
    if node_names:
        start_node = st.selectbox("Choisissez le nœud de départ", node_names, key="start_node")  # Sélectionner le nœud de départ
        end_node = st.selectbox("Choisissez le nœud d'arrivée", node_names, key="end_node")  # Sélectionner le nœud d'arrivée
        
        if st.button("Calculer le plus court chemin"):  # Si l'utilisateur appuie sur le bouton pour calculer le plus court chemin
            start_time = time.time()  # Démarre le chronométrage
            
            # Initialisation des distances
            initial_distances = {node: float('inf') for node in node_names}  # Distance initiale = inf pour tous les nœuds
            initial_distances[start_node] = 0  # La distance du nœud de départ est 0

            # Exécution de l'algorithme de Dijkstra
            dist, path = dijkstra(graph, start_node, end_node)  # Appliquer l'algorithme de Dijkstra
            
            execution_time = time.time() - start_time  # Temps écoulé
            
            if dist[end_node] == float('inf'):  # Si aucun chemin n'a été trouvé
                st.error(f"Aucun chemin disponible entre {start_node} et {end_node}.")
            else:
                st.success(f"Le plus court chemin de {start_node} à {end_node} est : {' -> '.join(path)}")
                st.info(f"Distance totale : {dist[end_node]} unités.")
            
            # Affichage des distances minimales
            st.write("### Distances minimales calculées :")
            st.write(dist)
            
            # Affichage des distances initiales et finales pour chaque nœud
            st.write("### Détails de chaque nœud :")
            for node in node_names:
               st.markdown(f"**Nœud : {node}**\n\n"
            f"Distance initiale : {initial_distances[node]}\n\n"
            f"Distance finale : {'∞' if dist[node] == float('inf') else dist[node]}\n\n"
            f"Chemin : {' -> '.join(path) if dist[node] != float('inf') else 'Aucun chemin'}\n\n")
            
            st.write(f"### Temps d'exécution de l'algorithme de Dijkstra :")
            st.write(f"{execution_time:.4f} secondes.")

st.markdown("""
    <style>
    /* Style pour le pied de page */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #9b111e; /* Couleur de l'arrière-plan */
        color: white; /* Couleur du texte */
        text-align: center; /* Centrer horizontalement le texte */
        padding: 10px 0; /* Espacement vertical */
        font-size: 14px; /* Taille de la police */
        font-family: Arial, sans-serif; /* Police */
        z-index: 1000; /* Priorité sur d'autres éléments */
        display: flex; /* Flexbox pour le centrage */
        justify-content: center; /* Centrage horizontal */
        align-items: center; /* Centrage vertical */
    }
    </style>
    <div class="footer">
        Réalisé par  Sabrine  , Houda Erimi, Rania Kettani
    </div>
""", unsafe_allow_html=True)


st.markdown("""
    <style>
        
        /* Appliquer la couleur rouge (#9b111e) et le gras à tous les grands titres */
        h1 {
            font-weight: bold;
            color: #9b111e;
        }

        /* Styliser la barre latérale avec la couleur #9b111e */
        .css-1d391kg {
            background-color: #9b111e;
            color: white;
        }

        /* Styliser le texte de la barre latérale */
        .css-1d391kg a {
            color: white;
        }

        /* Styliser les éléments de la barre latérale */
        .css-1v3fvcr {
            background-color: #9b111e;
        }
    </style>
            
""", unsafe_allow_html=True)
import streamlit as st

