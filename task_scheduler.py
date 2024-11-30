class Task:
    def __init__(self, name, duration, priority):
        self.name = name
        self.duration = duration  # Durée de la tâche
        self.priority = priority  # Priorité de la tâche
        self.assigned_to = None  # Ressource à laquelle la tâche est assignée
        self.start_time = None  # Heure de début
        self.end_time = None  # Heure de fin

    def __repr__(self):
        return f"Task(name={self.name}, duration={self.duration}, priority={self.priority})"


class Resource:
    def __init__(self, name):
        self.name = name  # Nom de la ressource (machine, personne, etc.)
        self.available_at = 0  # La ressource est disponible à partir de ce temps

    def __repr__(self):
        return f"Resource(name={self.name})"

# Algorithme glouton par durée minimale
def greedy_by_duration(tasks, resources):
    tasks_sorted = sorted(tasks, key=lambda x: x.duration)  # Trier par durée
    schedule = []

    for task in tasks_sorted:
        # Trouver la ressource qui sera disponible le plus tôt
        available_resource = min(resources, key=lambda r: r.available_at)
        
        # Si la ressource est disponible avant la tâche, on commence dès qu'elle est disponible
        task.start_time = available_resource.available_at
        task.end_time = task.start_time + task.duration
        
        # Attribuer la ressource et mettre à jour son temps de disponibilité
        task.assigned_to = available_resource
        available_resource.available_at = task.end_time
        
        schedule.append(task)

    return schedule

# Algorithme glouton par priorité
def greedy_by_priority(tasks, resources):
    tasks_sorted = sorted(tasks, key=lambda x: x.priority, reverse=True)  # Trier par priorité
    schedule = []

    for task in tasks_sorted:
        # Trouver la ressource qui sera disponible le plus tôt
        available_resource = min(resources, key=lambda r: r.available_at)
        
        # Si la ressource est disponible avant la tâche, on commence dès qu'elle est disponible
        task.start_time = available_resource.available_at
        task.end_time = task.start_time + task.duration
        
        # Attribuer la ressource et mettre à jour son temps de disponibilité
        task.assigned_to = available_resource
        available_resource.available_at = task.end_time
        
        schedule.append(task)

    return schedule
