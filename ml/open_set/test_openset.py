import torch

from ml.open_set.threshold import compute_open_set_threshold
from ml.fewshot.prototypes import compute_prototypes
from ml.fewshot.classifier import PrototypeClassifier
from ml.reasoning.api_reasoner import generate_ai_advisory
from ml.intelligence.agro_intelligence import assess_disease_intelligence


def test_open_set():
    # Device setup
    device = "cuda" if torch.cuda.is_available() else "cpu"

    encoder_path = "ml/encoder/encoder_supcon.pth"
    train_dir = "data/fewshot/train"

    # ----------------------------------------------------
    # 1️⃣ Compute open-set threshold
    # ----------------------------------------------------
    threshold = compute_open_set_threshold(
        encoder_path, train_dir, device
    )

    # ----------------------------------------------------
    # 2️⃣ Compute prototypes
    # ----------------------------------------------------
    prototypes, class_names = compute_prototypes(
        encoder_path, train_dir, device
    )

    # ----------------------------------------------------
    # 3️⃣ Initialize classifier
    # ----------------------------------------------------
    classifier = PrototypeClassifier(
        encoder_path, prototypes, class_names, device
    )

    print(f"\nOpen-set threshold: {threshold:.3f}")

    # ----------------------------------------------------
    # 4️⃣ Test image (MAKE SURE THIS PATH EXISTS)
    # ----------------------------------------------------
    image_path = "data/fewshot/test/Potato_Late_Blight/b9aecfc3-98d5-467a-8773-ee2905918c71___RS_LB 5161.jpg"

    # ----------------------------------------------------
    # 5️⃣ Predict disease
    # ----------------------------------------------------
    pred, confidence = classifier.predict(image_path, threshold)

    print(f"\nPrediction : {pred}")
    print(f"Confidence : {confidence:.3f}")

    # ----------------------------------------------------
    # 6️⃣ AI REASONING + INTELLIGENCE
    # ----------------------------------------------------
    if pred != "UNKNOWN":
        crop = pred.split("___")[0]
        severity = "High" if confidence >= 0.9 else "Medium"

        # ---------- AI Reasoning ----------
        print("\n--- AI ADVISORY (Disease-Specific) ---\n")

        advisory = generate_ai_advisory(
            disease=pred,
            crop=crop,
            confidence=confidence,
            severity=severity
        )
        print(advisory)

        # ---------- Intelligence Layer ----------
        cam_coverage = 0.7  # placeholder from Grad-CAM heat spread

        stage, action, yield_loss = assess_disease_intelligence(
            confidence=confidence,
            cam_coverage=cam_coverage
        )

        print("\n--- INTELLIGENCE ASSESSMENT ---")
        print(f"Disease Stage       : {stage}")
        print(f"Recommended Action  : {action}")
        print(f"Expected Yield Loss : {yield_loss}")

    else:
        print("\nDisease Status: UNKNOWN")
        print("Recommended Action: Consult an agricultural expert")


if __name__ == "__main__":
    test_open_set()
