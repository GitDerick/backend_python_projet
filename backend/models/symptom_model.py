from database import get_mongo_connection, get_gridfs_connection
from bson.objectid import ObjectId

db = get_mongo_connection()
fs = get_gridfs_connection()

class SymptomModel:

    @staticmethod
    def insert_symptom(patient_id, symptoms, duration, medical_history='', additional_info=''):
        # Crée un document pour les symptômes et l'insère dans MongoDB
        symptom_entry = {
            "patient_id": patient_id,
            "symptoms": symptoms,
            "duration": duration,
            "medical_history": medical_history,
            "additional_info": additional_info,
            "submitted_at": db.command("serverStatus")['localTime']
        }
        return db.patient_symptoms.insert_one(symptom_entry).inserted_id

    @staticmethod
    def save_file(file, patient_id, symptom_id, filename):
        # Sauvegarde le fichier dans GridFS et enregistre les métadonnées
        try:
            file_id = fs.put(file, filename=filename, metadata={"patient_id": patient_id, "symptom_id": symptom_id})
            db.patient_files.insert_one({
                "patient_id": patient_id,
                "symptom_id": symptom_id,
                "file_id": file_id,
                "filename": filename,
                "uploaded_at": db.command("serverStatus")['localTime']
            })
            return file_id
        except Exception as e:
            raise Exception(f"Erreur lors de l'enregistrement du fichier : {str(e)}")
        

    @staticmethod
    def delete_symptom_by_id(symptom_id):
        # Suppression d'un document en fonction de son ObjectId
        result = db.patient_symptoms.delete_one({"_id": ObjectId(symptom_id)})
        return result.deleted_count > 0  # Renvoie True si un document a été supprimé
