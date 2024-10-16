from flask import Blueprint, request, jsonify
from controllers.patient_controller import PatientController
from flask_jwt_extended import jwt_required  # Pour protéger certaines routes
from flask_jwt_extended import jwt_required, get_jwt_identity

# Blueprint pour les opérations CRUD des patients
patient_view = Blueprint('patient_view', __name__)

# Blueprint pour l'authentification des patients
auth_view = Blueprint('patient_auth_view', __name__)

@patient_view.route('/patients', methods=['POST'])
def create_patient():
    data = request.json
    return PatientController.create_patient(data)

@patient_view.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    data = request.json
    return PatientController.update_patient(patient_id, data)

@patient_view.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    return PatientController.delete_patient(patient_id)

@patient_view.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    print(f"Received request for patient ID: {patient_id}")
    return PatientController.get_patient(patient_id)



@auth_view.route('/login/patient', methods=['POST'])
def login():
    data = request.json

    # Vérifier si les champs email et password sont fournis
    if not data.get('email') or not data.get('password'):
        return jsonify({"message": "Email et mot de passe requis"}), 400

    # Appel au contrôleur pour l'authentification
    access_token, error_message, patient_id = PatientController.authenticate_patient(data['email'], data['password'])

    if error_message:
        return jsonify({"message": error_message}), 401

    return jsonify(access_token=access_token, id=patient_id), 200


# Route pour récupérer l'historique médical du patient
@patient_view.route('/patient/medical_history', methods=['GET'])
@jwt_required()  # Nécessite que le patient soit authentifié
def get_medical_history():
    patient_id = get_jwt_identity()  # Récupérer l'ID du patient connecté
    history = PatientController.get_medical_history(patient_id)
    return jsonify(history), 200


# Route pour que le patient accède aux symptômes d'un patient
@patient_view.route('/patient/doctor_response/<patient_id>', methods=['GET'])
@jwt_required()  # Le patient doit être authentifié
def get_patient_symptoms(patient_id):
    symptoms = PatientController.get_patient_symptoms(patient_id)
    return jsonify(symptoms), 200