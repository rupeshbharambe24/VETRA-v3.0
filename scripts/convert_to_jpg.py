import os
from PIL import Image

def convert_to_jpg(source_dir, dest_dir):
    """
    Converts all supported images in the source directory to JPEG format 
    and saves them in the destination directory.
    
    Args:
        source_dir (str): The path to the folder containing the original images.
        dest_dir (str): The path where the new JPEG images will be saved.
    """
    # Define supported image extensions to look for
    SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')
    
    # 1. Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Created destination directory: {dest_dir}")

    # 2. Iterate over all files in the source directory
    for filename in os.listdir(source_dir):
        # Full path to the original image
        source_path = os.path.join(source_dir, filename)
        
        # Check if the file is a supported image and not a directory
        if os.path.isfile(source_path) and filename.lower().endswith(SUPPORTED_EXTENSIONS):
            try:
                # Open the image
                img = Image.open(source_path)
                
                # Get the base name (without extension) for the new filename
                base_name, _ = os.path.splitext(filename)
                
                # 3. Define the new filename and path
                new_filename = f"{base_name}.jpg"
                dest_path = os.path.join(dest_dir, new_filename)
                
                # 4. Convert and Save as JPEG
                # The 'quality' parameter (0-100) is optional; default is 75.
                # Use RGB mode for JPEG conversion, as PNGs might have an alpha channel (RGBA).
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                    
                img.save(dest_path, "JPEG", quality=90)
                print(f"Converted and saved: {filename} -> {new_filename}")
                
            except Exception as e:
                print(f"Could not process {filename}: {e}")
        else:
            print(f"Skipping non-image file or directory: {filename}")

# --- Configuration ---
# Set the paths for your folders
SOURCE_FOLDER = r"D:\Projects\VETRA\Codes\VETRA v3.0\v3.0_Data\left_side_view_jpg" 
DESTINATION_FOLDER = r"D:\Projects\VETRA\Codes\VETRA v3.0\v3.0_Data\left_side_view_jpg"

# Call the function to start the process
if __name__ == "__main__":
    # IMPORTANT: Replace the placeholder paths above with your actual folder paths!
    convert_to_jpg(SOURCE_FOLDER, DESTINATION_FOLDER)