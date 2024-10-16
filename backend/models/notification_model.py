from datetime import datetime
from bson import ObjectId
from database import get_mongo_connection

db = get_mongo_connection()

class NotificationModel:

    @staticmethod
    def create_notification(patient_id, message, notification_type="diagnostic"):
        # Créer une notification pour le patient
        notification = {
            "patient_id": str(patient_id),  # Assurez-vous que patient_id est une chaîne
            "message": message,
            "notification_type": notification_type,  # Type de notification : diagnostic ou traitement
            "read": False,  # Indique si la notification a été lue
            "created_at": datetime.utcnow()  # Date de création
        }
        result = db.notifications.insert_one(notification)
        return str(result.inserted_id)

    @staticmethod
    def get_notifications_by_patient(patient_id):
        # Récupérer toutes les notifications non lues du patient
        notifications = db.notifications.find({"patient_id": str(patient_id), "read": False})
        notifications_list = []
        for notification in notifications:
            # Convertir ObjectId en chaîne de caractères
            notification["_id"] = str(notification["_id"])
            notifications_list.append(notification)
        return notifications_list

    @staticmethod
    def mark_notification_as_read(notification_id):
        # Marquer une notification comme lue
        result = db.notifications.update_one(
            {"_id": ObjectId(notification_id)},
            {"$set": {"read": True}}
        )
        return result.modified_count > 0
