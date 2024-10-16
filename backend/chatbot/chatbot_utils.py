# Par exemple, une fonction utilitaire pour ajuster les réponses en fonction du contexte
def adjust_response_based_on_context(response, doctor_id):
    # Logique pour personnaliser la réponse selon le médecin ou les données de contexte
    return f"Docteur {doctor_id}, voici votre rapport : {response}"

# Fonction pour vérifier l'intégrité des données fournies
def validate_data(data):
    if "report_text" not in data or "image_path" not in data:
        return False
    return True
