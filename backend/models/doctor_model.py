from models.notification_model import NotificationModel
from database import get_mysql_connection
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_mongo_connection
from bson.objectid import ObjectId

db = get_mongo_connection()

class DoctorModel:
    @staticmethod
    def create_doctor(first_name, last_name, email, password, specialization):
        conn = get_mysql_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO doctors (first_name, last_name, email, password, specialization)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (first_name, last_name, email, password, specialization))
        doctor_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return doctor_id

    @staticmethod
    def get_doctor_by_id(doctor_id):
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM doctor WHERE id = %s"
        cursor.execute(query, (doctor_id,))
        doctor = cursor.fetchone()

        cursor.close()
        conn.close()
        return doctor

    @staticmethod
    def update_doctor(doctor_id, data):
        conn = get_mysql_connection()
        cursor = conn.cursor()

        fields = []
        values = []
        for key in data:
            if key == "password":
                hashed_password = generate_password_hash(data[key])
                fields.append(f"{key} = %s")
                fields.append(hashed_password)
            else:
                fields.append(f"{key} = %s")
                values.append(data[key])

        values.append(doctor_id)
        fields_str = ", ".join(fields)

        query = f"UPDATE doctors SET {fields_str} WHERE id = %s"
        cursor.execute(query, values)
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return updated

    @staticmethod
    def delete_doctor(doctor_id):
        conn = get_mysql_connection()
        cursor = conn.cursor()

        query = "DELETE FROM doctors WHERE id = %s"
        cursor.execute(query, (doctor_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return deleted
    
    @staticmethod
    def get_doctor_by_email(email):
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM doctors WHERE email = %s"
        cursor.execute(query, (email,))
        doctor = cursor.fetchone()

        cursor.close()
        conn.close()
        return doctor
    
    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)
    

    # Récupérer tous les symptômes soumis par un patient depuis la base de données
    @staticmethod
    def get_symptoms_by_patient(patient_id):
        try:
            patient_id = int(patient_id)
        except ValueError:
            return []

        symptoms = db.patient_symptoms.find({"patient_id": patient_id})
        symptoms_list = []

        for symptom in symptoms:
            symptom_data = {
                "_id": str(symptom['_id']),  # Convertir ObjectId en chaîne
                "symptoms": symptom['symptoms'],
                "duration": symptom['duration'],
                "medical_history": symptom.get('medical_history', ''),
                "additional_info": symptom.get('additional_info', ''),
                "submitted_at": symptom['submitted_at'],
                "doctor_response": symptom.get('doctor_response', {}),
                "files": [
                    {
                        "file_id": str(file["file_id"]),  # Convertir ObjectId en chaîne
                        "filename": file["filename"],
                        "metadata": file["metadata"],
                        "uploadDate": file["uploadDate"]
                    } for file in symptom.get("files", [])
                ]
            }

            # Convertir symptom_id en ObjectId pour la requête dans GridFS
            symptom_id = ObjectId(symptom['_id'])

            files = db.fs.files.find({"metadata.symptom_id": symptom_id})

            for file in files:
                file_data = {
                    "filename": file['filename'],
                    "file_id": str(file['_id']),  # Convertir ObjectId en chaîne de caractères
                    "metadata": {
                        "patient_id": file['metadata']['patient_id'],
                        "symptom_id": str(file['metadata']['symptom_id'])  # Convertir ObjectId en chaîne de caractères
                    },
                    "uploadDate": file['uploadDate']
                }
                symptom_data['files'].append(file_data)

            symptoms_list.append(symptom_data)

        return symptoms_list

    @staticmethod
    def add_doctor_response(symptom_id, response):
        # Mettre à jour les symptômes avec la réponse du médecin
        result = db.patient_symptoms.update_one(
            {"_id": ObjectId(symptom_id)},
            {"$set": {"doctor_response": response}}
        )
        
        if result.modified_count > 0:
            # Si la mise à jour a réussi, créer une notification
            symptom = db.patient_symptoms.find_one({"_id": ObjectId(symptom_id)})
            if symptom:
                patient_id = symptom['patient_id']
                doctor_name = response.get('doctor_name', 'Votre médecin')

                # Créer la notification pour le patient
                message = f"{doctor_name} a ajouté de nouvelles instructions à vos symptômes."
                NotificationModel.create_notification(patient_id, message, "diagnostic")

            return True
        
        return False
    

    @staticmethod
    def update_doctor_response(id, response_update):
        # Mettre à jour la réponse du médecin en utilisant l'_id fourni par MongoDB
        result = db.patient_symptoms.update_one(
            {"_id": ObjectId(id)},  # Utiliser l'ObjectId de MongoDB pour identifier le document
            {"$set": {"doctor_response": response_update}}  # Mettre à jour le champ doctor_response
        )
        
        if result.modified_count > 0:
            # Si la mise à jour a réussi, créer une notification
            symptom = db.patient_symptoms.find_one({"_id": ObjectId(id)})
            if symptom:
                patient_id = symptom['patient_id']
                doctor_name = response_update.get('doctor_name', 'Votre médecin')

                # Créer la notification pour informer le patient que la réponse a été mise à jour
                message = f"{doctor_name} a mis à jour ses instructions concernant vos symptômes."
                NotificationModel.create_notification(patient_id, message, "updated_response")
            
            return True
        
        return False
    
    @staticmethod
    def delete_doctor_response(id):
        # Supprimer la réponse du médecin en supprimant le champ doctor_response
        result = db.patient_symptoms.update_one(
            {"_id": ObjectId(id)},  # Utiliser l'ObjectId pour identifier le document
            {"$unset": {"doctor_response": ""}}  # Utiliser $unset pour supprimer le champ doctor_response
        )
        
        if result.modified_count > 0:
            # Si la suppression a réussi, créer une notification
            symptom = db.patient_symptoms.find_one({"_id": ObjectId(id)})
            if symptom:
                patient_id = symptom['patient_id']

                # Créer la notification pour informer le patient que la réponse a été supprimée
                message = "Votre médecin a supprimé sa réponse concernant vos symptômes."
                NotificationModel.create_notification(patient_id, message, "deleted_response")
            
            return True
        
        return False
