from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.consultation_controller import ConsultationController

consultation_view = Blueprint('consultation_view', __name__)

# Pour le Docteur
@consultation_view.route('/doctor/create_remote_consultation', methods=['POST'])
@jwt_required()  # Le médecin doit être authentifié
def create_remote_consultation():
    doctor_id = get_jwt_identity()  # Récupérer l'ID du médecin connecté
    doctor_name = request.json.get('doctor_name')
    patient_id = request.json.get('patient_id')
    date = request.json.get('date')  # Format: "YYYY-MM-DD"
    time = request.json.get('time')  # Format: "HH:MM"
    notes = request.json.get('notes', "")

    # Créer une consultation à distance
    consultation_id, video_link = ConsultationController.create_remote_consultation(
        patient_id, doctor_id, doctor_name, date, time, notes
    )

    return jsonify({
        "message": "Consultation à distance créée avec succès",
        "consultation_id": consultation_id,
        "video_link": video_link
    }), 201


# Pour le patient
@consultation_view.route('/patient/remote_consultations', methods=['GET'])
@jwt_required()  # Le patient doit être authentifié
def get_remote_consultations():
    patient_id = get_jwt_identity()  # Récupérer l'ID du patient connecté

    # Récupérer toutes les consultations à distance du patient
    consultations = ConsultationController.get_remote_consultations_by_patient(patient_id)

    return jsonify(consultations), 200


# Pour le docteur
@consultation_view.route('/doctor/remote_consultations', methods=['GET'])
@jwt_required()  # Le docteur doit être authentifié
def get_all_consultations():
    doctor_id = get_jwt_identity()  # Récupérer l'ID du docteur à partir du JWT
    consultations = ConsultationController.get_consultations_by_doctor(doctor_id)
    return jsonify(consultations), 200



@consultation_view.route('/doctor/update_remote_consultation/<consultation_id>', methods=['PUT'])
@jwt_required()  # Le médecin doit être authentifié
def update_remote_consultation(consultation_id):
    data = request.json  # Récupérer les nouvelles données de la consultation
    success = ConsultationController.update_remote_consultation(consultation_id, data)
    if success:
        return jsonify({"message": "Consultation mise à jour avec succès"}), 200
    else:
        return jsonify({"message": "Échec de la mise à jour"}), 400


@consultation_view.route('/doctor/delete_remote_consultation/<consultation_id>', methods=['DELETE'])
@jwt_required()  # Le médecin doit être authentifié
def delete_remote_consultation(consultation_id):
    success = ConsultationController.delete_remote_consultation(consultation_id)

    if success:
        return jsonify({"message": "Consultation supprimée avec succès"}), 200
    else:
        return jsonify({"message": "Échec de la suppression de la consultation"}), 400
