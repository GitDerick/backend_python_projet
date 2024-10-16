from tqdm import tqdm
import torch
from torch import nn, optim
from torchvision import models
from train_thirdData import load_third_dataset  # Charger la fonction de chargement du 3ème dataset

def fine_tune_model(model_path='medical_model_combined.pth', num_epochs=5):
    # Spécifier l'utilisation du GPU ou CPU
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Device utilisé pour l'entraînement : {device}")

    # Charger le modèle existant
    print("Chargement du modèle pré-entraîné...")
    model = models.resnet50(pretrained=False)  # Ne pas re-télécharger les poids ImageNet
    model.fc = nn.Linear(model.fc.in_features, 4)  # 4 classes dans dataset3: glioma, meningioma, normal, pituitary

    # Charger les poids déjà entraînés, en ignorant la dernière couche fc
    state_dict = torch.load(model_path)
    state_dict.pop('fc.weight', None)  # Supprimer les poids de la dernière couche
    state_dict.pop('fc.bias', None)    # Supprimer les biais de la dernière couche
    model.load_state_dict(state_dict, strict=False)  # Charger le reste du modèle
    model = model.to(device)

    # Charger le troisième dataset (brain_disease)
    print("Chargement du 3ème dataset...")
    train_loader, classes = load_third_dataset()

    print(f"Classes dans le 3ème dataset : {classes}")

    # Définir la fonction de perte et l'optimiseur
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.0001)  # Apprentissage lent pour fine-tuning

    print("Début du fine-tuning du modèle...")

    # Fine-tuning du modèle avec le troisième dataset
    for epoch in range(num_epochs):
        print(f"Époque {epoch+1}/{num_epochs} en cours...")
        model.train()
        running_loss = 0.0

        # Barre de progression pour l'entraînement
        train_progress = tqdm(train_loader, desc=f"Époque {epoch+1}/{num_epochs}", unit="batch")
        for inputs, labels in train_progress:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            train_progress.set_postfix(loss=running_loss / len(train_loader))

        print(f"Loss après l'époque {epoch+1}: {running_loss/len(train_loader):.4f}")

    # Sauvegarder les poids finement ajustés
    torch.save(model.state_dict(), 'medical_model_combined_finetuned.pth')
    print("Modèle sauvegardé sous 'medical_model_combined_finetuned.pth'")

# Appel de la fonction de fine-tuning
if __name__ == '__main__':
    fine_tune_model(num_epochs=5)
