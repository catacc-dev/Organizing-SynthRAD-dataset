import os
import nibabel as nib
import matplotlib.pyplot as plt

data_path = './1PA001/'
type_nifti = os.path.join(data_path, 'ct.nii.gz')
#type_nifti = os.path.join(data_path, 'mr.nii.gz')
nifti_img = nib.load(type_nifti)
nii_data = nifti_img.get_fdata()
nii_aff  = nifti_img.affine
nii_hdr  = nifti_img.header
print(f'Position information: \n {nii_hdr.get_best_affine()}\n')
#print(nii_aff ,'\n',nii_hdr)
print(nii_data.shape) # 3D matrix (565, 338, 146) - 146 slices with dimension 565x338

if(len(nii_data.shape)==3):
   for slice_Number in range(nii_data.shape[2]):
       plt.imshow(nii_data[:,:,slice_Number ])
       plt.show()
if(len(nii_data.shape)==4):
   for frame in range(nii_data.shape[3]):
       for slice_Number in range(nii_data.shape[2]):
           plt.imshow(nii_data[:,:,slice_Number,frame])
           plt.show()