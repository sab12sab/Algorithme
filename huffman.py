import streamlit as st
from collections import Counter
import heapq
import pandas as pd  # Pour créer et afficher le tableau
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
import re

# Classe pour représenter les nœuds de l'arbre
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = self.right = None
        
    def __lt__(self, other):
        return self.freq < other.freq

# Calcul des fréquences des caractères




def calculate_frequency(text):
    # Conserver uniquement les caractères alphanumériques, les accents, les espaces et les signes de ponctuation spécifiés
    cleaned_text = re.sub(r"[^a-zA-Z0-9 .!,;:éèàç']", '', text)  # Inclut les caractères accentués et la ponctuation choisie
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Remplace plusieurs espaces par un seul et supprime les espaces aux extrémités
    
    frequencies = {}
    for char in cleaned_text:
        frequencies[char] = frequencies.get(char, 0) + 1
    return frequencies


# Construction de l'arbre de Huffman
def build_huffman_tree(frequencies):
    # Trier les caractères par fréquence (ordre croissant)
    heap = [Node(char, freq) for char, freq in sorted(frequencies.items(), key=lambda item: item[1])]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    
    return heap[0]

# Fonction récursive pour tracer l'arbre de Huffman avec étiquettes sur les arêtes
def plot_huffman_tree(node, graph=None, pos=None, x=0, y=0, layer=1, parent=None, edge_label=None, leaf_positions=None):
    if graph is None:
        graph = nx.DiGraph()
        pos = {}
        leaf_positions = {}

    if node.char:
        label = f"{node.char}:{node.freq}"
        # Placer les feuilles (les caractères) de manière horizontale (de gauche à droite)
        leaf_positions[node.char] = (x, y)
    else:
        label = f"{node.freq}"
    
    pos[label] = (x, y)
    graph.add_node(label)
    
    if parent:
        graph.add_edge(parent, label, label=edge_label)  # Ajouter l'étiquette de l'arête
    
    if node.left:
        plot_huffman_tree(node.left, graph, pos, x=x - 1 / layer, y=y - 1, layer=layer * 2, parent=label, edge_label='0', leaf_positions=leaf_positions)  # Étiquette '0' pour l'arête gauche
        
    if node.right:
        plot_huffman_tree(node.right, graph, pos, x=x + 1 / layer, y=y - 1, layer=layer * 2, parent=label, edge_label='1', leaf_positions=leaf_positions)  # Étiquette '1' pour l'arête droite
        
    return graph, pos, leaf_positions

# Définition des classes et fonctions nécessaires à l'algorithme de Huffman

def generate_codes(node, current_code="", codes={}):
    if node is None:
        return
    if node.char is not None:  # Feuille
        codes[node.char] = current_code
    generate_codes(node.left, current_code + "0", codes)
    generate_codes(node.right, current_code + "1", codes)
    return codes

def compress(text, codes):
    return "".join(codes[char] for char in text)

def decompress(binary_data, root):
    result = []
    node = root
    for bit in binary_data:
        node = node.left if bit == "0" else node.right
        if node.char is not None:  # Feuille
            result.append(node.char)
            node = root
    return "".join(result)



