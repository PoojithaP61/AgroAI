import shutil
import os
import datetime

def backup_dataset():
    source = "data/fewshot/train"
    destination = "data/fewshot/train_backup"

    if not os.path.exists(source):
        print(f"Error: Source directory '{source}' does not exist!")
        return

    if os.path.exists(destination):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        destination = f"{destination}_{timestamp}"
        print(f"Backup already exists. Creating new backup at: {destination}")

    try:
        shutil.copytree(source, destination)
        print(f"✅ Success: Dataset backed up to '{destination}'")
    except Exception as e:
        print(f"❌ Error during backup: {str(e)}")

if __name__ == "__main__":
    backup_dataset()
