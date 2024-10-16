from tqdm import tqdm
import torch
from torch import nn, optim
from torchvision import models
from dataset_loader import load_datasets

def train_model(num_epochs=10):
    # Spécifier l'utilisation du GPU 0 (NVIDIA GeForce RTX 3050) ou CPU si CUDA n'est pas disponible
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Device utilisé pour l'entraînement : {device}")

    # Chemins d'accès aux datasets
    dataset1_train_dir = 'C:/Users/deric/ZProjetStage/datasets/dataset1/Train'
    dataset1_val_dir = 'C:/Users/deric/ZProjetStage/datasets/dataset1/Val'
    dataset2_train_dir = 'C:/Users/deric/ZProjetStage/datasets/dataset2/Train'
    dataset2_val_dir = 'C:/Users/deric/ZProjetStage/datasets/dataset2/Val'

    print("Chargement des datasets...")
    # Charger les datasets avec des travailleurs parallèles (CPU)
    train_loader, val_loader, classes = load_datasets(dataset1_train_dir, dataset1_val_dir, dataset2_train_dir, dataset2_val_dir)

    print(f"Classes détectées : {classes}")
    print(f"Taille du dataset d'entraînement : {len(train_loader.dataset)}")
    print(f"Taille du dataset de validation : {len(val_loader.dataset)}")

    # Charger le modèle ResNet50 pré-entraîné
    print("Chargement du modèle ResNet50 pré-entraîné...")
    model = models.resnet50(pretrained=True)

    # Remplacer la dernière couche pour correspondre au nombre de classes (opacity, normal)
    num_classes = len(classes)
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    # Envoyer le modèle au GPU pour les calculs lourds
    model = model.to(device)

    # Définir la fonction de perte et l'optimiseur
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    print("Début de l'entraînement du modèle...")

    # Entraînement du modèle
    for epoch in range(num_epochs):
        print(f"Époque {epoch+1}/{num_epochs} en cours...")
        model.train()
        running_loss = 0.0

        # Barre de progression pour l'entraînement
        train_progress = tqdm(train_loader, desc=f"Époque {epoch+1}/{num_epochs}", unit="batch")
        for inputs, labels in train_progress:
            # Envoyer les images et labels au GPU pour les calculs
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()

            # Calcul des prédictions et de la perte (GPU)
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            # Rétropropagation et mise à jour des poids (GPU)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            # Mise à jour de la barre de progression avec la perte moyenne en temps réel
            train_progress.set_postfix(loss=running_loss / len(train_loader))

        print(f"Loss après l'époque {epoch+1}: {running_loss/len(train_loader):.4f}")

        # Validation après chaque époque
        print(f"Validation pour l'époque {epoch+1} en cours...")
        model.eval()
        val_loss = 0.0
        correct = 0
        total = 0

        # Barre de progression pour la validation
        val_progress = tqdm(val_loader, desc=f"Validation Époque {epoch+1}/{num_epochs}", unit="batch")
        with torch.no_grad():
            for inputs, labels in val_progress:
                # Envoyer les images et labels au GPU pour validation
                inputs, labels = inputs.to(device), labels.to(device)

                # Calcul des prédictions et de la perte (GPU)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item()

                # Calcul des prédictions (GPU)
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

            # Mise à jour de la barre de progression avec la perte moyenne et l'accuracy en temps réel
            val_progress.set_postfix(val_loss=val_loss / len(val_loader), accuracy=100 * correct / total)

        val_loss /= len(val_loader)
        accuracy = 100 * correct / total

        print(f"Validation Loss: {val_loss:.4f}, Accuracy: {accuracy:.2f}%")

    # Sauvegarder le modèle après l'entraînement
    torch.save(model.state_dict(), 'medical_model_combined.pth')
    print("Modèle sauvegardé sous 'medical_model_combined.pth'")

# Le point d'entrée de l'application doit être protégé par "if __name__ == '__main__':"
if __name__ == '__main__':
    train_model(num_epochs=10)
