import torch
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from backend.config import settings
from ml.fewshot.prototypes import compute_prototypes
from ml.open_set.threshold import compute_open_set_threshold

def train_model():
    print("🚀 Starting Model Training (Prototype Computation)...")
    print("-" * 50)
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    encoder_path = settings.ENCODER_PATH
    train_dir = settings.TRAIN_DATA_DIR
    
    if not os.path.exists(train_dir):
        print(f"❌ Error: Training directory not found at {train_dir}")
        return

    # 1. Compute Prototypes
    print("\n📸 Computing Class Prototypes...")
    prototypes, class_names = compute_prototypes(encoder_path, train_dir, device)
    
    print(f"✅ Prototypes computed for {len(class_names)} classes:")
    for name in class_names:
        print(f"   - {name}")
        
    # 2. Compute Threshold
    print("\n🔍 Optimizing Open-Set Threshold...")
    # Using 20.0 percentile for stricter checking
    threshold = compute_open_set_threshold(encoder_path, train_dir, device, percentile=20.0)
    
    print(f"✅ Optimal Threshold calculated: {threshold:.4f}")
    print("\n🎉 Training Complete! The model is ready.")
    print("Please restart your backend server to load these new parameters.")

if __name__ == "__main__":
    train_model()
