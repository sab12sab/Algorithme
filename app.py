import streamlit as st
from search_engine import SearchEngine
from huffman import calculate_frequency, build_huffman_tree, generate_codes, compress, decompress
from dij_app import dijkstra, draw_graph, generate_random_graph
import tempfile  # Pour créer un fichier temporaire
import matplotlib.pyplot as plt

# --- Interface Streamlit ---
st.sidebar.title("Choisissez une fonction")
option = st.sidebar.selectbox("Options", ["Moteur de Recherche", "Compression de Fichiers", "Algorithme de Dijkstra"])

# --- Moteur de Recherche ---
if option == "Moteur de Recherche":
    st.title("Moteur de Recherche Simplifié")
    
    uploaded_files = st.file_uploader("Téléchargez vos fichiers texte (.txt)", type=["txt"], accept_multiple_files=True)
    
    search_engine = SearchEngine()
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            content = uploaded_file.read().decode("utf-8")
            search_engine.index_document(uploaded_file.name, content)
        st.success(f"{len(uploaded_files)} fichier(s) indexé(s).")
    
    query = st.text_input("Entrez votre requête :")
    operator = st.radio("Choisissez un opérateur :", ["ET", "OU"])
    fuzzy = st.checkbox("Activer la recherche floue")
    
    if st.button("Rechercher"):
        if query:
            results = search_engine.search(query, operator=operator, fuzzy=fuzzy)
            if results:
                st.write("Documents trouvés :")
                for result in results:
                    st.write(f"- {result}")
            else:
                st.write("Aucun document trouvé pour votre recherche.")

# --- Compression Huffman ---
elif option == "Compression de Fichiers":
    st.title("Compression de Fichiers avec Huffman")
    
    uploaded_file = st.file_uploader("Téléchargez un fichier texte", type=["txt"])
    if uploaded_file:
        text = uploaded_file.read().decode("utf-8")
        st.write("Contenu du fichier :")
        st.text_area("Texte brut", text, height=200)
        
        # Compression
        frequencies = calculate_frequency(text)
        huffman_tree = build_huffman_tree(frequencies)
        codes = generate_codes(huffman_tree)
        compressed_data = compress(text, codes)
        
        st.write("Taille compressée :", len(compressed_data))
        st.write("Taux de compression :", len(compressed_data) / (len(text) * 8))

        # Visualiser le fichier compressé sous forme binaire
        st.write("Contenu compressé :")
        st.text_area("Données compressées (binaire)", compressed_data, height=200)

        # Créer un fichier temporaire pour le téléchargement
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix=".bin") as temp_file:
            temp_file.write(compressed_data)
            temp_file_path = temp_file.name
        
        # Bouton de téléchargement
        st.download_button(
            label="Télécharger le fichier compressé",
            data=compressed_data,
            file_name=f"{uploaded_file.name}.bin",
            mime="application/octet-stream"
        )

        # Décompression
        if st.button("Décompresser"):
            decompressed_text = decompress(compressed_data, huffman_tree)
            st.text_area("Texte décompressé", decompressed_text, height=200)

# --- Algorithme de Dijkstra ---
elif option == "Algorithme de Dijkstra":  # Suppression de l'espace avant le nom
    st.title("Application Dijkstra avec Tas Binaire")

    # Demander à l'utilisateur de choisir un graphe
    num_nodes = st.number_input("Nombre de nœuds", min_value=2, step=1, key="num_nodes")
    node_names = [f"Node{i+1}" for i in range(num_nodes)]

    # Créer un graphe vide
    graph = {node: {} for node in node_names}

    # Entrée des distances entre les nœuds
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            distance = st.number_input(f"Distance entre {node_names[i]} et {node_names[j]} (0 = pas de connexion)", 
                                      min_value=0, step=1, key=f"distance_{i}_{j}", format="%d")
            if distance > 0:
                graph[node_names[i]][node_names[j]] = distance
                graph[node_names[j]][node_names[i]] = distance

    # Choisir un nœud de départ et un nœud d'arrivée
    start_node = st.selectbox("Choisissez le nœud de départ", node_names, key="start_node")
    end_node = st.selectbox("Choisissez le nœud d'arrivée", node_names, key="end_node")

    if st.button("Calculer le plus court chemin"):
        # Appel de la fonction dijkstra provenant du fichier dij_app.py
        dist, path = dijkstra(graph, start_node, end_node)

        # Affichage du chemin et de la distance
        if dist[end_node] == float('inf'):
            st.write(f"Aucun chemin disponible entre {start_node} et {end_node}.")
        else:
            st.write(f"Le plus court chemin de {start_node} à {end_node} est :")
            st.write(" -> ".join(path))
            st.write(f"Distance totale : {dist[end_node]} unités.")

        # Affichage des distances minimales calculées par l'algorithme de Dijkstra
        st.write("### Distances minimales après l'algorithme de Dijkstra :")
        st.write(dist)
