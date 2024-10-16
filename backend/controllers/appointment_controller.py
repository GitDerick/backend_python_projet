from models.appointment_model import AppointmentModel

class AppointmentController:

    @staticmethod
    def get_patient_symptoms(patient_id):
        # Appeler le modèle pour récupérer les symptômes du patient
        return AppointmentModel.get_symptoms_by_patient(patient_id)
    


    # @staticmethod
    # def add_doctor_response(symptom_id, response):
    #     # Appeler le modèle pour ajouter une réponse du médecin aux symptômes du patient
    #     return ConsultationModel.add_doctor_response(symptom_id, response)

    @staticmethod
    def create_appointment(patient_id, doctor_id, doctor_name, submission_id, date, hospital_location, notes=""):
        # Appeler le modèle pour créer une consultation (rendez-vous)
        return AppointmentModel.create_appointment(patient_id, doctor_id, doctor_name, submission_id, date, hospital_location, notes)
    
    @staticmethod
    def update_appointment(appointment_id, update_data):
        # Appeler le modèle pour mettre à jour un rendez-vous
        return AppointmentModel.update_appointment(appointment_id, update_data)
    
    @staticmethod
    def delete_appointment(appointment_id):
        # Appeler le modèle pour supprimer un rendez-vous
        return AppointmentModel.delete_appointment(appointment_id)

    @staticmethod
    def get_patient_appointments(patient_id):
        # Appeler le modèle pour récupérer les consultations du patient
        return AppointmentModel.get_appointments_by_patient(patient_id)
    
    @staticmethod
    def get_doctor_appointments(doctor_id):
        # Appeler le modèle pour récupérer les rendez-vous assignés par le docteur
        return AppointmentModel.get_appointments_by_doctor(doctor_id)


    @staticmethod
    def get_patient_appointments_by_id(patient_id):
        # Appeler le modèle pour récupérer les rendez-vous du patient
        return AppointmentModel.get_appointments_by_patient_by_id(patient_id)