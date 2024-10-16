from io import BytesIO
from models.doctor_inscription_model import DoctorModel
from flask import request, jsonify, abort, send_file
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from datetime import datetime, date
from models.doctor_inscription_model import DoctorModel


class DoctorController:

    @staticmethod
    def register_doctor():
        # Récupérer les données envoyées dans la requête POST
        data = request.form.to_dict()  # Récupérer les données textuelles
        files = request.files  # Récupérer les fichiers téléversés

        # Champs requis pour l'inscription
        required_fields = ['full_name', 'date_of_birth', 'phone_number', 'email', 'password', 'speciality', 'license_number', 'work_institution', 'country', 'province', 'ville']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"message": f"Le champ {field} est obligatoire"}), 400

        # Appeler le modèle pour enregistrer le docteur
        response, status_code = DoctorModel.register_doctor(data)
        return jsonify(response), status_code

    @staticmethod
    def verify_email(token):
        # Vérifier le token de validation d'email
        email = DoctorModel.verify_email(token)
        if email:
            return jsonify({"message": "Email vérifié avec succès"}), 200
        else:
            return jsonify({"message": "Lien de vérification invalide ou expiré"}), 400

    @staticmethod
    def login_doctor():
        data = request.json  # Récupérer les données envoyées au format JSON
        
        # Vérifier que l'email et le mot de passe sont présents
        if 'email' not in data or 'password' not in data:
            return jsonify({"message": "Email et mot de passe sont obligatoires"}), 400

        # Appeler le modèle pour vérifier les informations de connexion du docteur
        doctor = DoctorModel.find_by_email(data['email'])
        
        if not doctor:
            return jsonify({"message": "Docteur non trouvé"}), 404
        
        # Vérifier si le mot de passe correspond
        if not DoctorModel.check_password(data['password'], doctor['password']):
            return jsonify({"message": "Mot de passe incorrect"}), 401

        # Vérifier si l'email du docteur est vérifié
        if not doctor['is_verified']:
            return jsonify({"message": "Veuillez vérifier votre email avant de vous connecter"}), 403
        
        # Générer un token d'accès JWT et un token de rafraîchissement
        access_token = create_access_token(identity=doctor['id'])
        refresh_token = create_refresh_token(identity=doctor['id'])

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,  # Ajout du token de rafraîchissement
            "id": doctor['id'],
            "message": "Connexion réussie"
        }), 200



    @staticmethod
    def update_doctor(doctor_id):
        data = request.json  # Récupérer les données envoyées dans la requête PUT

        # Appeler le modèle pour mettre à jour les informations du docteur
        updated = DoctorModel.update_doctor(doctor_id, data)

        if updated:
            return jsonify({"message": "Informations mises à jour avec succès"}), 200
        else:
            return jsonify({"message": "Erreur lors de la mise à jour"}), 400
        


    @staticmethod
    def get_doctor(doctor_id):
        doctor = DoctorModel.get_doctor_by_id(doctor_id)
        
        if doctor:
            print(f"Résultat SQL: {doctor}")  # Afficher les données récupérées pour déboguer

            # Vérification de la longueur de la réponse pour éviter KeyError
            if len(doctor) < 13:  # Assure-toi que la réponse contient toutes les colonnes attendues
                return {"message": "Données du docteur incomplètes"}, 500

            # Convertir la date de naissance en format 'YYYY-MM-DD'
            date_of_birth_str = doctor[2].strftime('%Y-%m-%d') if isinstance(doctor[2], (datetime, date)) else str(doctor[2])

            doctor_data = {
                "id": doctor[0],
                "full_name": doctor[1],
                "date_of_birth": date_of_birth_str,  # Format correct de la date
                "phone_number": doctor[3],
                "email": doctor[4],
                "address": doctor[5],
                "password": doctor[6],
                "speciality": doctor[7],
                "license_number": doctor[8],
                "work_institution": doctor[9],
                "country": doctor[10],
                "province": doctor[11],
                "ville": doctor[12]
            }
            return doctor_data, 200
        return {"message": "Docteur non trouvé"}, 404


    @staticmethod
    def get_all_patients_symptoms():
        try:
            symptoms = DoctorModel.get_all_symptoms()  # Appeler la méthode pour récupérer tous les symptômes
            return {"symptoms": symptoms}, 200
        except Exception as e:
            return {"message": f"Erreur lors de la récupération des symptômes : {str(e)}"}, 500
        

    @staticmethod
    def get_symptom_by_id(symptom_id):
        # Appeler le modèle pour récupérer les symptômes en fonction de l'ID unique
        return DoctorModel.get_symptoms_by_id(symptom_id)
    

