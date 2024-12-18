import json
from pathlib import Path
import SimpleITK as sitk
import argparse

def generate_json_file(pelvis_folder: str):
    """
    Generate a json file from dataset metadata.

    Args:
        pelvis_folder (str): directory containing each patient's images.
    """
    folder = Path(pelvis_folder)
    output_json_file = "Task1_pelvis_structure.json"

    # Prepare an empty dictionary to store the structured data
    dataset_structure = {}

    # Loop through each patient folder in the main directory
    for data_folder in folder.iterdir():
        #print(f"Processing folder: {data_folder.stem}") # - Processing folder: .git (for the first data_folder)
        if data_folder.is_dir() and data_folder.name != "overview" and not data_folder.stem.startswith("."):
            # Extract patient ID from the folder name (last three characters)
            patient_id = data_folder.stem[-3:]
            center = data_folder.stem[2]
            unique_key = f"{center}_{patient_id}"

            dataset_structure[unique_key] = {"Center": center, "PatientID": patient_id, "Images": []}

            image_paths = filter(lambda f: str(f).endswith("ct.nii.gz") or str(f).endswith("mr.nii.gz"), data_folder.iterdir())

            for image_path in image_paths:
                    # Read the image
                    itk_image = sitk.ReadImage(str(image_path))

                    # Get image metadata
                    origin_position = itk_image.GetOrigin()
                    direction_orientation = itk_image.GetDirection()
                    spacing = itk_image.GetSpacing()
                    size = itk_image.GetSize()
                    modality = "CT" if "ct" in image_path.stem.lower() else "MRI"

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
                    dataset_structure[unique_key]["Images"].append(image_data)

    # Save the structured dataset to a JSON file
    with open(output_json_file, "w") as outfile:
        json.dump(dataset_structure, outfile, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Generate a JSON file with structured dataset.')
    parser.add_argument('--input_path',type=str, help='Directory containing each patients folder.')
    args = parser.parse_args()

    # Run the JSON generation function
    generate_json_file(args.input_path) 

if __name__ == "__main__":
    main()

# to run it:
#python generate_json.py --input_path /folder/of/pelvis