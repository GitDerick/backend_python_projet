from datetime import timedelta
import logging
import os
import urllib.request
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from views.notification_view import notification_view
from views.patient_view import patient_view, auth_view
from views.doctor_view import doctor_view, authDoc_view
from views.symptom_view import symptom_view
from views.appointment_view import appointment_view
from views.consultation_view import consultation_view
from views.file_view import file_view
from views.doctor_inscription_view import doctor_inscription_view
from views.chatbot_view import chatbot_view

app = Flask(__name__)

# Configuration Flask pour accepter toutes les requêtes CORS
CORS(app)

# Clé secrète pour signer les tokens JWT
app.config['JWT_SECRET_KEY'] = 'Ma_superbe_cle_super_secrete'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)  # 30 minutes
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)  # Token de rafraîchissement expire en 7 jours

# Initialisation de Flask-JWT-Extended
jwt = JWTManager(app)


# Vue des patients
app.register_blueprint(patient_view)

# Vue d'authentification patient
app.register_blueprint(auth_view)

# Vue des docteurs
app.register_blueprint(doctor_view)

# Vue d'authentification doctor
app.register_blueprint(authDoc_view)

# Vue des symptomes
app.register_blueprint(symptom_view)

# Vue des rendez-vous
app.register_blueprint(appointment_view)

# Vue des consultations
app.register_blueprint(consultation_view)

# Vue des docteurs (inscription)
app.register_blueprint(doctor_inscription_view)

# Enregistrer la vue du fichier
app.register_blueprint(file_view)

# Enregistrer la vue du chatbot
app.register_blueprint(chatbot_view)

# Vue des notifications
app.register_blueprint(notification_view)

# # Fonction pour télécharger le modèle s'il n'est pas présent localement
# def download_model_if_needed():
#     model_path = "models/medical_model_combined_finetuned.pth"
#     model_url = "https://model-ia.s3.us-east-2.amazonaws.com/medical_model_combined_finetuned.pth"

#     # Vérifier si le fichier du modèle existe, sinon le télécharger
#     if not os.path.exists(model_path):
#         print("Téléchargement du modèle depuis S3...")
#         try:
#             urllib.request.urlretrieve(model_url, model_path)
#             print("Modèle téléchargé avec succès.")
#         except Exception as e:
#             print(f"Erreur lors du téléchargement du modèle : {e}")
#             raise  # Relancer l'erreur si le téléchargement échoue


# Ajouter des logs pour suivre les actions
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.before_request
def startup():
    logger.info("L'application est en train de démarrer...")

# Route de test basique
@app.route('/')
def home():
    return "L'application fonctionne correctement sur Railway!"

# Route de vérification supplémentaire
@app.route('/check', methods=['GET'])
def check():
    return "L'application est vivante et fonctionnelle !", 200

if __name__ == '__main__':
    # Télécharger le modèle avant de démarrer l'application
    # download_model_if_needed()
    
    # Utiliser le port fourni par Railway, ou par défaut le port 5000 en local
    port = int(os.environ.get('PORT', 5000))

    # Ajout de logs pour afficher le port utilisé
    logger.info(f"L'application va démarrer sur le port : {port}")

    # Activer le mode debug seulement si l'application est exécutée en local
    debug_mode = os.environ.get('RAILWAY_ENVIRONMENT') != 'production'

    logger.info(f"Mode debug activé : {debug_mode}")

    
    app.run(host='0.0.0.0', port=port, debug=True)
