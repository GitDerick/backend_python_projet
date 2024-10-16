from models.doctor_model import DoctorModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from database import get_mongo_connection
from bson.objectid import ObjectId


class DoctorController:
    @staticmethod
    def create_doctor(data):

        if not all([data.get('first_name'), data.get('last_name'), data.get('email'), data.get('password'), data.get('specialization')]):
            return {"message": "Les informations du docteur sont incomplètes"}, 400
        
        hashed_password = generate_password_hash(data['password'])
        doctor_id = DoctorModel.create_doctor(
            data['first_name'],
            data['last_name'],
            data['email'],
            hashed_password,
            data['specialization']
        )
        return {"message": "Docteur créé avec succès", "doctor_id": doctor_id}, 201

    @staticmethod
    def get_doctor(doctor_id):
        doctor = DoctorModel.get_doctor_by_id(doctor_id)
        if doctor:
            return doctor, 200
        return {"message": "Docteur non trouvé"}, 404

    @staticmethod
    def update_doctor(doctor_id, data):
        if 'password' in data:
            data['password'] = generate_password_hash(data['password'])
        updated = DoctorModel.update_doctor(doctor_id, data)
        if updated:
            return {"message": "Docteur mis à jour avec succès"}, 200
        return {"message": "Docteur non trouvé"}, 404

    @staticmethod
    def delete_doctor(doctor_id):
        deleted = DoctorModel.delete_doctor(doctor_id)
        if deleted:
            return {"message": "Docteur supprimé avec succès"}, 200
        return {"message": "Docteur non trouvé"}, 404



    @staticmethod
    def authenticate_doctor(email, password):
        doctor = DoctorModel.get_doctor_by_email(email)
        
        if not doctor or not check_password_hash(doctor['password'], password):
            return None, "Email ou mot de passe incorrect"

        access_token = create_access_token(identity=doctor['id'])
        return access_token, None

    
    @staticmethod 
    def get_patient_symptoms(patient_id):
        # Appeler le modèle pour récupérer les symptômes du patient
        return DoctorModel.get_symptoms_by_patient(patient_id)

    @staticmethod
    def add_doctor_response(symptom_id, response):
        # Appeler le modèle pour ajouter une réponse du médecin aux symptômes du patient
        return DoctorModel.add_doctor_response(symptom_id, response)
    
    @staticmethod
    def update_doctor_response(id, response_update):
        # Appeler le modèle pour mettre à jour la réponse du médecin
        return DoctorModel.update_doctor_response(id, response_update)


    @staticmethod
    def delete_doctor_response(id):
        # Appeler le modèle pour supprimer la réponse du médecin
        return DoctorModel.delete_doctor_response(id)