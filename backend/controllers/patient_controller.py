import datetime
import bcrypt
from models.patient_model import PatientModel
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from database import get_mysql_connection, get_gridfs_connection
from bson.objectid import ObjectId
from datetime import datetime, date

class PatientController:
    @staticmethod
    def create_patient(data):
        # Logique métier pour valider les données (par exemple)
        if not all([data.get('first_name'), data.get('last_name'), data.get('date_of_birth'), data.get('password')]):
            return {"message": "Les informations du patient sont incomplètes"}, 400
        
        # Hachage du mot de passe avant de le passer au modèle
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        

        # Appel au modèle pour créer un patient
        patient_id = PatientModel.create_patient(
            data['first_name'],
            data['last_name'],
            data['date_of_birth'],
            data['phone_number'],
            data['email'],
            data['address'],
            hashed_password.decode('utf-8')
        )
        return {"message": "Patient créé avec succès", "patient_id": patient_id}, 201

    # @staticmethod
    # def get_patient(patient_id):
    #     # Appel au modèle pour récupérer un patient
    #     patient = PatientModel.get_patient(patient_id)
    #     if patient:
    #         patient_data = {
    #             "id": patient[0],
    #             "first_name": patient[1],
    #             "last_name": patient[2],
    #             "date_of_birth": str(patient[3]),
    #             "phone_number": patient[4],
    #             "email": patient[5],
    #             "address": patient[6],
    #             "password": patient[7]
    #         }
    #         return patient_data, 200
    #     else:
    #         return {"message": "Patient non trouvé"}, 404

    @staticmethod
    def get_patient(patient_id):
        # Appel au modèle pour récupérer un patient
        patient = PatientModel.get_patient(patient_id)
        if patient:
            # Convertir la date de naissance en format 'YYYY-MM-DD'
            date_of_birth_str = patient[3].strftime('%Y-%m-%d') if isinstance(patient[3], (datetime, date)) else str(patient[3])

            patient_data = {
                "id": patient[0],
                "first_name": patient[1],
                "last_name": patient[2],
                "date_of_birth": date_of_birth_str,  # Format correct de la date
                "phone_number": patient[4],
                "email": patient[5],
                "address": patient[6],
                "password": patient[7]
            }

            return patient_data, 200
        else:
            return {"message": "Patient non trouvé"}, 404
        

    @staticmethod
    def update_patient(patient_id, data):
        if not data:
            return {"message": "Aucune donnée fournie pour la mise à jour"}, 400

        updated = PatientModel.update_patient(patient_id, data)
        if updated:
            return {"message": "Patient mis à jour avec succès"}, 200
        else:
            return {"message": "Patient non trouvé"}, 404
        
    
    @staticmethod
    def delete_patient(patient_id):
        deleted = PatientModel.delete_patient(patient_id)
        if deleted:
            return {"message": "Patient supprimé avec succès"}, 200
        else:
            return {"message": "Patient non trouvé"}, 404
        

    @staticmethod
    def authenticate_patient(email, password):
        # Chercher le patient dans la base de données via l'email
        patient = PatientModel.get_patient_by_email(email)

        # Vérifier si le patient existe et si le mot de passe correspond
        if not patient or not bcrypt.checkpw(password.encode('utf-8'), patient['password'].encode('utf-8')):
            return None, "Email ou mot de passe incorrect"

        # Si les informations sont correctes, générer un token JWT
        access_token = create_access_token(identity=patient['id'])
        return access_token, None, patient['id']
    

    @staticmethod
    def get_medical_history(patient_id):
        # Appeler le modèle pour récupérer l'historique médical du patient
        return PatientModel.get_medical_history(patient_id)
    

    @staticmethod
    def get_patient_symptoms(patient_id):
        # Appeler le modèle pour récupérer les symptômes du patient
        return PatientModel.get_symptoms_by_patient(patient_id)
