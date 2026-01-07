import shutil
import os

def restore_dataset():
    source = "data/fewshot/train_backup"
    destination = "data/fewshot/train"

    if not os.path.exists(source):
        print(f"Error: Backup directory '{source}' does not exist! Cannot restore.")
        return

    confirmation = input(f"⚠️  WARNING: This will overwrite '{destination}' with the backup. Are you sure? (yes/no): ")
    if confirmation.lower() != "yes":
        print("Restore cancelled.")
        return

    try:
        if os.path.exists(destination):
            shutil.rmtree(destination)
            print(f"Removed current '{destination}'")

        shutil.copytree(source, destination)
        print(f"✅ Success: Dataset restored from '{source}'")
    except Exception as e:
        print(f"❌ Error during restore: {str(e)}")

if __name__ == "__main__":
    restore_dataset()
