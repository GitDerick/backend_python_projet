from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.symptom_controller import SymptomController

symptom_view = Blueprint('symptom_view', __name__)

@symptom_view.route('/submit_symptoms', methods=['POST'])
@jwt_required()  # Réactiver l'authentification JWT si vous l'utilisez
def submit_symptoms():
    patient_id = get_jwt_identity()  # Récupérer l'ID du patient connecté
    data = request.form.to_dict()  # Récupérer les données textuelles du formulaire
    files = request.files.getlist('files')  # Récupérer les fichiers téléversés (s'il y en a)

    # Appeler le contrôleur pour soumettre les symptômes et fichiers
    response, status_code = SymptomController.submit_symptoms(data, files, patient_id)
    return jsonify(response), status_code


# Route pour récupérer tous les symptômes et les fichiers associés
@symptom_view.route('/get_symptoms', methods=['GET'])
def get_symptoms():
    # Appeler la fonction du contrôleur pour obtenir les symptômes et les fichiers
    symptoms = SymptomController.get_all_symptoms_and_files()
    
    # Retourner les données sous forme de JSON
    return jsonify(symptoms), 200

# Route pour supprimer un formulaire de symptômes
@symptom_view.route('/symptom/<symptom_id>', methods=['DELETE'])
@jwt_required()  # Assurez-vous que l'utilisateur est authentifié
def delete_symptom(symptom_id):
    success = SymptomController.delete_symptom(symptom_id)
    if success:
        return jsonify({"message": "Formulaire supprimé avec succès"}), 200
    else:
        return jsonify({"message": "Échec de la suppression du formulaire"}), 400