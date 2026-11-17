import os
from pathlib import Path

def delete_unlabeled_images(image_dir, label_dir):
    """
    Checks the image directory against the label directory and deletes 
    any image file that does not have a corresponding text label file.
    
    Args:
        image_dir (str): Path to the folder containing images.
        label_dir (str): Path to the folder containing label text files (.txt).
    """
    
    # Use Path for robust path handling
    images_path = Path(image_dir)
    labels_path = Path(label_dir)
    
    # 1. Define supported image extensions
    SUPPORTED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
    
    deleted_count = 0
    
    # 2. Iterate through all files in the image directory
    for image_file in images_path.iterdir():
        # Check if it's a file and has a supported image extension
        if image_file.is_file() and image_file.suffix.lower() in SUPPORTED_EXTENSIONS:
            
            # Get the base filename (e.g., 'image_001')
            base_name = image_file.stem
            
            # 3. Construct the expected label file path (e.g., 'labels/image_001.txt')
            label_file = labels_path / f"{base_name}.txt"
            
            # 4. Check if the label file exists
            if not label_file.exists():
                
                # 5. If missing, delete the image file
                try:
                    os.remove(str(image_file))
                    print(f"DELETED: {image_file.name} (Missing label: {label_file.name})")
                    deleted_count += 1
                except OSError as e:
                    print(f"Error deleting {image_file.name}: {e}")

    print("-" * 30)
    print(f"Finished check. Total images deleted: {deleted_count}")
    if deleted_count == 0:
        print("All images have corresponding label files.")


# --- Configuration ---
# IMPORTANT: Replace these placeholder paths with your actual folder paths!
IMAGE_FOLDER = r"D:\Projects\VETRA\Data\side_view" 
LABEL_FOLDER = r"D:\Projects\VETRA\Codes\VETRA v3.0\Training and Processing\side-view-16kpt-labels"

# Call the function to start the process
if __name__ == "__main__":
    # WARNING: This script permanently deletes files. 
    # Please backup your image folder before running!
    print("Starting process to remove unlabeled images...")
    delete_unlabeled_images(IMAGE_FOLDER, LABEL_FOLDER)