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

# Déterminer le chemin du fichier modèle en fonction de l'environnement
current_dir = os.getcwd()

# Chemin potentiel en local ou en production
possible_paths = [
    os.path.join(current_dir, 'models', 'medical_model_combined_finetuned.pth'),  # Cas local
    os.path.join(current_dir, 'backend', 'models', 'medical_model_combined_finetuned.pth')  # Cas Railway ou prod
]

# Sélectionner le chemin valide
model_path = None
for path in possible_paths:
    if os.path.exists(path):
        model_path = path
        break

# Si aucun chemin n'est trouvé, lever une exception
if model_path is None:
    raise FileNotFoundError(f"Le fichier du modèle n'a pas été trouvé dans les chemins suivants : {possible_paths}")

# Charger le modèle avec le chemin correct
model, device = load_model(model_path, num_classes=4)
