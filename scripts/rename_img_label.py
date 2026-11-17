import os
import shutil
from pathlib import Path

# --- Configuration (Adjust these paths) ---

# Source folders (your current dataset)
SOURCE_IMAGES_DIR = Path(r"D:\Projects\VETRA\Codes\VETRA v3.0\v3.0_Data\udder-bottom-images")
SOURCE_LABELS_DIR = Path(r"D:\Projects\VETRA\Codes\VETRA v3.0\Training and Processing\udder-bottom-labels")

# Destination folders (where the new, renamed files will go)
DEST_ROOT = Path("udder-bottom-dataset")
DEST_IMAGES_DIR = DEST_ROOT / "images"
DEST_LABELS_DIR = DEST_ROOT / "labels"

# File extensions
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']
LABEL_EXTENSION = '.txt'

def copy_and_rename_dataset(
    source_images: Path,
    source_labels: Path,
    dest_images: Path,
    dest_labels: Path
):
    """
    Copies and sequentially renames matching image and label files 
    from source to destination directories.
    """
    print("--- Starting Dataset Renaming and Copy ---")

    # 1. Ensure destination directories exist
    os.makedirs(dest_images, exist_ok=True)
    os.makedirs(dest_labels, exist_ok=True)
    print(f"Destination directories created/verified at: {DEST_ROOT}")

    # 2. Collect all image files
    all_image_paths = []
    for ext in IMAGE_EXTENSIONS:
        all_image_paths.extend(source_images.glob(f'*{ext}'))

    # 3. Process and rename files sequentially
    copy_count = 0
    
    # Sort files to ensure a consistent renaming order
    sorted_image_paths = sorted(all_image_paths) 

    for original_img_path in sorted_image_paths:
        # Determine the corresponding label path
        base_name = original_img_path.stem
        original_label_path = source_labels / f"{base_name}{LABEL_EXTENSION}"

        # Check if a matching label file exists
        if original_label_path.is_file():
            # Generate the new sequential name (e.g., 000001)
            new_file_index = copy_count + 1
            new_name_stem = f"{new_file_index:06d}" # Use 6 digits for leading zeros

            # Define new paths
            new_img_path = dest_images / (new_name_stem + original_img_path.suffix)
            new_label_path = dest_labels / (new_name_stem + LABEL_EXTENSION)

            try:
                # Copy and rename the image
                shutil.copy2(original_img_path, new_img_path)
                
                # Copy and rename the label
                shutil.copy2(original_label_path, new_label_path)
                
                copy_count += 1
                
            except Exception as e:
                print(f"Error processing {original_img_path.name}: {e}")
        else:
            print(f"Skipped {original_img_path.name}: No matching label file found.")


    print("\n--- Summary ---")
    print(f"Total matching pairs copied and renamed: **{copy_count}**")
    print("Process complete!")


# --- Execution ---
# NOTE: Ensure your source_dataset/images and source_dataset/labels folders exist 
# and contain files before running.
copy_and_rename_dataset(
    SOURCE_IMAGES_DIR, 
    SOURCE_LABELS_DIR, 
    DEST_IMAGES_DIR, 
    DEST_LABELS_DIR
)