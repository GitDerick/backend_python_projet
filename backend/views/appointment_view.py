from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.appointment_controller import AppointmentController

appointment_view = Blueprint('appointment_view', __name__)

# Route pour que le médecin récupère les symptômes d'un patient
@appointment_view.route('/doctor/patient_symptoms/<patient_id>', methods=['GET'])
@jwt_required()  # Le médecin doit être authentifié
def get_patient_symptoms(patient_id):
    symptoms = AppointmentController.get_patient_symptoms(patient_id)
    return jsonify(symptoms), 200



# # Route pour que le médecin ajoute un avis ou des instructions sur les symptômes du patient
# @consultation_view.route('/doctor/add_response/<symptom_id>', methods=['PUT'])
# @jwt_required()  # Le médecin doit être authentifié
# def add_doctor_response(symptom_id):
#     response = request.json.get('response')
#     success = ConsultationController.add_doctor_response(symptom_id, response)
#     if success:
#         return jsonify({"message": "Réponse ajoutée avec succès"}), 200
#     else:
#         return jsonify({"message": "Échec de l'ajout de la réponse"}), 400



# Route pour que le médecin réserve un rendez-vous pour un patient
@appointment_view.route('/doctor/create_appointment', methods=['POST'])
@jwt_required()  # Le médecin doit être authentifié
def create_appointment():
    patient_id = request.json.get("patient_id")
    submission_id = request.json.get("submission_id")  # Récupérer l'_id de la soumission
    doctor_id = get_jwt_identity()  # Récupérer l'ID du médecin connecté
    doctor_name = request.json.get("doctor_name")
    date = request.json.get("date")
    notes = request.json.get("notes", "")
    hospital_location = request.json.get("hospital_location")
    
    # Appel au contrôleur pour créer une consultation
    appointment_id = AppointmentController.create_appointment(patient_id, doctor_id, doctor_name, submission_id, date, hospital_location, notes)
    return jsonify({"appointment_id": appointment_id}), 201


@appointment_view.route('/doctor/update_appointment/<appointment_id>', methods=['PUT'])
@jwt_required()  # Le médecin doit être authentifié
def update_appointment(appointment_id):
    update_data = request.json  # Récupérer les données de mise à jour du rendez-vous
    success = AppointmentController.update_appointment(appointment_id, update_data)

    if success:
        return jsonify({"message": "Rendez-vous mis à jour avec succès"}), 200
    else:
        return jsonify({"message": "Échec de la mise à jour du rendez-vous"}), 400


@appointment_view.route('/doctor/delete_appointment/<appointment_id>', methods=['DELETE'])
@jwt_required()  # Le médecin doit être authentifié
def delete_appointment(appointment_id):
    success = AppointmentController.delete_appointment(appointment_id)

    if success:
        return jsonify({"message": "Rendez-vous supprimé avec succès"}), 200
    else:
        return jsonify({"message": "Échec de la suppression du rendez-vous"}), 400



# Route pour que le patient consulte ses rendez-vous
@appointment_view.route('/patient/appointments', methods=['GET'])
@jwt_required()  # Le patient doit être authentifié
def get_patient_appointments():
    patient_id = get_jwt_identity()  # Récupérer l'ID du patient connecté
    appointments = AppointmentController.get_patient_appointments(patient_id)
    return jsonify(appointments), 200



@appointment_view.route('/doctor/appointments', methods=['GET'])
@jwt_required()  # Le docteur doit être authentifié
def get_doctor_appointments():
    doctor_id = get_jwt_identity()  # Récupérer l'ID du docteur connecté
    print(f"Doctor ID récupéré : {doctor_id}")  # Trace pour voir l'ID du docteur

    appointments = AppointmentController.get_doctor_appointments(doctor_id)
    
    if not appointments:
        print("Aucun rendez-vous trouvé pour ce docteur.")
    else:
        print(f"Rendez-vous récupérés pour le docteur : {appointments}")  # Tracer les rendez-vous récupérés

    return jsonify(appointments), 200


# Route pour que le docteur consulte les rendez-vous d un patient
@appointment_view.route('/appointments/patient/<int:patient_id>', methods=['GET'])
@jwt_required()  # Le médecin ou utilisateur doit être authentifié
def get_patient_appointments_by_id(patient_id):
    try:
        # Appel au contrôleur pour récupérer les rendez-vous du patient
        appointments = AppointmentController.get_patient_appointments_by_id(patient_id)
        
        if appointments:
            return jsonify({"appointments": appointments}), 200
        else:
            return jsonify({"message": "Aucun rendez-vous trouvé pour ce patient"}), 404
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la récupération des rendez-vous: {str(e)}"}), 500
