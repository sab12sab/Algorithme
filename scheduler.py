from typing import List
from models import Task, Resource

# Fonction pour résoudre les dépendances entre tâches
def resolve_dependencies(tasks: List[Task]) -> List[Task]:
    """
    Trie les tâches en respectant leurs dépendances.

    Utilise un algorithme récursif pour vérifier que chaque tâche est exécutée
    uniquement après que ses dépendances aient été satisfaites.

    :param tasks: Liste de tâches à ordonner
    :return: Liste triée des tâches selon leurs dépendances
    """
    resolved = []  # Liste finale des tâches triées
    unresolved = []  # Tâches en cours d'exploration

    def resolve(task, resolved, unresolved):
        """
        Sous-fonction récursive pour trier les dépendances.
        :param task: Tâche actuelle à résoudre
        """
        if task in resolved:
            return  # Si la tâche est déjà résolue, on passe
        if task in unresolved:
            raise ValueError(f"Dépendance circulaire détectée : {task.name}")
        unresolved.append(task)  # Marquer comme en cours de traitement
        for dep_name in task.dependencies:
            # Trouver la tâche correspondant au nom dans les dépendances
            dep_task = next((t for t in tasks if t.name == dep_name), None)
            if dep_task:
                resolve(dep_task, resolved, unresolved)
        unresolved.remove(task)  # Retirer des tâches en cours
        resolved.append(task)  # Ajouter aux tâches résolues

    for task in tasks:
        resolve(task, resolved, unresolved)

    return resolved

# Fonction pour assigner des tâches à des ressources
def assign_tasks_to_resources(tasks: List[Task], resources: List[Resource]):
    """
    Assigne les tâches aux ressources disponibles en tenant compte de leur capacité.

    :param tasks: Liste de tâches triées par un critère (durée, priorité, etc.)
    :param resources: Liste des ressources disponibles
    :return: Dictionnaire avec les ressources comme clés et les tâches assignées comme valeurs
    """
    schedule = {resource.name: [] for resource in resources}  # Initialisation du planning
    for task in tasks:
        for resource in resources:
            # Vérifie si la ressource a encore de la capacité pour une nouvelle tâche
            if len(schedule[resource.name]) < resource.capacity:
                schedule[resource.name].append(task)
                break  # Une fois assignée, on passe à la tâche suivante
    return schedule

# Ordonnancement par durée minimale
def schedule_by_shortest_duration(tasks: List[Task], resources: List[Resource]):
    """
    Trie les tâches par durée croissante et les assigne aux ressources.
    :param tasks: Liste des tâches
    :param resources: Liste des ressources
    :return: Planning des tâches
    """
    tasks = sorted(tasks, key=lambda task: task.duration)  # Trier par durée croissante
    return assign_tasks_to_resources(tasks, resources)

# Ordonnancement par priorité maximale
def schedule_by_highest_priority(tasks: List[Task], resources: List[Resource]):
    """
    Trie les tâches par priorité décroissante et les assigne aux ressources.
    :param tasks: Liste des tâches
    :param resources: Liste des ressources
    :return: Planning des tâches
    """
    tasks = sorted(tasks, key=lambda task: task.priority, reverse=True)  # Trier par priorité décroissante
    return assign_tasks_to_resources(tasks, resources)

# Ordonnancement avec gestion des dépendances
def schedule_with_dependencies(tasks: List[Task], resources: List[Resource]):
    """
    Résout les dépendances avant d'assigner les tâches aux ressources.
    :param tasks: Liste des tâches
    :param resources: Liste des ressources
    :return: Planning des tâches
    """
    tasks = resolve_dependencies(tasks)  # Résoudre les dépendances
    return assign_tasks_to_resources(tasks, resources)
