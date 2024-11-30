# Implémentation d'un Tas de Fibonacci
import math

class FibonacciHeap:
    # Classe interne Node pour représenter un nœud dans le Tas de Fibonacci
    class Node:
        def __init__(self, key):
            self.key = key  # Clé du nœud
            self.degree = 0  # Degré du nœud (nombre d'enfants)
            self.parent = None  # Parent du nœud
            self.child = None  # Enfant du nœud
            self.marked = False  # Indicateur de coupure
            self.next = None  # Lien vers le nœud suivant
            self.prev = None  # Lien vers le nœud précédent

    def __init__(self):
        self.min_node = None  # Nœud minimum du tas
        self.num_nodes = 0  # Nombre de nœuds dans le tas

    def insert(self, key):
        """
        Insère un nouveau nœud avec une clé donnée dans le Tas de Fibonacci.
        """
        node = self.Node(key)
        if not self.min_node:
            self.min_node = node  # Si le tas est vide, le nœud devient le minimum
            node.next = node
            node.prev = node
        else:
            # Ajout du nœud à la liste circulaire des racines
            node.next = self.min_node
            node.prev = self.min_node.prev
            self.min_node.prev.next = node
            self.min_node.prev = node
            if key < self.min_node.key:
                self.min_node = node  # Mettre à jour le nœud minimum si nécessaire
        self.num_nodes += 1
        return node

    def delete_min(self):
        """
        Supprime et retourne le nœud avec la clé minimale du Tas de Fibonacci.
        """
        min_node = self.min_node
        if min_node:
            # Si le nœud minimum a des enfants, les ajouter à la racine du tas
            if min_node.child:
                child = min_node.child
                while child:
                    temp = child
                    child = child.next
                    self.insert(temp.key)
            # Retirer le nœud minimum de la liste
            if min_node.next == min_node:
                self.min_node = None  # Si le tas ne contient plus de nœuds
            else:
                self.min_node = min_node.next
            self.num_nodes -= 1
        return min_node

    def decrease_key(self, node, new_key):
        """
        Réduit la clé d'un nœud donné et effectue les coupures nécessaires si la clé du nœud
        devient plus petite que celle de son parent.
        """
        if new_key > node.key:
            raise ValueError("New key is greater than current key.")
        node.key = new_key
        parent = node.parent
        if parent and node.key < parent.key:
            # Si la clé du nœud devient plus petite que celle de son parent, effectuer une coupure
            self._cut(node, parent)
            self._cascading_cut(parent)
        if node.key < self.min_node.key:
            self.min_node = node  # Mettre à jour le nœud minimum si nécessaire

    def _cut(self, node, parent):
        """
        Effectue une coupure entre un nœud et son parent dans le Tas de Fibonacci.
        """
        if node.next == node:
            parent.child = None
        else:
            parent.child = node.next
        node.prev.next = node.next
        node.next.prev = node.prev
        parent.degree -= 1
        node.next = self.min_node
        node.prev = self.min_node.prev
        self.min_node.prev.next = node
        self.min_node.prev = node
        node.parent = None
        node.marked = False

    def _cascading_cut(self, node):
        """
        Effectue une coupure en cascade si nécessaire.
        """
        parent = node.parent
        if parent:
            if not node.marked:
                node.marked = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)

    def is_empty(self):
        """
        Retourne True si le tas est vide, sinon False.
        """
        return self.num_nodes == 0
