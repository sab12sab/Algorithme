import plotly.express as px
import pandas as pd

# Générer un diagramme de Gantt interactif
def generate_gantt_chart(schedule):
    """
    Génère un diagramme de Gantt interactif pour visualiser le planning.

    :param schedule: Planning sous forme de dictionnaire {ressource: [tâches]}
    :return: Objet graphique Plotly
    """
    data = []
    for resource, tasks in schedule.items():
        start_time = 0  # Temps de départ initial pour chaque ressource
        for task in tasks:
            # Ajouter les informations pour chaque tâche
            data.append({
                "Task": task.name,
                "Start": start_time,
                "Finish": start_time + task.duration,
                "Resource": resource,
            })
            start_time += task.duration  # Avancer le temps de début pour la ressource

    # Convertir les données en DataFrame pour Plotly
    df = pd.DataFrame(data)
    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Resource",
        color="Task",
        title="Diagramme de Gantt",
    )
    fig.update_yaxes(categoryorder="total ascending")  # Trier les ressources par ordre
    return fig
