"""
ML Service Layer - Initializes and manages ML models
"""
import torch
import os
from typing import Dict, Tuple
from ml.encoder.encoder import Encoder
from ml.fewshot.classifier import PrototypeClassifier
from ml.fewshot.prototypes import compute_prototypes
from ml.open_set.threshold import compute_open_set_threshold
from backend.config import settings


class MLService:
    """Singleton service for ML model management"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.device = settings.DEVICE
            if self.device == "cuda" and not torch.cuda.is_available():
                print("CUDA not available, using CPU")
                self.device = "cpu"
            
            self.classifier: PrototypeClassifier = None
            self.prototypes: Dict = None
            self.class_names: Tuple = None
            self.threshold: float = None
            self._initialized = True
    
    def initialize(self):
        """Initialize ML models and prototypes"""
        if self.classifier is not None:
            print("ML models already initialized")
            return
        
        print("Initializing ML models...")
        
        encoder_path = settings.ENCODER_PATH
        train_dir = settings.TRAIN_DATA_DIR
        
        if not os.path.exists(encoder_path):
            raise FileNotFoundError(f"Encoder model not found at {encoder_path}")
        
        if not os.path.exists(train_dir):
            raise FileNotFoundError(f"Training data directory not found at {train_dir}")
        
        # Compute open-set threshold
        print("Computing open-set threshold...")
        # increased percentile from default 0.5 to 15.0 to filter unknown classes better
        self.threshold = compute_open_set_threshold(
            encoder_path, train_dir, self.device, percentile=15.0
        )
        print(f"Open-set threshold: {self.threshold:.3f}")
        
        # Compute prototypes
        print("Computing prototypes...")
        self.prototypes, self.class_names = compute_prototypes(
            encoder_path, train_dir, self.device
        )
        print(f"Loaded {len(self.class_names)} disease classes")
        
        # Initialize classifier
        print("Initializing classifier...")
        self.classifier = PrototypeClassifier(
            encoder_path, self.prototypes, self.class_names, self.device
        )
        
        print("ML models initialized successfully!")
    
    def get_classifier(self) -> PrototypeClassifier:
        """Get the classifier instance"""
        if self.classifier is None:
            self.initialize()
        return self.classifier
    
    def get_threshold(self) -> float:
        """Get the open-set threshold"""
        if self.threshold is None:
            self.initialize()
        return self.threshold

    def retrain_model(self):
        """Force re-training of the model (re-compute prototypes)"""
        print("🔄 Retraining model with new data...")
        self.classifier = None  # Reset classifier
        
        # Re-run initialization (will re-scan the directories)
        encoder_path = settings.ENCODER_PATH
        train_dir = settings.TRAIN_DATA_DIR
        
        # Re-compute prototypes
        self.prototypes, self.class_names = compute_prototypes(
            encoder_path, train_dir, self.device
        )
        print(f"✅ Reloaded {len(self.class_names)} disease classes")
        
        # Re-initialize classifier
        self.classifier = PrototypeClassifier(
            encoder_path, self.prototypes, self.class_names, self.device
        )
        print("✅ Classifier updated successfully")


# Global ML service instance
ml_service = MLService()
