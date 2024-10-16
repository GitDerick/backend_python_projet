from torchvision import datasets, transforms
from torch.utils.data import DataLoader

def load_third_dataset(batch_size=32):
    # Prétraitement des images, même que les deux premiers datasets
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Charger le dataset3 avec ImageFolder, en passant le dossier brain_disease
    train_dataset = datasets.ImageFolder(root='C:/Users/deric/ZProjetStage/datasets/dataset3/brain_disease', transform=transform)

    # Créer un DataLoader pour charger les données par batchs
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)

    return train_loader, train_dataset.classes  # Retourner également les classes
