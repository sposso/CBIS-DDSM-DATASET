import os 
import shutil
import pandas as pd 
import pydicom as dicom





def mam_data(img_root, csv_root):
    
    
    """
    This function retrieves the path of all mammograms (3103) in the CBIS-DDSM.
    You need to import the original csv files from 
    "https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=22516629".
    This  function outputs 4 CSV files. Each CSV file includes the following columns:
    
    img id. Corresponds to the folder name where the mask is located. 
    img_path: Image path on your local machine.
    label: Image pathology (Benign or Malignant). BENIGN-WITHOUT-CALLBACK is replaced with Benign. 
    
    Parameters:
    img_root (str): Path of directory that contains mammograms.
    csv_root (str): Path of directory that contains the original CSV files.
    Returns:
    None: The function saves the CSV files in the specified output path.
    
    """
   
    # Create a temporal folder to save the CSV files
    csv_output_path = os.path.join(os.getcwd(), 'temp_mammograms_csv')
    os.makedirs(csv_output_path, exist_ok=True)  # Create the directory if it does not exist
    # Check if the img_root and csv_root directories exist
    # List all folders in the img_root directory
    folders = os.listdir(img_root)
    cases_dict = dict()  # save image id and path
    
    
    for f in folders:
        if f.endswith('_CC') or f.endswith('_MLO'):  # filter out the cropped images
            path = list()

            for root, dirs, files in os.walk(img_root + '/' + f):  # retrieve the path of image
                for d in dirs:
                    path.append(d)
                for filename in files:
                    path.append(filename)

            img_path = os.path.join(img_root, f, *path)  # generate image path
            cases_dict[f] = img_path
            
    df = pd.DataFrame(list(cases_dict.items()), columns=['img', 'img_path']) 
    
    type_dict = {'Calc-Test': 'calc_case_description_test_set.csv',
                 'Calc-Training': 'calc_case_description_train_set.csv',
                 'Mass-Test': 'mass_case_description_test_set.csv',
                 'Mass-Training': 'mass_case_description_train_set.csv'}

    for t in type_dict.keys():  # handle images based on the type
            df_subset = df[df['img'].str.startswith(t)]

            df_csv = pd.read_csv(csv_root + '/' + type_dict[t],
                                 usecols=['pathology', 'image file path'])  # read original csv file
            df_csv['img'] = df_csv.apply(lambda row: row['image file path'].split('/')[0],
                                         axis=1)  # extract image id from the path
            df_csv['pathology'] = df_csv.apply(
                lambda row: 'BENIGN' if row['pathology'] == 'BENIGN_WITHOUT_CALLBACK' else row['pathology'],
                axis=1)  # replace pathology 'BENIGN_WITHOUT_CALLBACK' to 'BENIGN'

            df_csv = df_csv.drop_duplicates(subset=["img"]) # Remove duplicate mammograms (orginal csv files assign mammograms with multi abnoramlities to different masks)

            df_subset_new = pd.merge(df_subset, df_csv, how='inner',
                                     on='img') #merge images path and pathology on img id. 


            df_subset_new = df_subset_new.drop(columns=["image file path"])
            df_subset_new.to_csv(os.path.join(csv_output_path, t.lower() + '.csv'),
                                 index=False)  # output merged dataframe in csv format
                               # output merged dataframe in csv format

            print(t)
            print('data_cnt: %d' % len(df_subset_new))
            
    print('Finished retrieval of mammogram paths!')
    
    return csv_output_path  # Return the path where the CSV files are saved
    
    
    
