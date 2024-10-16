import torch
from torchvision import models
import torch.nn as nn

# Fonction pour charger le modèle pré-entraîné
def load_model(model_path, num_classes):
    """
    Charge le modèle ResNet50 pré-entraîné et ajuste la dernière couche en fonction du nombre de classes.
    :param model_path: Chemin vers le fichier du modèle (fichier .pth)
    :param num_classes: Nombre de classes de sortie du modèle (ex: 4 pour glioma, meningioma, normal, pituitary tumor)
    :return: Modèle chargé et prêt à être utilisé pour les prédictions, et l'appareil (GPU/CPU)
    """
    # Charger le modèle ResNet50 sans pré-entraînement ImageNet
    model = models.resnet50(pretrained=False)
    
    # Remplacer la dernière couche pour correspondre au nombre de classes dans ton dataset (ici 4)
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    # Charger les poids entraînés depuis le fichier .pth
    model.load_state_dict(torch.load(model_path))

    # Définir l'appareil (GPU si disponible, sinon CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)  # Envoyer le modèle au GPU/CPU

    return model, device

# Spécifier le chemin absolu pour Railway
model_path = "/app/backend/models/medical_model_combined_finetuned.pth"  # Chemin absolu sur Railway

# Ou utilisez le chemin relatif en local si vous travaillez sur votre machine
# model_path = "models/medical_model_combined_finetuned.pth"

# Exemple d'utilisation de la fonction
model, device = load_model(model_path, num_classes=4)
