import os
import shutil
import exifread
from datetime import datetime

def get_capture_date(file_path):
    with open(file_path, 'rb') as image_file:
        tags = exifread.process_file(image_file, details=False)
        if 'EXIF DateTimeOriginal' in tags:
            capture_date = str(tags['EXIF DateTimeOriginal'])
            capture_date = capture_date.split()[0].replace(':', '-')
            return capture_date
    return None

def organize_images(source_dir, destination_dir):
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif')

    for filename in os.listdir(source_dir):
        if filename.endswith(image_extensions):
            file_path = os.path.join(source_dir, filename)
            capture_date = get_capture_date(file_path)
            if capture_date is None:
                modified_date = datetime.fromtimestamp(os.path.getmtime(file_path))
                capture_date = modified_date.strftime('%Y-%m-%d')
            
            destination_folder = os.path.join(destination_dir, capture_date)
            os.makedirs(destination_folder, exist_ok=True)
            destination_path = os.path.join(destination_folder, filename)
            shutil.move(file_path, destination_path)
            print(f"Moved {filename} to {destination_path}")

# Get the directory where the main script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Use the script directory as the source and destination directory
source_directory = script_directory
destination_directory = script_directory

organize_images(source_directory, destination_directory)
