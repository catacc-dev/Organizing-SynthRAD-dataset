import os
import nibabel as nib
import matplotlib.pyplot as plt
import argparse

# Task 1 - Pelvis P - Center A - PatientID 001
def load_nifti_images(patient_folder: str, modality: str='ct'):
    """
    Load and display slices of a NIfTI image.

    Args:
        patient_folder (str): Directory containing the patient NIfTI images.
        modality (str): Modality type, 'ct' for CT scan and 'mr' for MRI. Default is 'ct'.
    """
    nifti_file = os.path.join(patient_folder, f'{modality}.nii.gz')

    nifti_img = nib.load(nifti_file)
    nii_data = nifti_img.get_fdata()
    nii_aff  = nifti_img.affine
    nii_hdr  = nifti_img.header
    print("Affine Matrix:\n", nii_aff, '\n')
    print("Header:\n", nii_hdr)
    print("Data Shape:", nii_data.shape)

    if(len(nii_data.shape)==3):
        for slice_Number in range(nii_data.shape[2]):
            plt.imshow(nii_data[:,:,slice_Number])
            plt.show()

def main():
    parser = argparse.ArgumentParser(description='Visualize the slices of a NIfTI image.')
    parser.add_argument('--input_path', type=str, required=True, help='Directory containing the NIfTI images from the patient.')
    parser.add_argument('--modality', type=str, choices=['ct', 'mr'], default='ct', help="Type of NIfTI file to load: 'ct' or 'mr'. Default is 'ct'.")
    args = parser.parse_args()

    # Load and display the NIfTI images
    load_nifti_images(args.input_path, args.modality) 

if __name__ == "__main__":
    main()

# to run it:
#python load_nifti.py --input_path /folder/of/each/patient --modality ct