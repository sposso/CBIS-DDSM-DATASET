# CBIS-DDSM-DATASET
If you want to train a breast cancer classifier or a segmentation model using the CBIS-DDSM  dataset, this repository may help you to easily extract the mammograms and the masks from the original folder.

## Setup
1. The dataset can be downloaded directly from the [official site](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=22516629).
2.  If you want to go into detail about the CBIS-DDSM dataset, you can check this [paper](https://www.nature.com/articles/sdata2017177). It describes how to use the dataset and how the dataset was built. 

## Quantitative Description

Despite the [paper](https://www.nature.com/articles/sdata2017177) stating that CBIDS-DDSM has 753 calcification cases and 891 mass cases, it is difficult to determine how many images this dataset actually has. According to the metadata provided in the CSV files, CBIS-DDSM contains 3103 mammograms, 465 of which have more than one abnormality. 2.458 (79.21%) of the mamograms belong to the training set, and 645 (20.79% ) of them belong to the test set. Furthermore, 3568 cropped mammograms and 3568 masks are included.

## A bit of explanation of the repository's functions
### Mammograms_code.ipynb:
This script contains a function that retrieves the path of all mammograms on your local machine and merges each image path with its pathology in a data frame. The dataframe is subsequently saved as a CSV file. 
### mask_code.ipynb:
This script contains a function that retrieves the path of all patches in your local machine and then merges each mask path with its pathology in a data frame. This dataframe is subsequently  saved as CSV file. Note: There are more masks than mammograms since some mammograms have more than one lesion.

### convert_dicom.ipynb:
The  images provided by CBIS-DDSM  (mammograms, masks, and crops of abnormalities)  are saved in DICOM format. This function saves a 16-bit mammogram from DICOM as a rescaled 16-bit PNG file.

### Original_Split.ipynb:

This script creates the test and training set according to the standardized split given by the official [paper](https://www.nature.com/articles/sdata2017177). The path of all images is stored in a data frame, which is saved as a CSV file.

### Bonus :
In this [repository](https://github.com/sposso/Deep_learning_to_improve_breast_Cancer_pytorch), I implemented the deep learning classifier introduced in the [paper](https://www.nature.com/articles/s41598-019-48995-4) "Deep Learning to Improve Breast Cancer Detection on Screening Mammography" using PyTorch and CBIS-DDSM dataset.  The original code and model are available [here](https://github.com/lishen/end2end-all-conv). However, this  code is in Keras.  
My  main goal is to provide an understandable implementation of this model, which can be helpful for everyone, especially those who are beginning to work with deep learning and are interested in medical applications.

