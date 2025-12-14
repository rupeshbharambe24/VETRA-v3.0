import os
from pathlib import Path

# --- Configuration ---
# IMPORTANT: Update these paths to match your directory structure
IMAGES_DIR = Path("D:\Projects\VETRA\Data\side_view")
LABELS_DIR = Path("D:\Projects\VETRA\Codes\VETRA v3.0\Training and Processing\side-view-16kpt-labels")
SUPPORTED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']
LABEL_EXTENSION = '.txt'

def sync_and_clean_data(images_dir: Path, labels_dir: Path):
    """
    Synchronizes images and labels: keeps only matching pairs
    with supported image extensions.
    """
    print(f"Starting data cleanup...")

    # 1. Get all base names from the labels folder
    label_basenames = {
        p.stem
        for p in labels_dir.glob(f'*{LABEL_EXTENSION}')
        if p.is_file()
    }
    print(f"Found {len(label_basenames)} unique label files.")

    # 2. Process all image files
    all_images = list(images_dir.iterdir())
    images_cleaned = 0
    
    for image_path in all_images:
        if image_path.is_file():
            # Check for supported image format
            is_supported_format = image_path.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS

            # Check for corresponding label
            has_label = image_path.stem in label_basenames
            
            if not is_supported_format or not has_label:
                # Case 1: Image is unsupported OR label is missing
                
                print(f"🗑️ Deleting unsupported/unlabeled image: {image_path.name}")
                os.remove(image_path)
                images_cleaned += 1
                
                # If the image was deleted because its format was wrong,
                # we don't need to do anything with the label yet.
                
                # If the image was deleted because the label was missing,
                # we don't need to touch the labels folder either.

    print(f"\n--- Phase 1 Complete ---")
    print(f"Deleted {images_cleaned} images (unsupported format or missing label).")
    
    # 3. Process all label files (to check for deleted/missing images)
    labels_cleaned = 0
    all_labels = list(labels_dir.glob(f'*{LABEL_EXTENSION}'))
    
    for label_path in all_labels:
        if label_path.is_file():
            found_image = False
            
            # Check all supported extensions to see if the image exists
            for ext in SUPPORTED_IMAGE_EXTENSIONS:
                image_path_check = images_dir / f"{label_path.stem}{ext}"
                if image_path_check.is_file():
                    found_image = True
                    break

            if not found_image:
                # Case 2: Label exists, but the corresponding (and supported) image is missing
                print(f"🗑️ Deleting unattached label: {label_path.name}")
                os.remove(label_path)
                labels_cleaned += 1

    print(f"\n--- Cleanup Summary ---")
    print(f"Total Images Deleted: {images_cleaned}")
    print(f"Total Labels Deleted: {labels_cleaned}")
    print("Cleanup successful. Your dataset is synchronized!")


# --- Execute the function ---
# Make sure to run this script from the parent directory 
# containing the 'images' and 'labels' folders, or adjust the paths above.
sync_and_clean_data(IMAGES_DIR, LABELS_DIR)