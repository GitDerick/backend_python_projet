from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Chargement du modèle BioBERT pré-entraîné
nlp_model = BertForSequenceClassification.from_pretrained('dmis-lab/biobert-base-cased-v1.1')
tokenizer = BertTokenizer.from_pretrained('dmis-lab/biobert-base-cased-v1.1')

def analyze_medical_text(text):
    # Tokenization et encodage du texte
    inputs = tokenizer.encode(text, return_tensors="pt")
    outputs = nlp_model(inputs)
    # Interpréter les résultats
    predictions = torch.softmax(outputs.logits, dim=-1)
    predicted_class = torch.argmax(predictions).item()
    
    return f"Classe prédite pour le texte : {predicted_class}"
