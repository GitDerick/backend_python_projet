from werkzeug.utils import secure_filename
from models.symptom_model import SymptomModel
from database import get_mongo_connection, get_gridfs_connection
from bson.objectid import ObjectId  # Importer ObjectId pour la conversion
import gridfs

db = get_mongo_connection()
#fs = get_gridfs_connection()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'docx'}

class SymptomController:

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def submit_symptoms(data, files, patient_id):
        # Valider la présence des champs obligatoires
        if not data.get('symptoms') or not data.get('duration'):
            return {"message": "Les champs symptômes et durée sont obligatoires"}, 400

        try:
            # Insérer les symptômes dans MongoDB
            symptom_id = SymptomModel.insert_symptom(
                patient_id=patient_id,
                symptoms=data['symptoms'],
                duration=data['duration'],
                medical_history=data.get('medical_history', ''),
                additional_info=data.get('additional_info', '')
            )
        except Exception as e:
            return {"message": f"Erreur lors de l'insertion des symptômes : {str(e)}"}, 500

        # Enregistrer les fichiers s'ils sont présents
        if files:
            for file in files:
                if file and SymptomController.allowed_file(file.filename):
                    try:
                        filename = secure_filename(file.filename)
                        SymptomModel.save_file(file, patient_id, symptom_id, filename)
                    except Exception as e:
                        return {"message": f"Erreur lors de l'enregistrement du fichier : {str(e)}"}, 500

        return {"message": "Symptômes et fichiers soumis avec succès"}, 201
    

    @staticmethod
    def get_all_symptoms_and_files():
        symptoms_list = []
        fs = get_gridfs_connection()

        # Récupérer tous les symptômes
        symptoms = db.patient_symptoms.find()
        
        for symptom in symptoms:
            symptom_data = {
                "_id": str(symptom['_id']),
                "patient_id": symptom['patient_id'],
                "symptoms": symptom['symptoms'],
                "duration": symptom['duration'],
                "medical_history": symptom.get('medical_history', ''),
                "additional_info": symptom.get('additional_info', ''),
                "submitted_at": symptom['submitted_at'],
                "files": []
            }

            # Convertir symptom_id en ObjectId pour la requête dans GridFS
            symptom_id = ObjectId(symptom['_id'])

            # Vérifier s'il y a des fichiers associés à ce symptôme dans fs.files
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

        return symptoms_list  # Retourne les données sous forme de liste
    

    @staticmethod
    def delete_symptom(symptom_id):
        # Appeler le modèle pour supprimer le formulaire avec l'ID donné
        return SymptomModel.delete_symptom_by_id(symptom_id)
