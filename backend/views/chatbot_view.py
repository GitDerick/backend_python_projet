from flask import Blueprint, request, jsonify
from chatbot.chatbot_multimodal import analyze_medical_report
import os

# Déclaration du blueprint pour le chatbot
chatbot_view = Blueprint('chatbot_view', __name__)

@chatbot_view.route('/chatbot/analyze', methods=['POST'])
def analyze_medical_data():
    # Récupérer le texte du formulaire
    report_text = request.form.get("report_text")
    
    # Récupérer l'image depuis les fichiers envoyés
    image = request.files.get("image")

    # Vérifier si le texte et l'image sont présents
    if not report_text or not image:
        return jsonify({"error": "Le texte du rapport ou l'image est manquant"}), 400

    # Créer le dossier 'uploads' s'il n'existe pas
    if not os.path.exists("./uploads"):
        os.makedirs("./uploads")

    # Sauvegarder temporairement l'image pour analyse
    image_path = f"./uploads/{image.filename}"
    image.save(image_path)

    # Appel à la fonction d'analyse multimodale (texte + image)
    result = analyze_medical_report(report_text, image_path)
    
    return jsonify(result)
