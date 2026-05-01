import torch
import torch.nn.functional as F
from torchvision.datasets import ImageFolder
from backend.ml.encoder import Encoder
from backend.ml.prototypes import compute_prototypes
from backend.ml.transforms import train_transform, inference_transform
from PIL import Image

def _embed_with_tta(model, pil_image, device: str, tta_samples: int = 20):
    """
    Create an embedding using the same strategy as inference:
    - 1x deterministic inference_transform
    - (tta_samples-1)x train_transform augmentations
    - mean pooled + L2 normalized
    """
    embeddings = []

    std_input = inference_transform(pil_image).unsqueeze(0).to(device)
    with torch.no_grad():
        embeddings.append(F.normalize(model(std_input), dim=1))

    for _ in range(max(0, tta_samples - 1)):
        aug_input = train_transform(pil_image).unsqueeze(0).to(device)
        with torch.no_grad():
            embeddings.append(F.normalize(model(aug_input), dim=1))

    embedding = torch.stack(embeddings).mean(dim=0)
    return F.normalize(embedding, dim=1)


def compute_open_set_threshold(encoder_path, train_dir, device="cpu", percentile=0.5, tta_samples: int = 20):
    model = Encoder()
    model.load_state_dict(torch.load(encoder_path, map_location=device))
    model.to(device)
    model.eval()

    prototypes, class_names = compute_prototypes(encoder_path, train_dir, device)
    # NOTE: we intentionally load PIL images here to use the same embedding pipeline as inference.
    dataset = ImageFolder(train_dir, transform=None)
    similarities = []

    with torch.no_grad():
        for img, label in dataset:
            # img is a PIL image because transform=None
            emb = _embed_with_tta(model, img.convert("RGB"), device=device, tta_samples=tta_samples)

            proto = prototypes[label].unsqueeze(0).to(device)
            proto = F.normalize(proto, dim=1)

            sim = F.cosine_similarity(emb, proto)
            similarities.append(sim.item())

    # Accept both fraction (0-1) and percentage (1-100) inputs for backward compatibility.
    if percentile > 1:
        quantile_value = percentile / 100.0
    else:
        quantile_value = percentile

    threshold = torch.quantile(torch.tensor(similarities), quantile_value).item()

    return threshold
