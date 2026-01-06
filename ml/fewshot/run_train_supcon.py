import torch
from ml.fewshot.train_supcon import train_supcon

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    model = train_supcon(
        data_dir="data/fewshot/train",
        epochs=20,          # accuracy-focused
        batch_size=16,
        lr=1e-3,
        device=device
    )

    # Save trained encoder
    save_path = "ml/encoder/encoder_supcon.pth"
    torch.save(model.state_dict(), save_path)
    print(f"Encoder saved at {save_path}")

if __name__ == "__main__":
    main()
