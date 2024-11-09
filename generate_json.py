# For every image in a single folder

import json
import os
from pathlib import Path
import SimpleITK as sitk

# get list of .nii.gz files inside the given folder
folder = Path("C:\\Users\\catar\\OneDrive - Universidade de Coimbra\\Ambiente de Trabalho\\Master Thesis\\Dataset SynthRAD\\Task1\\pelvis\\")
output_json_file = "Task1_pelvis_structure.json"

# Prepare an empty dictionary to store the structured data
dataset_structure = {}

# Loop through each patient folder in the main directory
for data_folder in folder.iterdir():
    #print(data_folder)
    if data_folder.is_dir() and data_folder.name != "overview":
        # Extract patient ID from the folder name (last three characters)
        patient_id = data_folder.stem[-3:]
        center = data_folder.stem[-4]

        dataset_structure[patient_id] = {"Center": center, "Images": []}

        image_paths = filter(lambda f: str(f).endswith("ct.nii.gz") or str(f).endswith("mr.nii.gz"), data_folder.iterdir())

        for image_path in image_paths:
                # Read the image
                itk_image = sitk.ReadImage(str(image_path))

                # Check if the image is CT or MRI
                if "ct" in image_path.stem.lower():
                        origin_position = itk_image.GetOrigin()
                        direction_orientation = itk_image.GetDirection()
                        spacing = itk_image.GetSpacing()
                        size = itk_image.GetSize()
                        modality = "CT"

                        # Construct image data dictionary
                        image_data = {
                            "Modality": modality,
                            "FilePath": str(image_path),
                            "Origin in physical space": origin_position,
                            "Direction": direction_orientation,
                            "Image Size": size,
                            "Physical size of each pixel": spacing,
                            "Distance between consecutive slices (mm)": spacing[2]
                        }
                else:
                        origin_position = itk_image.GetOrigin()
                        direction_orientation = itk_image.GetDirection()
                        spacing = itk_image.GetSpacing()
                        size = itk_image.GetSize()
                        modality = "MRI"

                        # Construct image data dictionary
                        image_data = {
                            "Modality": modality,
                            "FilePath": str(image_path),
                            "Origin in physical space": origin_position,
                            "Direction": direction_orientation,
                            "Image Size": size,
                            "Physical size of each pixel": spacing,
                            "Distance between consecutive slices (mm)": spacing[2]
                        }

                # Append the image data to the patient’s images
                dataset_structure[patient_id]["Images"].append(image_data)

# Save the structured dataset to a JSON file
with open(output_json_file, "w") as outfile:
    json.dump(dataset_structure, outfile, indent=4)