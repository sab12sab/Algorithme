import heapq
from collections import defaultdict

# Fonction pour calculer la fréquence des caractères
def calculate_frequency(text):
    frequency = defaultdict(int)
    for char in text:
        frequency[char] += 1
    return frequency

# Classe pour représenter un nœud dans l'arbre de Huffman
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Définir l'ordre de comparaison pour les nœuds dans le tas (par fréquence)
    def __lt__(self, other):
        return self.freq < other.freq

# Fonction pour créer l'arbre de Huffman
def create_huffman_tree(frequency):
    # Vérifier si la fréquence est vide
    if not frequency:
        raise ValueError("Le texte est vide. Impossible de créer un arbre de Huffman.")

    # Créer un tas de nœuds
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    # Construire l'arbre de Huffman
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        # Créer un nœud interne avec les deux nœuds comme enfants
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        # Ajouter ce nœud au tas
        heapq.heappush(heap, merged)

    # Retourner le seul nœud restant, qui est la racine de l'arbre
    return heap[0] if heap else None  # Vérification si heap n'est pas vide

# Fonction de compression de Huffman
def huffman_compress(text):
    # Calculer la fréquence des caractères
    frequency = calculate_frequency(text)
    
    # Créer l'arbre de Huffman
    tree = create_huffman_tree(frequency)
    
    # Générer le code binaire pour chaque caractère
    huffman_codes = {}
    generate_huffman_codes(tree, "", huffman_codes)

    # Encoder le texte avec les codes de Huffman
    encoded_data = "".join(huffman_codes[char] for char in text)
    
    return encoded_data, tree  # Retourner les données compressées et l'arbre

# Fonction pour générer les codes de Huffman à partir de l'arbre
def generate_huffman_codes(node, current_code, huffman_codes):
    if node is not None:
        if node.char is not None:
            huffman_codes[node.char] = current_code
        generate_huffman_codes(node.left, current_code + "0", huffman_codes)
        generate_huffman_codes(node.right, current_code + "1", huffman_codes)

# Fonction pour décompresser les données Huffman
def huffman_decompress(encoded_data, tree):
    decoded_data = []
    current_node = tree
    for bit in encoded_data:
        current_node = current_node.left if bit == '0' else current_node.right
        if current_node.char is not None:
            decoded_data.append(current_node.char)
            current_node = tree  # Revenir à la racine après avoir trouvé un caractère
    return "".join(decoded_data)
