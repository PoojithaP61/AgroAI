from torchvision import transforms

train_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),  # Focus on the center (leaf)
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2), # Robustness to lighting
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Inference transform
inference_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224), # Focus on the center (leaf)
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])