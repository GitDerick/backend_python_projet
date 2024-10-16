# predict_model.py : Utilisé pour faire des prédictions après l'entraînement.

import torch
from torchvision import transforms, models
import torch.nn as nn
from PIL import Image
import os

# Prétraitement des images (même que lors de l'entraînement)
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def load_model(model_path, num_classes):
    # Charger le modèle ResNet50
    model = models.resnet50(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    # Charger les poids sauvegardés
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Le fichier modèle '{model_path}' n'existe pas.")

    model.load_state_dict(torch.load(model_path))

    # Utiliser le GPU si disponible
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()

    return model, device

def predict_image(model, image_path, device):
    # Vérifier si l'image existe
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"L'image '{image_path}' n'a pas été trouvée.")

    # Charger et prétraiter l'image
    image = Image.open(image_path)
    image_tensor = transform(image).unsqueeze(0).to(device)

    # Passer l'image à travers le modèle pour obtenir la prédiction
    with torch.no_grad():
        outputs = model(image_tensor)
        _, predicted_class = torch.max(outputs, 1)

    return predicted_class.item()
