import os
import torch
from torchvision import models
import torch.nn as nn

# Fonction pour charger le modèle pré-entraîné depuis le chemin relatif local
def load_model(model_path, num_classes):
    """
    Charge le modèle ResNet50 pré-entraîné et ajuste la dernière couche en fonction du nombre de classes.
    :param model_path: Chemin vers le fichier du modèle (fichier .pth)
    :param num_classes: Nombre de classes de sortie du modèle
    :return: Modèle chargé et prêt à être utilisé pour les prédictions, et l'appareil (GPU/CPU)
    """
    # Charger le modèle ResNet50 sans pré-entraînement ImageNet
    model = models.resnet50(pretrained=False)
    
    # Remplacer la dernière couche pour correspondre au nombre de classes dans votre dataset (ici 4)
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    # Charger les poids entraînés depuis le fichier .pth
    model.load_state_dict(torch.load(model_path))

    # Définir l'appareil (GPU si disponible, sinon CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)  # Envoyer le modèle au GPU/CPU

    return model, device

# Vérification du chemin de travail actuel et des fichiers
print("Répertoire de travail actuel :", os.getcwd())
print("Liste des fichiers dans le répertoire actuel :", os.listdir(os.getcwd()))

# Vérifier le répertoire des modèles
model_dir = os.path.join(os.getcwd(), 'backend', 'models')
if os.path.exists(model_dir):
    print("Liste des fichiers dans le répertoire des modèles :", os.listdir(model_dir))
else:
    print("Le répertoire des modèles n'existe pas :", model_dir)

# Utilisation du chemin relatif local à l'intérieur du projet déployé
model_path = '../backend/models/medical_model_combined_finetuned.pth'
model, device = load_model(model_path, num_classes=4)
