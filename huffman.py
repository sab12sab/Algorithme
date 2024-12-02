from collections import Counter
import heapq

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

# Fonction compressée modifiée pour ajouter un espace entre chaque code binaire
def compress(text, codes):
    # Ajouter un espace entre chaque code binaire
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

# Exemple d'utilisation
text = "hello world"
frequencies = calculate_frequency(text)  # Calculer la fréquence des caractères
huffman_tree = build_huffman_tree(frequencies)  # Construire l'arbre Huffman
codes = generate_codes(huffman_tree)  # Générer les codes Huffman
compressed_data = compress(text, codes)  # Compresser les données avec les codes Huffman

# Calcul de la taille avant compression (en bits)
original_size = len(text) * 8  # Taille en bits du texte original (1 caractère = 8 bits)

# Calcul de la taille après compression (en bits)
compressed_size_bits = sum(len(codes[char]) for char in text)  # Compter les bits dans la compression
compressed_size_bits_with_spaces = len(compressed_data.replace(" ", ""))  # Compter sans espaces

# Afficher les tailles
print(f"Taille originale : {original_size} bits")
print(f"Taille compressée (sans espaces) : {compressed_size_bits_with_spaces} bits")
print(f"Taille compressée (avec espaces) : {compressed_size_bits} bits")
print("Texte compressé avec espaces entre les caractères :", compressed_data)

# Décompresser le texte pour vérifier
decompressed_text = decompress(compressed_data.replace(" ", ""), huffman_tree)
print("Texte décompressé :", decompressed_text)


