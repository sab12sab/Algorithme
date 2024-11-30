import streamlit as st
from graph_generator import generate_random_graph, graph_to_dict
from dijkstra import dijkstra_fibonacci, dijkstra_binary_heap
from huffman import huffman_compress, huffman_decompress

# Titre de l'application Streamlit
st.title("Application Dijkstra et Huffman")

# Choix de l'algorithme via un menu déroulant
algorithm = st.sidebar.selectbox("Choisissez un algorithme", ["Dijkstra avec Tas de Fibonacci", "Dijkstra avec Tas Binaire", "Compression et Décompression Huffman"])

# Implémentation du Dijkstra avec Tas de Fibonacci
if algorithm == "Dijkstra avec Tas de Fibonacci":
    st.header("Dijkstra avec Tas de Fibonacci")
    
    # Paramètres du graphe
    num_nodes = st.slider("Nombre de nœuds", min_value=5, max_value=50, value=10)
    density = st.slider("Densité du graphe", min_value=0.1, max_value=1.0, value=0.5)
    
    # Générer le graphe aléatoire
    graph = generate_random_graph(num_nodes, density)
    graph_dict = graph_to_dict(graph)
    
    start_node = st.selectbox("Choisissez le nœud de départ", options=list(graph_dict.keys()))
    
    # Calcul des plus courts chemins avec Dijkstra
    distances, predecessors = dijkstra_fibonacci(graph_dict, start_node)  # Ou dijkstra_binary_heap
    
    st.write(f"Distances depuis le nœud {start_node} :", distances)
    st.write("Prédécesseurs :", predecessors)

# Implémentation de la compression et décompression Huffman
elif algorithm == "Compression et Décompression Huffman":
    st.header("Compression et Décompression Huffman")

    uploaded_file = st.file_uploader("Téléchargez un fichier à compresser", type=["txt"])
    if uploaded_file:
        file_content = uploaded_file.getvalue().decode("utf-8")
        
        if not file_content:
            st.error("Le fichier est vide. Impossible de compresser.")
        else:
            # Compression du fichier
            compressed_data, tree = huffman_compress(file_content)
            
            st.write("Données compressées :", compressed_data)
            st.write("Arbre de Huffman :", tree)
            
            # Sauvegarder l'arbre et les données compressées dans les variables de session
            st.session_state.compressed_data = compressed_data
            st.session_state.tree = tree

    # Décompression
    if 'compressed_data' in st.session_state:
        if st.button("Décompresser"):
            decompressed_data = huffman_decompress(st.session_state.compressed_data, st.session_state.tree)
            st.write("Données décompressées :", decompressed_data)
