import torch
import cv2
import numpy as np
from PIL import Image

from ml.encoder.encoder import Encoder
from ml.explainability.gradcam import GradCAM
from ml.utils.transforms import train_transform

def test_gradcam(image_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = Encoder()
    model.load_state_dict(torch.load("ml/encoder/encoder_supcon.pth", map_location=device))
    model.to(device)
    model.eval()

    # Target layer (last convolution layer)
    target_layer = model.feature_extractor[-1]

    cam_generator = GradCAM(model, target_layer)

    image = Image.open(image_path).convert("RGB")
    input_tensor = train_transform(image).unsqueeze(0).to(device)

    cam = cam_generator.generate(input_tensor, class_idx=0)

    img = cv2.cvtColor(np.array(image.resize((224,224))), cv2.COLOR_RGB2BGR)
    heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)

    overlay = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)

    cv2.imwrite("gradcam_output.jpg", overlay)
    print("Grad-CAM saved as gradcam_output.jpg")

if __name__ == "__main__":
    test_gradcam("data/fewshot/test/Tomato_Bacterial_Spot/13cc9108-fcd9-4e6f-aed4-01813cebc881___UF.GRC_BS_Lab Leaf 8611.jpg")
