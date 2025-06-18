
from retrieval_utils import mam_data,mask_data, final_dataset
import os

#directory that contains the  orginal dataset

img_root = '/home/sposso22/work/shared_data/breast_cancer/RAW_CBIS-DDSM'

# Create and save all 4 CSV files  (metadata) from the website  in a different folder
# This folder must contain the following files:
    # calc_case_description_test_set.csv, 
    # calc_case_description_train_set.csv
    # mass_case_description_train_set.csv
    # mass_case_description_test_set.csv

csv_root = '/home/sposso22/work/shared_data/breast_cancer/metadata_RAW_CBIS_DDSM'

mask_info = mam_data(img_root, csv_root)

mammo_info = mask_data(img_root, csv_root)


# The final training and test dataset will be saved in the current working directory
output_path = os.getcwd()

final_dataset(mask_info, mammo_info, output_path)


