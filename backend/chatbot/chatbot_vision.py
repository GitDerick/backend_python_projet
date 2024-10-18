import torch
from torchvision import transforms
from PIL import Image
from models.chatbot_model import load_model

# Prétraitement des images
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Charger le modèle pré-entraîné
model_path = 'models/medical_model_combined_finetuned.pth'
model, device = load_model(model_path, num_classes=4)  # Charger le modèle avec 4 classes
model.eval()  # Mode évaluation

# Définir un seuil de confiance (ex: 0.6)
CONFIDENCE_THRESHOLD = 0.6

def analyze_medical_image(image_path):
    image = Image.open(image_path)
    
    # Si l'image est en niveaux de gris, la convertir en RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')

    image = transform(image).unsqueeze(0).to(device)  # Appliquer le prétraitement et envoyer au GPU/CPU

    with torch.no_grad():
        outputs = model(image)  # Obtenir les prédictions
        probabilities = torch.nn.functional.softmax(outputs, dim=1)  # Calculer les probabilités
        confidence, predicted_class = torch.max(probabilities, 1)  # Extraire la confiance et la classe prédite

    # Afficher les probabilités pour chaque classe
    print(f"Probabilités : {probabilities.cpu().numpy()}")

    # Si la confiance dépasse le seuil (réduit à 0.5), retourner la classe prédite
    if confidence.item() > CONFIDENCE_THRESHOLD:
        classes = ['glioma_tumor', 'meningioma_tumor', 'normal', 'pituitary_tumor']
        predicted_label = classes[predicted_class.item()]  # Classe prédite
        confidence_percentage = confidence.item() * 100 # Renvoyer le score de confiance en pourcent
        
        #return f"Classe prédite : {predicted_label} avec une confiance de {confidence.item():.2f}"
        return predicted_label, confidence_percentage
    else:
        # Si la confiance est faible, retourner une incertitude
        return "Image inconnue ou incertaine."


# import os
# import torch
# from torchvision import transforms
# from PIL import Image
# from models.chatbot_model import load_model

# # Prétraitement des images
# transform = transforms.Compose([
#     transforms.Resize(256),
#     transforms.CenterCrop(224),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
# ])

# # Déterminer le chemin du fichier modèle (ici simple_model.pth dans le répertoire 'backend/models')
# current_dir = os.getcwd()  # Répertoire de travail actuel
# model_path = os.path.join(current_dir, 'backend', 'models', 'simple_model.pth')  # Correction du chemin

# # Charger le modèle simple
# model, device = load_model(model_path)  # Charger le modèle simple sans num_classes
# model.eval()  # Mode évaluation

# # Définir un seuil de confiance (ex: 0.6)
# CONFIDENCE_THRESHOLD = 0.6

# def analyze_medical_image(image_path):
#     image = Image.open(image_path)
    
#     # Si l'image est en niveaux de gris, la convertir en RGB
#     if image.mode != 'RGB':
#         image = image.convert('RGB')

#     image = transform(image).unsqueeze(0).to(device)  # Appliquer le prétraitement et envoyer au GPU/CPU

#     with torch.no_grad():
#         outputs = model(image)  # Obtenir les prédictions
#         probabilities = torch.nn.functional.softmax(outputs, dim=1)  # Calculer les probabilités
#         confidence, predicted_class = torch.max(probabilities, 1)  # Extraire la confiance et la classe prédite

#     # Afficher les probabilités pour chaque classe
#     print(f"Probabilités : {probabilities.cpu().numpy()}")

#     # Si la confiance dépasse le seuil (réduit à 0.5), retourner la classe prédite
#     if confidence.item() > CONFIDENCE_THRESHOLD:
#         classes = ['classe_0', 'classe_1']  # Classes prédéfinies pour le modèle simple
#         predicted_label = classes[predicted_class.item()]  # Classe prédite
#         confidence_percentage = confidence.item() * 100  # Renvoyer le score de confiance en pourcent

#         return predicted_label, confidence_percentage
#     else:
#         # Si la confiance est faible, retourner une incertitude
#         return "Image inconnue ou incertaine."
