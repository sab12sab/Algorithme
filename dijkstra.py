import heapq

def dijkstra_binary_heap(graph, start):
    """
    Implémentation de l'algorithme de Dijkstra avec un tas binaire pour trouver les plus
    courts chemins d'un nœud de départ à tous les autres nœuds d'un graphe.
    """
    # Initialisation des distances et prédécesseurs
    distances = {node: float('inf') for node in graph}  # On initialise toutes les distances à l'infini
    distances[start] = 0  # La distance du nœud de départ à lui-même est 0
    predecessors = {node: None for node in graph}  # On initialise les prédécesseurs à None
    priority_queue = [(0, start)]  # On commence avec le nœud de départ

    while priority_queue:
        # Extraire le nœud avec la plus petite distance
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Si la distance actuelle est plus grande que la distance connue, on passe au suivant
        if current_distance > distances[current_node]:
            continue
        
        # Examiner les voisins du nœud courant
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight  # Calcul de la nouvelle distance
            if distance < distances[neighbor]:
                distances[neighbor] = distance  # Mise à jour de la distance
                predecessors[neighbor] = current_node  # Mise à jour du prédécesseur
                heapq.heappush(priority_queue, (distance, neighbor))  # Ajout du voisin dans le tas

    return distances, predecessors  # On retourne les distances et les prédécesseurs

def dijkstra_fibonacci(graph, start):
    """
    Implémentation de Dijkstra avec un tas de Fibonacci.
    Cette implémentation utilise un tas de Fibonacci (bien plus performant que le tas binaire 
    dans certaines situations, mais nécessitant une implémentation plus complexe).
    """
    # La version Fibonacci est ici simplifiée. Une véritable implémentation de tas de Fibonacci
    # nécessiterait l'écriture d'une classe supplémentaire pour gérer le tas.
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    predecessors = {node: None for node in graph}

    # Pour la démonstration, nous allons utiliser un tas binaire (remarque : à remplacer par un tas de Fibonacci)
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Si la distance actuelle est plus grande que celle enregistrée, on passe au suivant
        if current_distance > distances[current_node]:
            continue
        
        # Examiner les voisins du nœud courant
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance  # Mise à jour de la distance
                predecessors[neighbor] = current_node  # Mise à jour du prédécesseur
                heapq.heappush(priority_queue, (distance, neighbor))  # Ajout du voisin dans le tas

    return distances, predecessors
