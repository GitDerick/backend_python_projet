from bson import ObjectId
from models.notification_model import NotificationModel
from database import get_mongo_connection, get_mysql_connection

db = get_mongo_connection()

class ConsultationModel:

    @staticmethod
    def create_remote_consultation(patient_id, doctor_id, doctor_name, date, time, notes=""):
        # Générer un lien unique pour la vidéoconférence
        video_link = f"https://meet.jit.si/consultation-{str(ObjectId())}"

        # Créer une nouvelle consultation à distance pour le patient
        remote_consultation = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "doctor_name": doctor_name,
            "date": date,
            "time": time,
            "video_link": video_link,  # Lien de vidéoconférence
            "status": "pending",  # Par défaut, la consultation est en attente
            "notes": notes
        }

        # Insérer la consultation à distance dans MongoDB
        result = db.remote_consultations.insert_one(remote_consultation)

        # Envoyer une notification au patient
        message = f"Une consultation à distance a été programmée avec {doctor_name} le {date} à {time}."
        NotificationModel.create_notification(patient_id, message, "remote_consultation")

        return str(result.inserted_id), video_link  # Retourner l'ID et le lien vidéo

    

    @staticmethod
    def get_remote_consultations_by_patient(patient_id):
        # Convertir patient_id en chaîne si nécessaire
        if isinstance(patient_id, int):
            patient_id = str(patient_id)  # S'assurer que le patient_id est une chaîne

        # Rechercher les consultations avec le patient_id
        consultations = db.remote_consultations.find({"patient_id": patient_id})
        
        # Convertir ObjectId et retourner la liste
        consultations_list = []
        for consultation in consultations:
            consultation["_id"] = str(consultation["_id"])  # Convertir ObjectId en chaîne
            consultations_list.append(consultation)
        
        return consultations_list
    


    @staticmethod
    def get_consultations_by_doctor(doctor_id):
        # Récupérer les consultations de MongoDB
        consultations = db.remote_consultations.find({"doctor_id": doctor_id})

        # Connexion à la base de données MySQL pour récupérer les noms des patients
        connection = get_mysql_connection()
        cursor = connection.cursor(dictionary=True)

        consultations_with_patient_names = []
        
        for consultation in consultations:
            patient_id = consultation["patient_id"]
            
            # Requête SQL pour récupérer les informations du patient à partir de l'ID
            cursor.execute("SELECT first_name, last_name FROM patients WHERE id = %s", (patient_id,))
            patient_info = cursor.fetchone()
            
            if patient_info:
                # Concaténer le nom complet
                patient_name = f"{patient_info['first_name']} {patient_info['last_name']}"
            else:
                patient_name = "Nom du patient inconnu"
            
            # Ajouter les données au résultat final
            consultations_with_patient_names.append({
                "id": str(consultation["_id"]),
                "patient_name": patient_name,  # Utiliser le nom complet récupéré
                "date": consultation.get("date", "Date non spécifiée"),
                "time": consultation.get("time", "Heure non spécifiée"),
                "status": consultation.get("status", "Statut non spécifié"),
                "video_link": consultation.get("video_link", "#"),
                "notes": consultation.get("notes", "Aucune note")
            })

        cursor.close()
        connection.close()

        return consultations_with_patient_names

    

    @staticmethod
    def update_remote_consultation(consultation_id, data):
        # Convertir consultation_id en ObjectId
        consultation_id = ObjectId(consultation_id)

        # Mise à jour de la consultation dans MongoDB
        result = db.remote_consultations.update_one(
            {"_id": consultation_id},  # Recherche par ID de la consultation
            {"$set": data}  # Mettre à jour les champs avec les nouvelles données
        )

        # Si la mise à jour réussit, créer une notification
        if result.modified_count > 0:
            consultation = db.remote_consultations.find_one({"_id": consultation_id})
            patient_id = consultation['patient_id']
            doctor_name = consultation['doctor_name']

            # Envoyer une notification au patient
            message = f"Votre consultation à distance avec {doctor_name} a été mise à jour."
            NotificationModel.create_notification(patient_id, message, "updated_consultation")

        return result.modified_count > 0

    

    @staticmethod
    def delete_remote_consultation(consultation_id):
        # Convertir consultation_id en ObjectId
        consultation_id = ObjectId(consultation_id)

        # Récupérer les détails de la consultation avant la suppression
        consultation = db.remote_consultations.find_one({"_id": consultation_id})
        if consultation:
            patient_id = consultation['patient_id']
            doctor_name = consultation['doctor_name']

            # Suppression de la consultation dans MongoDB
            result = db.remote_consultations.delete_one({"_id": consultation_id})

            # Si la suppression réussit, créer une notification
            if result.deleted_count > 0:
                message = f"Votre consultation à distance avec {doctor_name} a été annulée."
                NotificationModel.create_notification(patient_id, message, "deleted_consultation")
            
            return result.deleted_count > 0

        return False


