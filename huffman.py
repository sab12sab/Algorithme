import streamlit as st
from collections import Counter
import heapq
import tempfile

# Définition des fonctions nécessaires à l'algorithme de Huffman
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
    return " ".join(codes[char] for char in text)

def decompress(binary_data, root):
    result = []
    node = root
    for bit in binary_data:
        node = node.left if bit == "0" else node.right
        if node.char is not None:  # Feuille
            result.append(node.char)
            node = root
    return "".join(result)


