from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from controllers.doctor_inscription_controller import DoctorController

# Création du blueprint pour l'inscription des docteurs
doctor_inscription_view = Blueprint('doctor_inscription_view', __name__)

# Route pour l'inscription des docteurs
@doctor_inscription_view.route('/doctor/register_doctor', methods=['POST'])
def register_doctor():
    return DoctorController.register_doctor()

# Route pour vérifier l'email
@doctor_inscription_view.route('/doctor/verify_email/<token>', methods=['GET'])
def verify_email(token):
    return DoctorController.verify_email(token)

# Route pour la connexion des docteurs
@doctor_inscription_view.route('/doctor/login_doctor', methods=['POST'])
def login_doctor():
    return DoctorController.login_doctor()

# Route pour créer le token de rafraîchissement
@doctor_inscription_view.route('/doctor/refresh', methods=['POST'])
@jwt_required(refresh=True)  # Cette route nécessite un token de rafraîchissement
def refresh_access_token():
    current_doctor = get_jwt_identity()  # Récupérer l'identité depuis le token de rafraîchissement
    new_access_token = create_access_token(identity=current_doctor)  # Générer un nouveau token d'accès
    
    return jsonify({"access_token": new_access_token}), 200



# Route pour modifier les informations personnelles d'un docteur
@doctor_inscription_view.route('/doctor/update/<int:doctor_id>', methods=['PUT'])
def update_doctor_info(doctor_id):
    return DoctorController.update_doctor(doctor_id)


@doctor_inscription_view.route('/doctor/<int:doctor_id>', methods=['GET'])
#@jwt_required()  # Protéger avec JWT
def get_doctor(doctor_id):
    return DoctorController.get_doctor(doctor_id)


# Route pour récupérer tous les symptômes de tous les patients
@doctor_inscription_view.route('/doctor/Allsymptoms', methods=['GET'])
@jwt_required()  # Protéger avec JWT
def get_all_patients_symptoms():
    return DoctorController.get_all_patients_symptoms()

# Route pour que le médecin accède aux symptômes d'un patient via l'ID unique des symptômes
@doctor_inscription_view.route('/doctor/patient_symptom/<symptom_id>', methods=['GET'])
@jwt_required()  # Le médecin doit être authentifié
def get_symptom_by_id(symptom_id):
    symptom = DoctorController.get_symptom_by_id(symptom_id)
    return jsonify(symptom), 200


