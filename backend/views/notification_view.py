from bson import ObjectId
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.notification_controller import NotificationController

notification_view = Blueprint('notification_view', __name__)

# Route pour récupérer les notifications du patient
@notification_view.route('/patient/notifications', methods=['GET'])
@jwt_required()  # Le patient doit être authentifié
def get_notifications():
    patient_id = get_jwt_identity()  # Récupérer l'ID du patient connecté
    notifications = NotificationController.get_notifications_by_patient(patient_id)
    return jsonify(notifications), 200

@notification_view.route('/patient/notifications/<notification_id>', methods=['PUT'])
@jwt_required()  # Le patient doit être authentifié
def mark_notification_as_read(notification_id):
    try:
        # Convertir le notification_id en ObjectId si ce n'est pas déjà le cas
        object_id = ObjectId(notification_id)
        success = NotificationController.mark_notification_as_read(object_id)
        if success:
            return jsonify({"message": "Notification marquée comme lue"}), 200
        else:
            return jsonify({"message": "Échec de l'opération"}), 400
    except Exception as e:
        return jsonify({"message": f"Erreur: {str(e)}"}), 500