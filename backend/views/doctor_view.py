from flask import Blueprint, request, jsonify
from controllers.doctor_controller import DoctorController
from flask_jwt_extended import jwt_required, get_jwt_identity

doctor_view = Blueprint('doctor_view', __name__)
authDoc_view = Blueprint('doctor_auth_view', __name__)

@doctor_view.route('/doctors', methods=['POST'])
def create_doctor():
    data = request.json
    return DoctorController.create_doctor(data)


@doctor_view.route('/doctors/<int:doctor_id>', methods=['GET'])
@jwt_required()  # Protéger avec JWT
def get_doctor(doctor_id):
    return DoctorController.get_doctor(doctor_id)


@doctor_view.route('/doctors/<int:doctor_id>', methods=['PUT'])
#@jwt_required()  # Protéger avec JWT
def update_doctor(doctor_id):
    data = request.json
    return DoctorController.update_doctor(doctor_id, data)


@doctor_view.route('/doctors/<int:doctor_id>', methods=['DELETE'])
#@jwt_required()  # Protéger avec JWT
def delete_doctor(doctor_id):
    return DoctorController.delete_doctor(doctor_id)


@authDoc_view.route('/login/doctor', methods=['POST'])
def login():
    data = request.json

    # Vérifier si les champs email et password sont fournis
    if not data.get('email') or not data.get('password'):
        return jsonify({"message": "Email et mot de passe requis"}), 400

    # Appel au contrôleur pour l'authentification
    access_token, error_message = DoctorController.authenticate_doctor(data['email'], data['password'])

    if error_message:
        return jsonify({"message": error_message}), 401

    return jsonify(access_token=access_token), 200


# Route pour que le médecin accède aux symptômes d'un patient
@doctor_view.route('/doctor/patient_symptoms/<patient_id>', methods=['GET'])
@jwt_required()  # Le médecin doit être authentifié
def get_patient_symptoms(patient_id):
    symptoms = DoctorController.get_patient_symptoms(patient_id)
    return jsonify(symptoms), 200


@doctor_view.route('/doctor/add_response/<symptom_id>', methods=['PUT'])
@jwt_required()  # Le médecin doit être authentifié
def add_doctor_response(symptom_id):
    doctor_id = get_jwt_identity()  # Récupérer l'ID du médecin connecté
    doctor_name = request.json.get('doctor_name')  # Récupérer le nom du médecin

    # Récupérer les notes et instructions
    notes = request.json.get('notes')
    instructions = request.json.get('instructions')

    # Créer la réponse complète avec les informations du médecin
    response = {
        "doctor_id": doctor_id,
        "doctor_name": doctor_name,
        "notes": notes,
        "instructions": instructions,
        "status": "Instructions données"
    }

    # Appel au contrôleur pour ajouter la réponse
    success = DoctorController.add_doctor_response(symptom_id, response)
    if success:
        return jsonify({"message": "Réponse ajoutée avec succès"}), 200
    else:
        return jsonify({"message": "Échec de l'ajout de la réponse"}), 400


# Utilisation de _id au lieu de symptom_id #
@doctor_view.route('/doctor/update_response/<id>', methods=['PUT'])
@jwt_required()  # Le médecin doit être authentifié
def update_doctor_response(id):
    doctor_id = get_jwt_identity()  # Récupérer l'ID du médecin connecté
    doctor_name = request.json.get('doctor_name')  # Récupérer le nom du médecin

    # Récupérer les nouvelles notes et instructions
    notes = request.json.get('notes')
    instructions = request.json.get('instructions')

    # Créer la nouvelle réponse avec les informations mises à jour
    response_update = {
        "doctor_id": doctor_id,
        "doctor_name": doctor_name,
        "notes": notes,
        "instructions": instructions,
        "status": "Réponse mise à jour"
    }

    # Appel au contrôleur pour mettre à jour la réponse
    success = DoctorController.update_doctor_response(id, response_update)
    if success:
        return jsonify({"message": "Réponse mise à jour avec succès"}), 200
    else:
        return jsonify({"message": "Échec de la mise à jour de la réponse"}), 400



@doctor_view.route('/doctor/delete_response/<id>', methods=['DELETE'])
@jwt_required()  # Le médecin doit être authentifié
def delete_doctor_response(id):
    # Appeler le contrôleur pour supprimer la réponse du médecin
    success = DoctorController.delete_doctor_response(id)
    if success:
        return jsonify({"message": "Réponse supprimée avec succès"}), 200
    else:
        return jsonify({"message": "Échec de la suppression de la réponse"}), 400