def mask_data(img_root, csv_root):
    
    """
    This function retrieves the path of all masks (3568 masks) in the CBIS-DDSM.
    You need to import the original csv files from 
    "https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=22516629".
    
    This  function outputs 4 csv files.Each csv file include the following columns:
    img id. Corresponds to the folder name where the mask is located. 
    img_path: Image path on your local machine.
    label: Image pathology (Benign or Malignant). BENIGN-WHITOUT-CALLBACK is replaced to Benign. 
    
    Parameters:
    img_root (str): Path of directory that contains mammograms.
    csv_root (str): Path of directory that contains the original CSV files. 
    Returns:
    None: The function saves the CSV files in the specified output path.
    3568 masks are retrieved from the CBIS-DDSM dataset.
    3103 mammograms are retrieved from the CBIS-DDSM dataset.
   
    
    """
    
    # Create a temporal folder to save the CSV files
    csv_output_path = os.path.join(os.getcwd(), 'temp_masks_csv')
    # Create the directory if it does not exist
    
    os.makedirs(csv_output_path, exist_ok=True)  # Create the directory if it does not exist
 
    #Folder where you want to save the new csv files that will contain the  local paths of the masks
    folders = os.listdir(img_root)
    cases_dict = dict()  # save image id and path
    count =0
    for f in folders:
        if f[-1].isdigit():
            path =list()#get mask 
            for roots, dirs, files in os.walk(img_root + "/"+f):
                if len(dirs)>1: #cropped images and masks are stored in a different directory .
                    for i in dirs:
                        for root,dirs,file in os.walk(img_root + "/"+f+"/"+i):
                            for final in dirs:
                                if final.startswith("1.000000-ROI"):

                                    path.append(final)
                                    path.append('1-1.dcm')

                                    img_path = root + '/' + '/'.join(path)  # generate image path

                                    cases_dict[f] = img_path


                else: #cropped images and masks are stored in a single directory . 

                    for d in dirs:
                        path.append(d)                    
                    for filenames in files:
                        if filenames.endswith('2.dcm'): #There is no consistent mask naming convention. 
                            path.append(filenames)

                            img_path = img_root + '/' + f + '/' + '/'.join(path)  # generate image path

                            img = dicom.dcmread(img_path).pixel_array
                            if img.dtype == 'uint16':

                                img_path = img_path[:-5]+"1.dcm" #There is no consistent mask naming convention
                                cases_dict[f] = img_path

                            else:
                                cases_dict[f] = img_path
                            
    df = pd.DataFrame(list(cases_dict.items()), columns=['img', 'roi_path']) #dictionary is converted to dataframe
    #original csv files 
    type_dict = {'Calc-Test': 'calc_case_description_test_set.csv',
                 'Calc-Training': 'calc_case_description_train_set.csv',
                 'Mass-Test': 'mass_case_description_test_set.csv',
                 'Mass-Training': 'mass_case_description_train_set.csv'}


    
    for t in type_dict.keys():  # handle images based on the type
            df_subset = df[df['img'].str.startswith(t)]

            df_csv = pd.read_csv(csv_root + '/' + type_dict[t],
                                 usecols=['pathology', 'ROI mask file path'])  # read original csv file
            df_csv['img'] = df_csv.apply(lambda row: row['ROI mask file path'].split('/')[0],
                                         axis=1)  # extract image id from the path
            df_csv['pathology'] = df_csv.apply(
                lambda row: 'BENIGN' if row['pathology'] == 'BENIGN_WITHOUT_CALLBACK' else row['pathology'],
                axis=1)  # replace pathology 'BENIGN_WITHOUT_CALLBACK' to 'BENIGN'

            df_subset_new = pd.merge(df_subset, df_csv, how='inner',
                                     on='img') # Merge image path and pathology in img id. 
            df_subset_new = df_subset_new.drop(columns=["ROI mask file path"]) #Drop original file path 

            df_subset_new.to_csv(csv_output_path + '/' + t.lower() + '.csv',
                                 index=False)  # output merged dataframe in csv format

            print(t)
            print('data_cnt: %d' % len(df_subset_new))
        
    print('Finished retrieval of mask paths!')
    
    return csv_output_path  # Return the path where the CSV files are saved
    
    
