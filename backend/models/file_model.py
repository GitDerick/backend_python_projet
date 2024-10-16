from database import get_mongo_connection
from bson import ObjectId

db = get_mongo_connection()

class FileModel:
    @staticmethod
    def get_file_by_id(file_id):
        try:
            # Chercher le fichier dans GridFS
            file = db.fs.files.find_one({"_id": ObjectId(file_id)})
            if not file:
                return None

            # Récupérer les données binaires du fichier
            grid_out = db.fs.get(ObjectId(file_id))
            file_data = grid_out.read()

            return {
                "file_data": file_data,
                "content_type": file.get("contentType", "application/octet-stream"),
                "filename": file.get("filename", "unknown")
            }
        except Exception as e:
            print(f"Erreur lors de la récupération du fichier: {str(e)}")
            return None
