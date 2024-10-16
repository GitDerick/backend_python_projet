from datetime import timedelta
import os
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
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)  # Token de rafraîchissement expire en 30 jours

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


if __name__ == '__main__':
    # Utiliser le port fourni par Railway, ou par défaut le port 5000 en local
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
