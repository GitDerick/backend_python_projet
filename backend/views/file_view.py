from flask import Blueprint
from controllers.file_controller import FileController

file_view = Blueprint('file_view', __name__)

# Route pour télécharger un fichier par son ID
@file_view.route('/files/<file_id>', methods=['GET'])
def get_file(file_id):
    return FileController.serve_file(file_id)
