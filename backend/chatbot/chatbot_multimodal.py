import openai
import os
from chatbot.chatbot_vision import analyze_medical_image
from dotenv import load_dotenv
from flask import Flask, request, jsonify  # Assurez-vous d'importer Flask et jsonify

# Initialiser l'application Flask
app = Flask(__name__)

# Charger la clé API OpenAI à partir du fichier .env
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Fonction pour générer une explication clinique détaillée avec des propositions de traitement adaptées
def generate_explanation_openai(image_class, report_text, confidence_score):
    prompt = (f"L'image montre des signes de {image_class} avec un seuil de confiance de {confidence_score:.0f}%. "
              f"Le patient présente les symptômes suivants : {report_text}. "
              "Veuillez fournir une explication clinique détaillée en fonction de cette condition, en précisant les impacts endocriniens et neurologiques potentiels. "
              "Fournissez également des options de traitement possibles en tenant compte des symptômes et de la condition prédite. "
              "Cette réponse est destinée à un médecin spécialisé.")

    # Utiliser chat.completions.create pour générer une réponse clinique complète et contextuelle
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful medical assistant providing detailed clinical information to doctors, including immediate treatment recommendations."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=3000,
        temperature=0.7
    )

    # Extraire le texte généré
    explanation = response.choices[0].message.content.strip()
    return explanation

# Fonction pour générer une recommandation spécifique
def generate_recommendation_openai(image_class, report_text):
    prompt = (f"En se basant sur le fait que l'image montre des signes de {image_class} et que le patient présente les symptômes suivants : {report_text}, "
              "quelle recommandation immédiate donneriez-vous au médecin pour la prise en charge de ce patient ? Soyez clair et concis.")

    # Utiliser chat.completions.create pour générer une recommandation immédiate
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a medical assistant providing immediate treatment recommendations to doctors."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7
    )

    # Extraire la recommandation générée
    recommendation = response.choices[0].message.content.strip()
    return recommendation

# Fonction d'analyse multimodale (texte et image)
def analyze_medical_report(report_text, image_path):
    # Analyse de l'image médicale (IRM, radiographie, etc.)
    image_analysis, confidence_score = analyze_medical_image(image_path)  # image_analysis retourne maintenant aussi le score de confiance

    # Générer une explication contextuelle en tenant compte de l'image et des symptômes
    explanation = generate_explanation_openai(image_analysis, report_text, confidence_score)

    # Générer la recommandation distincte
    recommendation = generate_recommendation_openai(image_analysis, report_text)

    # Structurer le rapport en HTML pour un meilleur rendu visuel
    combined_report = (
        f"<h2>Réponse du Chatbot :</h2>\n\n"
        f"<h3>Analyse de l'image :</h3>\n<p><strong>Classe prédite :</strong> {image_analysis}<br>\n"
        f"<strong>Seuil de confiance :</strong> {confidence_score:.0f}%</p>\n\n"
        f"<h3>Symptômes rapportés :</h3>\n<p>{report_text}</p>\n\n"
        f"<hr>\n\n"
        f"<h3>Explication clinique :</h3>\n<p>{explanation}</p>\n\n"
    )

    # Imprimer le résultat pour debug si besoin
    result = {
        "generated_report_html": combined_report,
        "recommendation_html": f"<p>{recommendation}</p>"
    }
    print(result)  # Vérifier la structure avant retour
    
    return result

# Route Flask pour gérer la requête POST du chatbot
@app.route('/chatbot/analyze', methods=['POST'])
def analyze():
    # Récupérer les données du formulaire multipart
    report_text = request.form['report_text']
    image = request.files['image']

    # Appeler la fonction d'analyse
    result = analyze_medical_report(report_text, image)

    # Retourner la réponse JSON correctement formatée
    return jsonify(result)

# Lancer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
