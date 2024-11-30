import streamlit as st
from search_engine import SearchEngine
from huffman import calculate_frequency, build_huffman_tree, generate_codes, compress, decompress
from task_scheduler import Task, Resource, greedy_by_duration, greedy_by_priority, greedy_by_duration_and_priority
import tempfile  # Pour créer un fichier temporaire
import matplotlib.pyplot as plt



# --- Interface Streamlit ---
st.sidebar.title("Choisissez une fonction")
option = st.sidebar.selectbox("Options", ["Moteur de Recherche", "Compression de Fichiers", "Planificateur de Tâches"])


# --- Moteur de Recherche ---
if option == "Moteur de Recherche":
    st.title("Moteur de Recherche Simplifié")
    
    uploaded_files = st.file_uploader("Téléchargez vos fichiers texte (.txt)", type=["txt"], accept_multiple_files=True)
    
    search_engine = SearchEngine()
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            content = uploaded_file.read().decode("utf-8")
            search_engine.index_document(uploaded_file.name, content)
        st.success(f"{len(uploaded_files)} fichier(s) indexé(s).")
    
    query = st.text_input("Entrez votre requête :")
    operator = st.radio("Choisissez un opérateur :", ["ET", "OU"])
    fuzzy = st.checkbox("Activer la recherche floue")
    
    if st.button("Rechercher"):
        if query:
            results = search_engine.search(query, operator=operator, fuzzy=fuzzy)
            if results:
                st.write("Documents trouvés :")
                for result in results:
                    st.write(f"- {result}")
            else:
                st.write("Aucun document trouvé pour votre recherche.")

# --- Compression Huffman ---
elif option == "Compression de Fichiers":
    st.title("Compression de Fichiers avec Huffman")
    
    uploaded_file = st.file_uploader("Téléchargez un fichier texte", type=["txt"])
    if uploaded_file:
        text = uploaded_file.read().decode("utf-8")
        st.write("Contenu du fichier :")
        st.text_area("Texte brut", text, height=200)
        
        # Compression
        frequencies = calculate_frequency(text)
        huffman_tree = build_huffman_tree(frequencies)
        codes = generate_codes(huffman_tree)
        compressed_data = compress(text, codes)
        
        st.write("Taille compressée :", len(compressed_data))
        st.write("Taux de compression :", len(compressed_data) / (len(text) * 8))

        # Visualiser le fichier compressé sous forme binaire
        st.write("Contenu compressé :")
        st.text_area("Données compressées (binaire)", compressed_data, height=200)

        # Créer un fichier temporaire pour le téléchargement
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix=".bin") as temp_file:
            temp_file.write(compressed_data)
            temp_file_path = temp_file.name
        
        # Bouton de téléchargement
        st.download_button(
            label="Télécharger le fichier compressé",
            data=compressed_data,
            file_name=f"{uploaded_file.name}.bin",
            mime="application/octet-stream"
        )

        # Décompression
        if st.button("Décompresser"):
            decompressed_text = decompress(compressed_data, huffman_tree)
            st.text_area("Texte décompressé", decompressed_text, height=200)


elif option == "Planificateur de Tâches":
    st.title("Planificateur de Tâches avec Algorithmes Gloutons")

    # Formulaire pour entrer les ressources
    resources_input = st.text_area("Entrez les ressources séparées par une virgule", "Ressource1, Ressource2, Ressource3")
    resources_names = resources_input.split(",")
    resources = [Resource(name.strip()) for name in resources_names]

    # Formulaire pour entrer les tâches
    tasks_input = st.text_area("Entrez les tâches au format 'Nom, Durée, Priorité, Durée maximale (optionnel)'", 
                               "Tâche 1, 3, 2, 5\nTâche 2, 1, 1\nTâche 3, 4, 3, 6")
    tasks_lines = tasks_input.split("\n")
    tasks = []

    for line in tasks_lines:
        task_details = line.split(",")
        task_name = task_details[0].strip()
        duration = int(task_details[1].strip())
        priority = int(task_details[2].strip())
        max_duration = int(task_details[3].strip()) if len(task_details) > 3 else None
        tasks.append(Task(task_name, duration, priority, max_duration))

    # Choix de l'algorithme
    algorithm = st.selectbox("Choisissez l'algorithme de planification", ["Par Durée Minimale", "Par Priorité", "Par Durée et Priorité"])

    if st.button("Planifier"):
        if algorithm == "Par Durée Minimale":
            schedule = greedy_by_duration(tasks, resources)
        elif algorithm == "Par Priorité":
            schedule = greedy_by_priority(tasks, resources)
        else:
            schedule = greedy_by_duration_and_priority(tasks, resources)

        # Affichage du planning
        st.write("Planning des tâches :")
        for task in schedule:
            st.write(f"{task.name} - Début: {task.start_time} - Fin: {task.end_time} - Assignée à: {task.assigned_to.name}")

        # Visualiser le planning des ressources avec un graphique
        fig, ax = plt.subplots()
        for resource in resources:
            ax.plot([task.start_time for task in schedule if task.assigned_to == resource],
                    [task.end_time for task in schedule if task.assigned_to == resource], label=resource.name)

        ax.set_xlabel("Temps")
        ax.set_ylabel("Tâches")
        ax.set_title("Planning des Ressources")
        ax.legend()
        st.pyplot(fig)