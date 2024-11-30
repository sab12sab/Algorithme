import heapq
from collections import defaultdict

# Fonction pour calculer la fréquence des caractères dans le texte
def calculate_frequencies(data):
    """
    Cette fonction prend en entrée une chaîne de texte et renvoie un dictionnaire
    avec les caractères comme clés et leurs fréquences comme valeurs.
    """
    frequency = defaultdict(int)
    for char in data:
        frequency[char] += 1
    return frequency

# Classe pour représenter un nœud de l'arbre de Huffman
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char  # Le caractère dans ce nœud
        self.freq = freq  # La fréquence du caractère
        self.left = None   # Sous-arbre gauche
        self.right = None  # Sous-arbre droit
    
    def __lt__(self, other):
        """
        Redéfinir l'opérateur < pour permettre de trier les nœuds par fréquence dans un tas.
        """
        return self.freq < other.freq

# Fonction pour créer l'arbre de Huffman
def create_huffman_tree(frequency):
    """
    Cette fonction crée l'arbre de Huffman en utilisant un tas de priorité
    pour fusionner les nœuds jusqu'à ce qu'il n'en reste qu'un.
    """
    # Créer un tas de nœuds Huffman à partir des fréquences
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    # Fusionner les nœuds jusqu'à ce qu'il n'en reste qu'un seul
    while len(heap) > 1:
        left = heapq.heappop(heap)  # Extraire le nœud avec la plus petite fréquence
        right = heapq.heappop(heap) # Extraire le nœud suivant
        merged = HuffmanNode(None, left.freq + right.freq)  # Créer un nœud parent
        merged.left = left  # Sous-arbre gauche
        merged.right = right  # Sous-arbre droit
        heapq.heappush(heap, merged)  # Ajouter le nœud fusionné au tas

    # Le seul nœud restant dans le tas est la racine de l'arbre de Huffman
    return heap[0]

# Fonction pour générer les codes Huffman à partir de l'arbre
def generate_huffman_codes(tree, prefix='', codebook=None):
    """
    Cette fonction génère les codes binaires pour chaque caractère en traversant
    l'arbre de Huffman de manière récursive.
    """
    if codebook is None:
        codebook = {}  # Initialiser le dictionnaire des codes Huffman
    
    # Si nous atteignons une feuille, assigner le code à ce caractère
    if tree.char is not None:
        codebook[tree.char] = prefix
    else:
        # Si ce n'est pas une feuille, continuer la récursion sur les sous-arbres
        generate_huffman_codes(tree.left, prefix + '0', codebook)  # Sous-arbre gauche
        generate_huffman_codes(tree.right, prefix + '1', codebook)  # Sous-arbre droit

    return codebook

# Fonction pour compresser les données avec l'algorithme de Huffman
def huffman_compress(data):
    """
    Cette fonction compresse les données en générant un arbre de Huffman
    et en remplaçant chaque caractère par son code binaire.
    """
    frequency = calculate_frequencies(data)  # Calculer les fréquences des caractères
    tree = create_huffman_tree(frequency)  # Créer l'arbre de Huffman
    huffman_codes = generate_huffman_codes(tree)  # Générer les codes Huffman
    
    # Compresser le texte avec les codes générés
    compressed_data = ''.join(huffman_codes[char] for char in data)
    return compressed_data, tree

# Fonction pour décompresser les données avec l'arbre de Huffman
def huffman_decompress(compressed_data, tree):
    """
    Cette fonction décompresse les données en suivant les codes binaires
    et en naviguant dans l'arbre de Huffman.
    """
    current_node = tree  # Commencer à la racine de l'arbre
    decompressed_data = []  # Liste pour stocker les données décompressées

    # Parcourir les bits compressés et naviguer dans l'arbre de Huffman
    for bit in compressed_data:
        if bit == '0':
            current_node = current_node.left  # Aller à gauche si le bit est '0'
        else:
            current_node = current_node.right  # Aller à droite si le bit est '1'
        
        # Si un caractère est trouvé (nœud feuille), l'ajouter à la sortie
        if current_node.char is not None:
            decompressed_data.append(current_node.char)
            current_node = tree  # Retourner à la racine pour le prochain caractère
    
    return ''.join(decompressed_data)
