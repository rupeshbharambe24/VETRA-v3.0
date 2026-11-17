import os
import random
import shutil

def rename_images_randomly(source_dir, dest_dir):
    """
    Randomly shuffles and renames all supported images from a source folder,
    copying them to a destination folder with sequential names (1, 2, 3...).
    
    Args:
        source_dir (str): The path to the folder with the original images.
        dest_dir (str): The path where the sequentially named copies will be saved.
    """
    # Define supported image extensions
    SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
    
    # 1. Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Created destination directory: {dest_dir}")
    
    # 2. Get a list of all supported image files
    image_files = []
    for filename in os.listdir(source_dir):
        if filename.lower().endswith(SUPPORTED_EXTENSIONS) and os.path.isfile(os.path.join(source_dir, filename)):
            image_files.append(filename)
            
    if not image_files:
        print(f"No supported images found in the source directory: {source_dir}")
        return

    # 3. Randomly shuffle the list of filenames
    random.shuffle(image_files)
    print(f"Found {len(image_files)} images and shuffled their order.")

    # 4. Loop through the shuffled list and rename sequentially
    for index, original_filename in enumerate(image_files, start=1):
        # Get the original file extension (e.g., .jpg, .png)
        _, ext = os.path.splitext(original_filename)
        
        # Create the new sequential name (e.g., "1.jpg", "2.png")
        new_filename = f"{index}{ext}"
        
        # Define full paths
        source_path = os.path.join(source_dir, original_filename)
        dest_path = os.path.join(dest_dir, new_filename)
        
        try:
            # Copy the file to the new destination with the new name
            shutil.copy2(source_path, dest_path)
            print(f"Copied: {original_filename} -> {new_filename}")
            
        except Exception as e:
            print(f"Error copying {original_filename}: {e}")

# --- Configuration ---
# IMPORTANT: Replace these placeholder paths with your actual folder paths!
SOURCE_FOLDER = r"D:\Projects\VETRA\Codes\VETRA v3.0\v3.0_Data\udder-bottom-images" 
DESTINATION_FOLDER = r"D:\Projects\VETRA\Codes\VETRA v3.0\Training and Processing\udder_bottom_dataset"

# Call the function to start the process
if __name__ == "__main__":
    rename_images_randomly(SOURCE_FOLDER, DESTINATION_FOLDER)