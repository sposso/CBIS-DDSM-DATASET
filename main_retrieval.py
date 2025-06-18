
from retrieval_utils import mam_data,mask_data, final_dataset
import os
import pandas as pd

#directory that contains the  orginal dataset

img_root = '/home/sposso22/work/shared_data/breast_cancer/RAW_CBIS-DDSM'

# Create and save all 4 CSV files  (metadata) from the website  in a different folder
# This folder must contain the following files:
    # calc_case_description_test_set.csv, 
    # calc_case_description_train_set.csv
    # mass_case_description_train_set.csv
    # mass_case_description_test_set.csv

csv_root = '/home/sposso22/work/shared_data/breast_cancer/metadata_RAW_CBIS_DDSM'

csv_mam_path = mam_data(img_root, csv_root)

csv_mask_path = mask_data(img_root, csv_root)

output_path = os.path.join(os.getcwd(), 'final_datasets')
if not os.path.exists(output_path):
    os.makedirs(output_path)


# Create the final dataset by merging the mask and mammogram dataframes
final_dataset(csv_mask_path, csv_mam_path, output_path)
    
    


# %%
