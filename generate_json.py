# For every image in a single folder

import json
from pathlib import Path
import SimpleITK as sitk

# get list of .nii.gz files inside the given folder
folder = Path("C:\\Users\\catar\\OneDrive - Universidade de Coimbra\\Ambiente de Trabalho\\Master Thesis\\Dataset SynthRAD\\Task1\\pelvis\\1PA001\\")
output_json_file = "dataset_structure.json"

# Extract patient ID from the folder name (last three characters)
patient_id = folder.stem[-3:]

# Prepare an empty dictionary to store the structured data
dataset_structure = {}
dataset_structure[patient_id] = {"Images": []}

image_paths = filter(lambda f: str(f).endswith("ct.nii.gz") or str(f).endswith("mr.nii.gz"), folder.iterdir())

for image_path in image_paths:
    # Read the image
    itk_image = sitk.ReadImage(str(image_path))

    # Check if the image is CT or MRI
    if "ct" in image_path.stem.lower():
        origin_position = itk_image.GetOrigin()
        direction_orientation = itk_image.GetDirection()
        modality = "CT"

        # Construct image data dictionary
        image_data = {
            "FilePath": str(image_path),
            "Image Position (Patient)": origin_position,
            "Image Orientation": direction_orientation,
            "Modality": modality
        }
    else:
        origin_position = itk_image.GetOrigin()
        direction_orientation = itk_image.GetDirection()
        modality = "MRI"
        
        # Construct image data dictionary
        image_data = {
            "FilePath": str(image_path),
            "Image Position (Patient)": origin_position,
            "Image Orientation": direction_orientation,
            "Modality": modality
        }

    # Append the image data to the patient’s images
    dataset_structure[patient_id]["Images"].append(image_data)

# Save the structured dataset to a JSON file
with open(output_json_file, "w") as outfile:
    json.dump(dataset_structure, outfile, indent=4)