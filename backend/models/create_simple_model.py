import torch
import torch.nn as nn

# Définir un modèle simple (un réseau linéaire ici)
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc = nn.Linear(10, 2)  # Une couche linéaire (dense)

    def forward(self, x):
        return self.fc(x)

# Initialiser le modèle
model = SimpleModel()

# Sauvegarder les poids du modèle
model_path = 'simple_model.pth'
torch.save(model.state_dict(), model_path)
print(f"Modèle simple sauvegardé dans {model_path}")
