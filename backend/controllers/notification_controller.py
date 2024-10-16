from models.notification_model import NotificationModel

class NotificationController:

    @staticmethod
    def create_notification(patient_id, message, notification_type="diagnostic"):
        return NotificationModel.create_notification(patient_id, message, notification_type)

    @staticmethod
    def get_notifications_by_patient(patient_id):
        return NotificationModel.get_notifications_by_patient(patient_id)

    @staticmethod
    def mark_notification_as_read(notification_id):
        return NotificationModel.mark_notification_as_read(notification_id)
