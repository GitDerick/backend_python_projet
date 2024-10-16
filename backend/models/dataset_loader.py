# dataset_loader.py : responsable du chargement des datasets et
# de la gestion des transformations des images.

import torch
from torchvision import datasets, transforms
from torch.utils.data import ConcatDataset, DataLoader

# Prétraitement des images (géré par le CPU)
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def load_datasets(dataset1_train_dir, dataset1_val_dir, dataset2_train_dir, dataset2_val_dir):
    print(f"Chemin dataset1_train_dir: {dataset1_train_dir}")
    print(f"Chemin dataset1_val_dir: {dataset1_val_dir}")
    print(f"Chemin dataset2_train_dir: {dataset2_train_dir}")
    print(f"Chemin dataset2_val_dir: {dataset2_val_dir}")

    # Charger les datasets individuels pour dataset1 et dataset2
    train_dataset1 = datasets.ImageFolder(dataset1_train_dir, transform=transform)
    val_dataset1 = datasets.ImageFolder(dataset1_val_dir, transform=transform)

    train_dataset2 = datasets.ImageFolder(dataset2_train_dir, transform=transform)
    val_dataset2 = datasets.ImageFolder(dataset2_val_dir, transform=transform)

    # Combiner les deux datasets pour l'entraînement et la validation
    train_dataset = ConcatDataset([train_dataset1, train_dataset2])
    val_dataset = ConcatDataset([val_dataset1, val_dataset2])

    print("Datasets chargés avec succès.")

    # Créer les DataLoaders avec num_workers pour paralléliser le chargement des données sur le CPU
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)  # 4 threads CPU pour charger les données
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=4)

    return train_loader, val_loader, train_dataset1.classes
