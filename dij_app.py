import streamlit as st
import heapq
import networkx as nx
import matplotlib.pyplot as plt
import random

# Fonction pour implémenter l'algorithme de Dijkstra avec un tas binaire
def dijkstra(graph, start, end):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    priority_queue = [(0, start)]
    previous_nodes = {node: None for node in graph}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > dist[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            if weight == 0:  # Ne pas traiter les arêtes avec une distance de 0
                continue
            distance = current_distance + weight
            if distance < dist[neighbor]:
                dist[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    # Pour afficher le chemin
    path = []
    current_node = end
    while current_node:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    
    path.reverse()
    return dist, path  # Retourne les distances et le chemin

# Fonction pour afficher un graphe avec networkx
def draw_graph(graph):
    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            if weight > 0:  # Ignorer les arêtes avec une distance de 0
                G.add_edge(node, neighbor, weight=weight)
    
    pos = nx.spring_layout(G)  # Positionnement des nœuds
    labels = nx.get_edge_attributes(G, 'weight')
    
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=12)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    st.pyplot(plt)

# Fonction pour générer un graphe avec des nœuds et distances aléatoires
def generate_random_graph(num_nodes):
    node_names = [f"Node{i+1}" for i in range(num_nodes)]
    graph = {node: {} for node in node_names}

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            distance = random.randint(1, 10)  # Génère des distances aléatoires entre 1 et 10
            graph[node_names[i]][node_names[j]] = distance
            graph[node_names[j]][node_names[i]] = distance

    return node_names, graph

# Interface Streamlit
def app():
    st.title("Application Dijkstra avec Tas Binaire et Graphe Dynamique")

    # Demander à l'utilisateur s'il veut générer des noms de nœuds et des distances aléatoires
    choix = st.radio("Souhaitez-vous :",
                     ["Générer des nœuds et distances aléatoires", "Choisir vos nœuds et distances"])

    if choix == "Générer des nœuds et distances aléatoires":
        # Entrée du nombre de nœuds avec clé unique
        num_nodes = st.number_input("Nombre de nœuds", min_value=2, step=1, key="num_nodes")

        # Générer un graphe avec des nœuds et distances aléatoires
        node_names, graph = generate_random_graph(num_nodes)

        # Affichage du graphe généré
        st.write("### Graphe généré aléatoirement :")
        draw_graph(graph)

    else:
        # Entrée du nombre de nœuds avec clé unique
        num_nodes = st.number_input("Nombre de nœuds", min_value=2, step=1, key="num_nodes")

        # Entrée des noms des nœuds avec des clés uniques
        node_names = []
        for i in range(num_nodes):
            node_name = st.text_input(f"Nom du nœud {i+1}", f"Nœud {i+1}", key=f"node_name_{i}")
            node_names.append(node_name)

        # Création du graphe
        graph = {node: {} for node in node_names}

        # Entrée des distances entre les nœuds avec des clés uniques
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                distance = st.number_input(f"Distance entre {node_names[i]} et {node_names[j]} (0 = pas de connexion)", 
                                          min_value=0, step=1, key=f"distance_{i}_{j}", format="%d")
                if distance > 0:  # Si la distance est positive, on l'ajoute au graphe
                    graph[node_names[i]][node_names[j]] = distance
                    graph[node_names[j]][node_names[i]] = distance

        # Affichage du graphe immédiatement après avoir entré les informations
        st.write("### Graphe créé par l'utilisateur :")
        draw_graph(graph)

    # Choisir un nœud de départ et un nœud d'arrivée
    start_node = st.selectbox("Choisissez le nœud de départ", node_names, key="start_node")
    end_node = st.selectbox("Choisissez le nœud d'arrivée", node_names, key="end_node")

    if st.button("Calculer le plus court chemin"):
        # Exécution de l'algorithme de Dijkstra
        dist, path = dijkstra(graph, start_node, end_node)

        # Affichage des distances initiales
        st.write("### Distances initiales de chaque nœud (avant l'algorithme de Dijkstra) :")
        initial_distances = {node: (0 if node == start_node else float('inf')) for node in graph}
        st.write(initial_distances)

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

if __name__ == "__main__":
    app()
