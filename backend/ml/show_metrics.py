import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import numpy as np
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

from backend.config import settings
from backend.ml.encoder import Encoder
from backend.ml.transforms import inference_transform, train_transform

def show_metrics():
    TRAIN_DIR = os.path.join(project_root, "data", "fewshot", "train")
    TEST_DIR = os.path.join(project_root, "data", "fewshot", "test")
    ENCODER_PATH = os.path.join(project_root, "backend", "ml", "encoder_supcon.pth")
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    BATCH_SIZE = 32

    print(f"Train Source: {TRAIN_DIR}")
    print(f"Test Source:  {TEST_DIR}")
    print(f"Model:        {ENCODER_PATH}")
    print("-" * 50)
    model = Encoder()
    try:
        model.load_state_dict(torch.load(ENCODER_PATH, map_location=DEVICE))
    except FileNotFoundError:
        print("Error: Model file not found.")
        return
    model.to(DEVICE)
    model.eval()
    train_dataset = ImageFolder(TRAIN_DIR, transform=train_transform) # Train transform for prototypes
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    prototypes = {}
    counts = {}
    
    with torch.no_grad():
        for images, labels in train_loader:
            images = images.to(DEVICE)
            features = model(images)
            for f, l in zip(features, labels):
                l_item = l.item()
                if l_item not in prototypes:
                    prototypes[l_item] = f.clone()
                    counts[l_item] = 1
                else:
                    prototypes[l_item] += f
                    counts[l_item] += 1
                    
    for l in prototypes:
        prototypes[l] /= counts[l]
        
    class_names = train_dataset.classes
    print(f"Prototypes computed for {len(class_names)} classes.")
    test_dataset = ImageFolder(TEST_DIR, transform=inference_transform) 
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    y_true = []
    y_pred = []
    
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(DEVICE)
            embeddings = model(images)
            embeddings = F.normalize(embeddings, dim=1)
            
            for i in range(len(embeddings)):
                emb = embeddings[i]
                max_sim = -1
                best_label = -1
                
                for p_idx, p_vec in prototypes.items():
                    p_vec = p_vec.to(DEVICE)
                    sim = F.cosine_similarity(emb.unsqueeze(0), p_vec.unsqueeze(0)).item()
                    if sim > max_sim:
                        max_sim = sim
                        best_label = p_idx
                
                y_true.append(labels[i].item())
                y_pred.append(best_label)
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    
    print("\n" + "="*30)
    print(f"FINAL METRICS")
    print("="*30)
    print(f"Accuracy:  {acc*100:.2f}%")
    print(f"Precision: {prec*100:.2f}%")
    print(f"Recall:    {rec*100:.2f}%")
    print(f"F1 Score:  {f1*100:.2f}%")
    print("="*30)
    print("\nDetailed Classification Report:")
    print(classification_report(y_true, y_pred, target_names=class_names, digits=4))

if __name__ == "__main__":
    show_metrics()
