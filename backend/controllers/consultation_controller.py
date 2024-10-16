from models.consultation_model import ConsultationModel

class ConsultationController:

    @staticmethod
    def create_remote_consultation(patient_id, doctor_id, doctor_name, date, time, notes=""):
        # Appeler le modèle pour créer une consultation à distance
        return ConsultationModel.create_remote_consultation(patient_id, doctor_id, doctor_name, date, time, notes)
    

    @staticmethod
    def get_remote_consultations_by_patient(patient_id):
        return ConsultationModel.get_remote_consultations_by_patient(patient_id)
    
    @staticmethod
    def get_consultations_by_doctor(doctor_id):
        # Appeler le modèle pour récupérer les consultations du docteur
        return ConsultationModel.get_consultations_by_doctor(doctor_id)
    
    @staticmethod
    def update_remote_consultation(consultation_id, data):
        # Appeler le modèle pour mettre à jour la consultation à distance
        return ConsultationModel.update_remote_consultation(consultation_id, data)
    
    @staticmethod
    def delete_remote_consultation(consultation_id):
        # Appeler le modèle pour supprimer la consultation à distance
        return ConsultationModel.delete_remote_consultation(consultation_id)


