from chatbot.chatbot_nlp import analyze_medical_text
from chatbot.chatbot_vision import analyze_medical_image

def analyze_medical_report(text, image_path):
    # Analyse du texte médical
    text_analysis = analyze_medical_text(text)

    # Analyse de l'image médicale (si une image est fournie)
    if image_path:
        image_analysis = analyze_medical_image(image_path)
    else:
        image_analysis = "Aucune image fournie."

    # Combiner les résultats
    combined_report = f"Analyse du texte : {text_analysis}\nAnalyse de l'image : {image_analysis}"
    return combined_report
