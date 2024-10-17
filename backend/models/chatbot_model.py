import torch
from torchvision import models
import torch.nn as nn
import urllib.request

# Fonction pour télécharger et charger le modèle pré-entraîné depuis S3
def load_model(model_url, num_classes):
    """
    Télécharge et charge le modèle ResNet50 pré-entraîné et ajuste la dernière couche en fonction du nombre de classes.
    :param model_url: URL du fichier du modèle (fichier .pth sur S3)
    :param num_classes: Nombre de classes de sortie du modèle
    :return: Modèle chargé et prêt à être utilisé pour les prédictions, et l'appareil (GPU/CPU)
    """
    # Télécharger le fichier du modèle à partir de l'URL
    model_path = "medical_model.pth"  # Nom temporaire local
    urllib.request.urlretrieve(model_url, model_path)
    
    # Charger le modèle ResNet50 sans pré-entraînement ImageNet
    model = models.resnet50(pretrained=False)
    
    # Remplacer la dernière couche pour correspondre au nombre de classes dans ton dataset (ici 4)
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    # Charger les poids entraînés depuis le fichier .pth téléchargé
    model.load_state_dict(torch.load(model_path))

    # Définir l'appareil (GPU si disponible, sinon CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)  # Envoyer le modèle au GPU/CPU

    return model, device

# Exemple d'appel avec le lien de votre modèle sur S3
model_url = "https://model-ia.s3.us-east-2.amazonaws.com/medical_model_combined_finetuned.pth"
model, device = load_model(model_url, num_classes=4)
