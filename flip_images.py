import os
from PIL import Image

def flip_images_in_folder(source_dir, dest_dir):
    """
    Flips all images in the source directory horizontally and saves them 
    to the destination directory.
    
    Args:
        source_dir (str): The path to the folder containing the original images.
        dest_dir (str): The path where the flipped images will be saved.
    """
    # 1. Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Created destination directory: {dest_dir}")

    # 2. Iterate over all files in the source directory
    for filename in os.listdir(source_dir):
        # Full path to the original image
        source_path = os.path.join(source_dir, filename)
        
        # Check if the file is a supported image (basic check)
        # Pillow handles most common formats (JPG, PNG, BMP, etc.)
        if os.path.isfile(source_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            try:
                # Open the image
                img = Image.open(source_path)
                
                # 3. Perform the Horizontal Flip
                flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
                # 
                
                # Full path for the new flipped image
                dest_path = os.path.join(dest_dir, filename)
                
                # 4. Save the flipped image to the destination folder
                flipped_img.save(dest_path)
                print(f"Flipped and saved: {filename} -> {dest_path}")
                
            except Exception as e:
                print(f"Could not process {filename}: {e}")
        else:
            print(f"Skipping non-image file: {filename}")

# --- Configuration ---
# Set the paths for your folders
SOURCE_FOLDER = r"D:\Projects\VETRA\Codes\VETRA v3.0\v3.0_Data\FinalDataset\right_side_view" 
DESTINATION_FOLDER = r"D:\Projects\VETRA\Codes\VETRA v3.0\v3.0_Data\FinalDataset\left_side_view"

# Call the function to start the process
if __name__ == "__main__":
    # IMPORTANT: Replace the placeholder paths above with your actual folder paths!
    flip_images_in_folder(SOURCE_FOLDER, DESTINATION_FOLDER)