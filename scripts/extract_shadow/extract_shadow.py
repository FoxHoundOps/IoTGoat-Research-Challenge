import os
import subprocess
import sys
import shutil


def search_shadow_file(directory):
    """
    Recursively searches for the 'shadow' file within the given directory.
    Returns the path to the 'shadow' file if found, otherwise returns None.
    """
    for root, dirs, files in os.walk(directory):
        if "shadow" in files:
            shadow_file = os.path.join(root, "shadow")
            return shadow_file
    return None


def extract_shadow(image_path, output_dir):
    # Check if the image file exists
    if not os.path.isfile(image_path):
        print("Invalid image file path")
        sys.exit(1)

    # Perform binwalk extraction
    print(f"Performing binwalk extraction for '{image_path}'...")
    try:
        subprocess.run(["binwalk", "-e", "--run-as=root", image_path], check=True)
    except subprocess.CalledProcessError:
        print("Error occurred during binwalk extraction")
        return

    # Find the extracted directory
    extracted_dir = None
    for file in os.listdir("."):
        if file.endswith(".extracted") and os.path.isdir(file):
            extracted_dir = file
            break

    if extracted_dir is None:
        print("Extraction directory not found")
        return

    # Search for the shadow file
    print("Searching for shadow file...")
    shadow_file = search_shadow_file(extracted_dir)
    if shadow_file is None:
        print("Shadow file not found")
        return

    # Copy the shadow file to the output directory
    output_file = os.path.join(output_dir, "shadow")
    shutil.copy(shadow_file, output_file)
    print(f"Successfully extracted /etc/shadow to {output_file}")


if __name__ == "__main__":
    # Check the command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python3 extract_shadow.py <image_path> <output_dir>")
        sys.exit(1)

    image_path = sys.argv[1]
    output_dir = sys.argv[2]

    # Extract the shadow file
    extract_shadow(image_path, output_dir)
