from models.notification_model import NotificationModel
from database import get_mongo_connection, get_mysql_connection
from bson.objectid import ObjectId

db = get_mongo_connection()

class AppointmentModel:

    @staticmethod
    def get_symptoms_by_patient(patient_id):
        # Récupérer tous les symptômes soumis par un patient
        return list(db.patient_symptoms.find({"patient_id": patient_id}))

    # @staticmethod
    # def add_doctor_response(symptom_id, response):
    #     # Mettre à jour les symptômes avec la réponse du médecin
    #     result = db.patient_symptoms.update_one(
    #         {"_id": ObjectId(symptom_id)},
    #         {"$set": {"doctor_response": response}}
    #     )
    #     return result.modified_count > 0

    @staticmethod
    def create_appointment(patient_id, doctor_id, doctor_name, submission_id, date, hospital_location, notes=""):
        # Créer une nouvelle consultation (rendez-vous) pour le patient
        appointment = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "doctor_name": doctor_name,
            "submission_id": ObjectId(submission_id),  # Lier ce rendez-vous à la soumission via son _id
            "date": date,
            "status": "confirmed",  # Rendez-vous confirmé par le médecin
            "hospital_location": hospital_location,
            "notes": notes
        }
        result = db.appointments.insert_one(appointment)

        # Envoyer une notification au patient
        message = f"Votre rendez-vous avec {doctor_name} est confirmé pour le {date} à {hospital_location}."
        NotificationModel.create_notification(patient_id, message, "appointment")

        return str(result.inserted_id)
    

    @staticmethod
    def update_appointment(appointment_id, update_data):
        # Convertir appointment_id en ObjectId
        appointment_id = ObjectId(appointment_id)

        # Mise à jour du rendez-vous dans MongoDB
        result = db.appointments.update_one(
            {"_id": appointment_id},  # Recherche par ID du rendez-vous
            {"$set": update_data}  # Mettre à jour les champs avec les nouvelles données
        )

        # Si la mise à jour réussit, créer une notification
        if result.modified_count > 0:
            appointment = db.appointments.find_one({"_id": appointment_id})
            patient_id = appointment['patient_id']
            doctor_name = appointment['doctor_name']

            # Envoyer une notification au patient
            message = f"Votre rendez-vous avec {doctor_name} a été mis à jour."
            NotificationModel.create_notification(patient_id, message, "updated_appointment")

        return result.modified_count > 0
    

    @staticmethod
    def delete_appointment(appointment_id):
        # Convertir appointment_id en ObjectId
        appointment_id = ObjectId(appointment_id)

        # Récupérer les détails du rendez-vous avant la suppression
        appointment = db.appointments.find_one({"_id": appointment_id})
        if appointment:
            patient_id = appointment['patient_id']
            doctor_name = appointment['doctor_name']

            # Suppression du rendez-vous dans MongoDB
            result = db.appointments.delete_one({"_id": appointment_id})

            # Si la suppression réussit, créer une notification
            if result.deleted_count > 0:
                message = f"Votre rendez-vous avec {doctor_name} a été annulé."
                NotificationModel.create_notification(patient_id, message, "deleted_appointment")

            return result.deleted_count > 0

        return False




    @staticmethod
    def get_appointments_by_patient(patient_id):
        patient_id = str(patient_id)
        # Récupérer les rendez-vous du patient
        appointments = db.appointments.find({"patient_id": patient_id})

        # Convertir les ObjectId en chaînes de caractères
        appointment_list = []
        for appointment in appointments:
            appointment["_id"] = str(appointment["_id"])  # Convertir l'ObjectId du rendez-vous en chaîne
            if "submission_id" in appointment:
                appointment["submission_id"] = str(appointment["submission_id"])  # Convertir l'ObjectId de la soumission en chaîne
            # Pas besoin de convertir doctor_id, car il est déjà un entier
            appointment_list.append(appointment)

        return appointment_list
    
    @staticmethod
    def get_appointments_by_doctor(doctor_id):
        # Récupérer les rendez-vous assignés par le docteur dans MongoDB
        appointments = db.appointments.find({"doctor_id": doctor_id})

        # Créer une liste pour stocker les rendez-vous et les informations des patients
        appointment_list = []

        # Connexion à MySQL pour récupérer les informations des patients
        connection = get_mysql_connection()
        cursor = connection.cursor(dictionary=True)

        for appointment in appointments:
            # Convertir ObjectId en chaînes de caractères
            appointment["_id"] = str(appointment["_id"])
            if "submission_id" in appointment:
                appointment["submission_id"] = str(appointment["submission_id"])  # Convertir ObjectId de la soumission en chaîne

            # Gestion du `patient_id` : d'abord essayer comme entier puis comme chaîne si la conversion échoue
            patient_id = appointment['patient_id']
            
            # Vérifier si `patient_id` est un entier ou une chaîne, et adapter les requêtes en fonction
            try:
                # Convertir en entier pour la requête MySQL
                patient_id_int = int(patient_id)
                print(f"Conversion réussie du patient_id en entier : {patient_id_int}")
            except ValueError:
                # Si la conversion échoue, utiliser la version en chaîne
                patient_id_int = patient_id
                print(f"Conversion en chaîne pour le patient_id : {patient_id_int}")

            # Requête pour récupérer les informations du patient depuis MySQL
            query = "SELECT first_name, last_name FROM patients WHERE id = %s"
            cursor.execute(query, (patient_id_int,))
            patient_info = cursor.fetchone()

            if patient_info:
                # Ajouter le nom du patient aux détails de l'appointment
                appointment["patient_name"] = f"{patient_info['first_name']} {patient_info['last_name']}"
            else:
                appointment["patient_name"] = "Nom inconnu"

            # Récupérer les symptômes et les antécédents médicaux du patient depuis MongoDB
            # Adapter la requête selon le type du `patient_id`
            try:
                # Convertir le patient_id pour MongoDB
                patient_id_mongo = int(patient_id) if isinstance(patient_id, str) else patient_id
                print(f"Utilisation de patient_id pour MongoDB : {patient_id_mongo}")
            except ValueError:
                # Si la conversion échoue, rester sur la chaîne
                patient_id_mongo = patient_id

            # Chercher les symptômes dans MongoDB
            symptoms = db.patient_symptoms.find_one({"patient_id": patient_id_mongo})
            if symptoms:
                appointment["symptoms"] = symptoms.get("symptoms", "Aucun symptôme")
                appointment["medical_history"] = symptoms.get("medical_history", "Pas d'antécédents")
            else:
                appointment["symptoms"] = "Aucun symptôme"
                appointment["medical_history"] = "Pas d'antécédents"

            # Ajouter l'appointment modifié à la liste
            appointment_list.append(appointment)

        cursor.close()
        connection.close()

        return appointment_list




    @staticmethod
    def get_patient_by_id(patient_id):
        # Connexion à la base de données MySQL pour récupérer les informations du patient
        connection = get_mysql_connection()  
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT first_name, last_name FROM patients WHERE id = %s"
            cursor.execute(query, (patient_id,))
            patient = cursor.fetchone()
            return patient
        except Exception as e:
            print(f"Erreur lors de la récupération du patient : {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    


    @staticmethod
    def get_appointments_by_patient_by_id(patient_id):
        # Convertir le patient_id en chaîne de caractères pour correspondre au format MongoDB
        patient_id_str = str(patient_id)
        
        # Récupérer tous les rendez-vous du patient à partir de la collection "appointments"
        appointments = db.appointments.find({"patient_id": patient_id_str})
        appointments_list = []
        
        for appointment in appointments:
            appointment_data = {
                "_id": str(appointment["_id"]),
                "patient_id": appointment["patient_id"],
                "doctor_id": appointment["doctor_id"],
                "doctor_name": appointment["doctor_name"],
                "submission_id": str(appointment["submission_id"]),
                "date": appointment["date"],
                "status": appointment["status"],
                "hospital_location": appointment.get("hospital_location", ""),
                "notes": appointment.get("notes", "")
            }
            appointments_list.append(appointment_data)
        
        return appointments_list