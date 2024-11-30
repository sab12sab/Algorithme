import streamlit as st
from models import Task, Resource
from scheduler import (
    schedule_by_shortest_duration,
    schedule_by_highest_priority,
    schedule_with_dependencies,
)
from utils import generate_gantt_chart

# Initialisation des sessions
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "resources" not in st.session_state:
    st.session_state.resources = []

# Titre principal
st.title("Planificateur de Tâches avec Algorithmes Gloutons")

# Section pour ajouter des ressources
st.header("Ajouter des ressources")
resource_name = st.text_input("Nom de la ressource")
resource_capacity = st.number_input("Capacité (nombre de tâches)", min_value=1, step=1)
if st.button("Ajouter la ressource"):
    st.session_state.resources.append(Resource(resource_name, resource_capacity))
    st.success(f"Ressource {resource_name} ajoutée avec capacité {resource_capacity}.")

# Section pour ajouter des tâches
st.header("Ajouter des tâches")
task_name = st.text_input("Nom de la tâche")
task_duration = st.number_input("Durée (heures)", min_value=1, step=1)
task_priority = st.slider("Priorité", min_value=1, max_value=10)
task_dependencies = st.multiselect(
    "Dépendances (nom des tâches nécessaires avant celle-ci)",
    [t.name for t in st.session_state.tasks]
)

if st.button("Ajouter la tâche"):
    st.session_state.tasks.append(Task(task_name, task_duration, task_priority, task_dependencies))
    st.success(f"Tâche {task_name} ajoutée avec dépendances : {', '.join(task_dependencies)}")

# Afficher les données ajoutées
st.subheader("Tâches ajoutées")
for t in st.session_state.tasks:
    st.write(f"{t.name} - Durée: {t.duration}h, Priorité: {t.priority}, Dépendances: {', '.join(t.dependencies)}")

st.subheader("Ressources ajoutées")
for r in st.session_state.resources:
    st.write(f"{r.name} - Capacité: {r.capacity} tâches")

# Choisir l'algorithme d'ordonnancement
st.header("Choisir l'algorithme d'ordonnancement")
algorithm = st.selectbox(
    "Sélectionnez un algorithme",
    ["Ordonnancement par durée minimale", "Ordonnancement par priorité maximale", "Ordonnancement avec dépendances"],
)

# Appliquer l'algorithme choisi
if st.button("Planifier"):
    if algorithm == "Ordonnancement par durée minimale":
        schedule = schedule_by_shortest_duration(st.session_state.tasks, st.session_state.resources)
    elif algorithm == "Ordonnancement par priorité maximale":
        schedule = schedule_by_highest_priority(st.session_state.tasks, st.session_state.resources)
    else:
        schedule = schedule_with_dependencies(st.session_state.tasks, st.session_state.resources)

    # Générer et afficher le diagramme de Gantt
    fig = generate_gantt_chart(schedule)
    st.plotly_chart(fig)
