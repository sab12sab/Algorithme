from typing import List, Optional
from datetime import datetime, time

# Classe pour représenter une tâche
class Task:
    def __init__(
        self,
        name: str,
        duration: int,
        priority: int,
        dependencies: List[str] = None,
        deadline: Optional[datetime] = None,
        time_window: Optional[List[time]] = None,
    ):
        """
        Modèle pour une tâche avec ses caractéristiques principales.

        :param name: Nom de la tâche (ex: "Développer le backend")
        :param duration: Durée en heures nécessaires pour exécuter la tâche
        :param priority: Niveau de priorité de la tâche (ex: 10 = très urgent, 1 = peu urgent)
        :param dependencies: Liste des noms de tâches nécessaires avant de commencer celle-ci
        :param deadline: Date limite pour finir la tâche (optionnel)
        :param time_window: Plage horaire autorisée pour la tâche (ex: [9:00, 17:00])
        """
        self.name = name
        self.duration = duration
        self.priority = priority
        self.dependencies = dependencies or []  # Si aucune dépendance n'est spécifiée, on initialise une liste vide
        self.deadline = deadline
        self.time_window = time_window or []

    def __repr__(self):
        """Représentation lisible d'une tâche, utile pour le débogage ou l'affichage."""
        return f"Task({self.name}, {self.duration}, P{self.priority})"

# Classe pour représenter une ressource, par exemple une personne ou une machine
class Resource:
    def __init__(self, name: str, capacity: int):
        """
        Modèle pour une ressource qui peut exécuter des tâches.

        :param name: Nom de la ressource (ex: "Machine A" ou "Développeur 1")
        :param capacity: Nombre maximal de tâches que la ressource peut gérer en parallèle
        """
        self.name = name
        self.capacity = capacity

    def __repr__(self):
        """Représentation lisible d'une ressource."""
        return f"Resource({self.name}, Capacity={self.capacity})"
