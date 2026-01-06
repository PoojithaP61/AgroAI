import torch
import torch.nn.functional as F
from PIL import Image

from ml.encoder.encoder import Encoder
from ml.utils.transforms import inference_transform


class PrototypeClassifier:
    """
    Open-Set Aware Prototype-Based Classifier
    Based on:
    - Snell et al., 2017 (Prototypical Networks)
    - Scheirer et al., 2013 (Open Set Recognition)
    """

    def __init__(self, encoder_path, prototypes, class_names, device="cpu"):
        self.device = device

        # Load trained encoder
        self.model = Encoder()
        self.model.load_state_dict(torch.load(encoder_path, map_location=device))
        self.model.to(device)
        self.model.eval()

        # Store prototypes
        self.prototypes = {
            k: v.to(device) for k, v in prototypes.items()
        }

        # Class names (index -> disease name)
        self.class_names = class_names

    def predict(self, image_path, threshold=0.6):
        """
        Predict disease for a given image.
        Returns:
        - disease name OR 'UNKNOWN'
        - confidence score (cosine similarity)
        """

        # Load and preprocess image
        image = Image.open(image_path).convert("RGB")
        image = inference_transform(image).unsqueeze(0).to(self.device)

        # Extract embedding
        with torch.no_grad():
            embedding = self.model(image)
            embedding = F.normalize(embedding, dim=1)

        # Compute cosine similarity with each prototype
        similarities = {}

        for label, prototype in self.prototypes.items():
            prototype = F.normalize(prototype.unsqueeze(0), dim=1)
            similarity = F.cosine_similarity(embedding, prototype)
            similarities[label] = similarity.item()

        # Best matching class
        best_label = max(similarities, key=similarities.get)
        best_score = similarities[best_label]

        # Open-set rejection
        if best_score < threshold:
            return "UNKNOWN", float(best_score)

        return self.class_names[best_label], float(best_score)
