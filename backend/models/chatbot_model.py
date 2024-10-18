# import os
# import torch
# from torchvision import models
# import torch.nn as nn

# # Fonction pour charger le modèle pré-entraîné depuis le chemin relatif local
# def load_model(model_path, num_classes):
#     """
#     Charge le modèle ResNet50 pré-entraîné et ajuste la dernière couche en fonction du nombre de classes.
#     :param model_path: Chemin vers le fichier du modèle (fichier .pth)
#     :param num_classes: Nombre de classes de sortie du modèle
#     :return: Modèle chargé et prêt à être utilisé pour les prédictions, et l'appareil (GPU/CPU)
#     """
#     # Charger le modèle ResNet50 sans pré-entraînement ImageNet
#     model = models.resnet50(pretrained=False)
    
#     # Remplacer la dernière couche pour correspondre au nombre de classes dans votre dataset (ici 4)
#     model.fc = nn.Linear(model.fc.in_features, num_classes)

#     # Charger les poids entraînés depuis le fichier .pth, en s'assurant de charger sur CPU
#     model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

#     # Définir l'appareil (GPU si disponible, sinon CPU)
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     model = model.to(device)  # Envoyer le modèle au GPU/CPU

#     return model, device

# # Déterminer le chemin du fichier modèle en fonction de l'environnement
# current_dir = os.getcwd()

# # Chemin potentiel en local ou en production
# possible_paths = [
#     os.path.join(current_dir, 'models', 'medical_model_combined_finetuned.pth'),  # Cas local
#     os.path.join(current_dir, 'backend', 'models', 'medical_model_combined_finetuned.pth')  # Cas Railway ou prod
# ]

# # Sélectionner le chemin valide
# model_path = None
# for path in possible_paths:
#     if os.path.exists(path):
#         model_path = path
#         break

# # Si aucun chemin n'est trouvé, lever une exception
# if model_path is None:
#     raise FileNotFoundError(f"Le fichier du modèle n'a pas été trouvé dans les chemins suivants : {possible_paths}")

# # Charger le modèle avec le chemin correct
# model, device = load_model(model_path, num_classes=4)
import os
import torch
import torch.nn as nn

# Définir la classe du modèle simple pour correspondre à celle utilisée lors de la sauvegarde
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc = nn.Linear(10, 2)  # Une couche linéaire (dense)

    def forward(self, x):
        return self.fc(x)

# Fonction pour charger le modèle simple depuis le chemin local
def load_model(model_path):
    """
    Charge un modèle simple avec une couche linéaire.
    :param model_path: Chemin vers le fichier du modèle (fichier .pth)
    :return: Modèle chargé et prêt à être utilisé pour les prédictions, et l'appareil (GPU/CPU)
    """
    # Initialiser le modèle simple
    model = SimpleModel()

    # Charger les poids entraînés depuis le fichier .pth, en s'assurant de charger sur CPU
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

    # Définir l'appareil (GPU si disponible, sinon CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)  # Envoyer le modèle au GPU/CPU

    return model, device

# Afficher le répertoire de travail actuel
print("Répertoire de travail actuel :", os.getcwd())

# Lister les fichiers et dossiers dans le répertoire de travail actuel
print("Contenu du répertoire de travail :")
for root, dirs, files in os.walk(os.getcwd()):
    level = root.replace(os.getcwd(), '').count(os.sep)
    indent = ' ' * 4 * (level)
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 4 * (level + 1)
    for f in files:
        print(f"{subindent}{f}")

# Déterminer le chemin du fichier modèle (ici simple_model.pth dans le répertoire 'models')
current_dir = os.getcwd()  # Répertoire de travail actuel (backend)
model_path = os.path.join(current_dir, 'models', 'simple_model.pth')

# Afficher le chemin du fichier modèle
print(f"Chemin du fichier modèle : {model_path}")

# Vérifier si le fichier existe
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Le fichier du modèle n'a pas été trouvé à l'emplacement : {model_path}")

# Charger le modèle simple
model, device = load_model(model_path)
print("Modèle simple chargé avec succès.")
