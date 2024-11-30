import networkx as nx
import random

def generate_random_graph(num_nodes, density):
    """
    Cette fonction génère un graphe aléatoire à l'aide du modèle d'Erdős–Rényi,
    en créant un graphe avec un nombre donné de nœuds et une densité spécifiée.
    """
    # Créer un graphe aléatoire en utilisant le modèle d'Erdős–Rényi
    G = nx.erdos_renyi_graph(num_nodes, density)
    
    # Ajouter des poids aléatoires sur les arêtes du graphe
    for u, v in G.edges():
        G[u][v]['weight'] = random.randint(1, 10)  # Poids entre 1 et 10
    
    return G

def graph_to_dict(G):
    """
    Cette fonction convertit un graphe NetworkX en un dictionnaire de voisins pour
    chaque nœud avec leurs poids. Ceci est utile pour l'algorithme de Dijkstra.
    """
    return {node: {neighbor: data['weight'] for neighbor, data in G[node].items()} for node in G}
