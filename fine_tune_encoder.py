import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from backend.config import settings
from ml.encoder.encoder import Encoder
from ml.utils.transforms import train_transform
from ml.fewshot.prototypes import compute_prototypes
from ml.open_set.threshold import compute_open_set_threshold

def fine_tune():
    print("🚀 Starting Deep Fine-Tuning (Epochs & Loss)...")
    print("-" * 50)

    # 1. Setup Device & Data
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    train_dir = settings.TRAIN_DATA_DIR
    encoder_path = settings.ENCODER_PATH
    
    if not os.path.exists(train_dir):
        print("❌ Data directory not found!")
        return

    dataset = ImageFolder(train_dir, transform=train_transform)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    num_classes = len(dataset.classes)
    print(f"Found {num_classes} classes. Training on {len(dataset)} images.")

    # 2. Setup Model
    print("Loading Encoder...")
    model = Encoder(embedding_dim=128)
    if os.path.exists(encoder_path):
        try:
            model.load_state_dict(torch.load(encoder_path, map_location=device))
            print("Loaded existing weights.")
        except:
            print("Could not load existing weights, starting from scratch (ImageNet).")
    
    model.to(device)
    
    # Add a temporary classification head for Fine-Tuning
    # The Encoder outputs 128-dim embeddings. We map 128 -> num_classes
    head = nn.Linear(128, num_classes).to(device)
    
    # 3. Training Setup
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(list(model.parameters()) + list(head.parameters()), lr=0.0001)
    
    EPOCHS = 20
    
    # 4. Training Loop
    model.train()
    head.train()
    
    for epoch in range(EPOCHS):
        running_loss = 0.0
        correct = 0
        total = 0
        
        for images, labels in dataloader:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            
            embeddings = model(images)
            outputs = head(embeddings)
            
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
        epoch_loss = running_loss / len(dataloader)
        epoch_acc = 100 * correct / total
        print(f"Epoch [{epoch+1}/{EPOCHS}] | Loss: {epoch_loss:.4f} | Accuracy: {epoch_acc:.2f}%")

    # 5. Save the Fine-Tuned Encoder
    print("-" * 50)
    print("💾 Saving fine-tuned encoder...")
    torch.save(model.state_dict(), encoder_path)
    print("✅ Encoder saved.")

    # 6. Re-Compute Prototypes & Threshold
    print("\n🔄 Updating Prototypes & Threshold...")
    prototypes, class_names = compute_prototypes(encoder_path, train_dir, device)
    threshold = compute_open_set_threshold(encoder_path, train_dir, device, percentile=10.0) # Using 10th percentile
    
    print(f"✅ Re-computed prototypes for {len(class_names)} classes.")
    print(f"✅ New Open-Set Threshold: {threshold:.4f}")
    
    print("\n🎉 Model successfully fine-tuned and updated!")
    print("Please restart your backend server.")

if __name__ == "__main__":
    fine_tune()