def final_dataset(csv_mask_path, csv_mam_path, output_path, delete_temp_csv=True):
    
    """
    This function merges the mammograms and masks dataframes based on the image id.
    It outputs two CSV files: one for the training set and one for the test set.
    Each CSV file includes the following columns:
    img_path: Image path on your local machine.
    roi_path: Mask path on your local machine.
    label: Image pathology  -> 1 for calc Malignant, 2 for calc Benign.
                               3 for mass Malignant, 4 for mass Benign.    
    
    Parameters:
    csv_mask_path (str): Path of directory that contains the CSV files for masks.
    csv_mam_path (str): Path of directory that contains the CSV files for mammograms.
    output_path (str): Folder where you want to save the final merged CSV files.
    Returns:
    None: The function saves the final merged CSV files in the specified output path.
    
    """
    
    
    
    # official split
    sets = ['training', 'test']
    
    #types of lesions
    types = ['calc', 'mass']
    
    
    for s in sets:
        
        final_dfs = {'mam_set': [], 'mask_set': []}
    
        for t in types:
            df_mask = pd.read_csv(csv_mask_path + '/' + t + '-' + s + '.csv')
            df_mam = pd.read_csv(csv_mam_path + '/' + t + '-' + s + '.csv')
            
            if t == 'calc':
                # Map malignant to 1 and benign to 2 in the label column
                df_mask['label'] = df_mask['pathology'].map({'MALIGNANT': 1, 'BENIGN': 2})
                df_mam['label'] = df_mam['pathology'].map({'MALIGNANT': 1, 'BENIGN': 2})
                
                final_dfs['mask_set'].append(df_mask)
                final_dfs['mam_set'].append(df_mam)
            elif t == 'mass':
                df_mask['label'] = df_mask['pathology'].map({'MALIGNANT': 3, 'BENIGN': 4})
                df_mam['label'] = df_mam['pathology'].map({'MALIGNANT': 3, 'BENIGN': 4})
                
                final_dfs['mask_set'].append(df_mask)
                final_dfs['mam_set'].append(df_mam)
                
        # Concatenate all dataframes for masks and mammograms
        final_mask_df = pd.concat(final_dfs['mask_set'], ignore_index=True)
        final_mask_df = final_mask_df.drop(columns=['pathology'], errors='ignore') 
        final_mam_df = pd.concat(final_dfs['mam_set'], ignore_index=True)
        final_mam_df = final_mam_df.drop(columns=['pathology'], errors='ignore') 
        print(f"Number of masks in {s} set: {len(final_mask_df)}")
        print(f"Number of mammograms in {s} set: {len(final_mam_df)}")

        # We will use the name of the images as the merge criteria  to merge the mask and mammogram dataframes.
        
        final_mam_df = final_mam_df.rename(columns={'img': 'merge_key', 'label': 'label_mam'})
        
        # Generate a new column 'merge' in the mask dataframe with the original names of mammograms.
        
        final_mask_df['merge_key'] = final_mask_df.apply(lambda row: row['img'][:-2], axis=1)
        
        # Merge the mammogram and mask dataframes on the 'merge' column.
        
        merged_df = pd.merge(final_mam_df, final_mask_df, on='merge_key', how='inner')
        
        # Drop columns that are either redundant or were only used for merging and are not needed in the final output
        merged_df = merged_df.drop(columns=['img', 'merge_key', 'label_mam'])

        
        # Save the final merged dataframe to a CSV file
        
        merged_df.to_csv(os.path.join(output_path, f"{s}_dataset.csv"), index=False)
        
        #delete the temporary csv folders (csv_mask_path and csv_mam_path)
        # delete all the folder
        
    if delete_temp_csv:
        
        if os.path.exists(csv_mask_path):
            shutil.rmtree(csv_mask_path)
        if os.path.exists(csv_mam_path):
            shutil.rmtree(csv_mam_path)
            
    
    print('Training and test datasets saved as training_dataset.csv and test_dataset.csv in the current working directory!')
        
        
        
        
    
                
        
                
            
                
            
                
            
                
                
                
        
