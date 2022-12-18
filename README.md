# CBIS-DDSM-DATASET
If you want to train a breast cancer classifier or a segmentation model using the CBIS-DDSM  dataset, this repository may help you to easily extract the mammograms and the masks from the original folder.

## Setup
1. The dataset can be downloaded directly from the[official site](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=22516629).
2.  If you wat to go into details about the CBIS-DDSM dataset, you can check this [paper](https://www.nature.com/articles/sdata2017177). It describes how to use the dataset and how the dataset was built. 

## Quantitative Description

Despite of [paper](https://www.nature.com/articles/sdata2017177) states that CBIDS-DDSM has 753 calcification cases and 891 mass cases, it is difficult to determine how many images actually this dataset has. According to the metadeta provided in the CSV files, CBIS-DDSM contains 3103 mammograms,  and 465 have more than one abnormality. 2.458 mamograms (79.21%) belong to the training set, and 645 (20.79% ) belong to the test set. Furthermore, 3568 cropped mammograms and 3568 masks are included.

## A bit explanation of the respository´s functions
### Mammograms_code.ipynb:
This script contains a function that retrieves the path of all mammograms in your local machine and then merges each image path with its pathology in a dataframe. This dataframe is subsequently  saved as csv file. 
### mask_code.ipynb:
This script contains a function that retrieves the path of all patches in your local machine and then merges each mask path with its pathology in a dataframe. This dataframe is subsequently  saved as csv file. Note: There are more masks than mammograms since some mammograms have more than one lesion.

### convert_dicom.ipynb:
The  images provided by CBIS-DDSM  (mammograms, masks, crops of abnormalities)  are saved in DICOM format. This function saves 16-bit mammogram from dicom as rescaled 16-bit png file.


