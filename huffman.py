import streamlit as st
from collections import Counter
import heapq
import pandas as pd  # Pour créer et afficher le tableau
import matplotlib.pyplot as plt
import networkx as nx










# Définition des classes et fonctions nécessaires à l'algorithme de Huffman
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def calculate_frequency(text):
    return Counter(text)

def build_huffman_tree(frequencies):
    heap = [Node(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    
    return heap[0]

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

# Fonction récursive pour tracer l'arbre de Huffman avec étiquettes sur les arêtes
def plot_huffman_tree(node, graph=None, pos=None, x=0, y=0, layer=1, parent=None, edge_label=None):
    if graph is None:
        graph = nx.DiGraph()
        pos = {}
    
    if node.char:
        label = f"{node.char}:{node.freq}"
    else:
        label = f"{node.freq}"
    
    pos[label] = (x, y)
    graph.add_node(label)
    
    if parent:
        graph.add_edge(parent, label, label=edge_label)  # Ajouter l'étiquette de l'arête
    
    if node.left:
        plot_huffman_tree(node.left, graph, pos, x=x - 1 / layer, y=y - 1, layer=layer * 2, parent=label, edge_label='0')  # Étiquette '0' pour l'arête gauche
        
    if node.right:
        plot_huffman_tree(node.right, graph, pos, x=x + 1 / layer, y=y - 1, layer=layer * 2, parent=label, edge_label='1')  # Étiquette '1' pour l'arête droite
        
    return graph, pos
