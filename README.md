# CBIS-DDSM-DATASET
Suppose you want to train a breast cancer classifier or a segmentation model using the CBIS-DDSM dataset. In that case, this repository may help you to easily extract the mammograms and the masks from the original folder.

## 🔧 Setup Instructions

### 1. Download the Dataset

You can download the dataset directly from the [official TCIA page](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=22516629).

#### a. Install the NBIA Data Retriever

To download the dataset, you’ll need the **NBIA Data Retriever**, a tool provided by TCIA:

- [Click here to download NBIA Data Retriever](https://wiki.cancerimagingarchive.net/display/NBIA/Version+4.4.3)

#### b. Ubuntu Linux Installation Guide

As an Ubuntu Linux user, here’s a step-by-step guide to installing the NBIA Data Retriever and then the dataset:

1. [Download the `.deb` installer](https://github.com/CBIIT/NBIA-TCIA/releases/download/DR-4_4_3-TCIA-20240916-1/nbia-data-retriever_4.4.3-1_amd64.deb) to your computer.

2. Open a terminal, navigate to the directory that contains the .deb installer, and run the following command:

   ```bash
   sudo dpkg -i nbia-data-retriever_4.4.3-1_amd64.deb

    ``` 

   💡  Take into account that you should replace _nbia-data-retriever_4.4.3-1_amd64.deb_ by the actual name of the installer you downloaded before.

3. [Download the `.tcia` file](https://www.cancerimagingarchive.net/wp-content/uploads/CBIS-DDSM-All-doiJNLP-zzWs5zfZ.tcia) that contains the mammograms to your computer.
4. Open the terminal and navigate to the directory that contains the .tcia file, and run the following command:

5.  ```bash
   
    /opt/nbia-data-retriever/bin/nbia-data-retriever --cli CBIS-DDSM-All-doiJNLP-zzWs5zfZ.tcia

    ```
      📁 This command will begin downloading the dataset into folders containing the mammogram images and masks. If your .tcia file has a different name, update the command accordingly.

### Additional information 
To go into detail about the CBIS-DDSM dataset, you can check this [paper](https://www.nature.com/articles/sdata2017177). It describes how to use the dataset and how the dataset was built. 

## 📊 Quantitative Description

Despite the [paper](https://www.nature.com/articles/sdata2017177) stating that CBIDS-DDSM has 753 calcification cases and 891 mass cases, it is difficult to determine how many images this dataset has. According to the metadata provided in the CSV files, CBIS-DDSM contains 3103 mammograms, 465 of which have more than one abnormality. 2.458 (79.21%) of the mammograms belong to the training set, and 645 (20.79% ) belong to the test set. Furthermore, the dataset includes 3,568 cropped mammograms along with their corresponding masks, which provide pixel-level annotations of abnormalities as identified by a radiologist.

# Repository Function Overview

### `main_retrieval.py`

This script generates two CSV files: `training_dataset.csv` and `test_dataset.csv`. The data split follows the official partition provided by the dataset's authors.

Each CSV file contains three columns:
1. **Mammogram Path**: The local file path (path on your machine) to each mammogram image.
2. **Mask Path**: The local file path of each annotation mask. Each mask is matched to its respective mammogram.
3. **Label** : The classification label for each mammogram, defined as:
   - `1` – Malignant Calcification  
   - `2` – Benign Calcification  
   - `3` – Malignant Mass  
   - `4` – Benign Mass

### `retrieval_utils.py`
This script contains three functions: 
   - **mam_data**: This function retrieves the path of all mammograms (3103) in your local machine.
   - **mask_data**: This function retrieves the path of all masks (3568) in your local machine.
   - **final_dataset**: This function merges the mammograms and masks dataframes based on the image id. It outputs two CSV files: one for the training set and one for the test set.
    
### `convert_dicom.ipynb`:
The  images provided by CBIS-DDSM  (mammograms, masks, and crops of abnormalities)  are saved in DICOM format. This function saves a 16-bit mammogram from DICOM as a rescaled 16-bit PNG file.


### 🎁 Bonus
In this [repository](https://github.com/sposso/Deep_learning_to_improve_breast_Cancer_pytorch), I implemented the deep learning classifier introduced in the [paper](https://www.nature.com/articles/s41598-019-48995-4) "Deep Learning to Improve Breast Cancer Detection on Screening Mammography" using PyTorch and CBIS-DDSM dataset.  The original code and model are available [here](https://github.com/lishen/end2end-all-conv). However, this  code is in Keras.  
My PyTorch version aims to be more readable and beginner-friendly, especially for researchers and students working on medical deep learning applications.

