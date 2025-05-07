import os
import shutil
from textnode import TextNode, TextType

def main():
    copy_directory("static", "public")

def copy_directory(source_dir, dest_dir):
    # Removes destination directly, ensures clean copy
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    # Creates destination directory
    os.mkdir(dest_dir)

    # List all items in source directory
    items = os.listdir(source_dir)

    # Process items
    for item in items:
        # Structure filepaths in both directories
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        # copies item if it is a file
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_dir)
            # NON-ESSENTIAL: log path of copied file for debugging
            print(f"Copied file: {source_path} to {dest_path}")

        # Calls function recursively if item is a directory
        else:
            copy_directory(source_path, dest_path)
            print(f"Copied directory: {source_path} to {dest_path}")



main()