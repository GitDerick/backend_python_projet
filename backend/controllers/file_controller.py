from flask import send_file, jsonify
from bson.objectid import ObjectId
from database import get_mongo_connection
import gridfs
from io import BytesIO

db = get_mongo_connection()
fs = gridfs.GridFS(db)

class FileController:

    @staticmethod
    def serve_file(file_id):
        try:
            # Vérifier si le fichier existe dans GridFS
            file_id = ObjectId(file_id)  # Convertir l'ID en ObjectId
            file = fs.get(file_id)  # Utiliser GridFS pour obtenir le fichier

            # Créer un flux binaire pour lire le fichier
            file_data = BytesIO(file.read())
            file_data.seek(0)

            # Envoyer le fichier en tant que réponse HTTP
            return send_file(
                file_data,
                mimetype=file.content_type,  # Type MIME du fichier
                as_attachment=True,
                download_name=file.filename  # Le nom du fichier à télécharger
            )
        except gridfs.NoFile:
            return jsonify({"error": "Fichier introuvable"}), 404
        except Exception as e:
            return jsonify({"error": f"Erreur lors de la récupération du fichier: {str(e)}"}), 500
