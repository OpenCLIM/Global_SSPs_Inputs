# Global_SSPs_Inputs
The first model in the workflow designed to crop global ssp datasets to a specific country. This model takes all of the user parameter and dataset inputs and formats them ready to be used by the subsequent models. This data is then propogated through the model, reducing user input. 

## Description
All data/ choices made by the user are inputted at this stage of the model to reduce user error.  This process simplifies the user input methods.

## Input Parameters
*Country
  * Description: The country of interest.
*SSP
  * Description: The socio-economic pathway of interest.
*Administation Level
  * Description: Countries are often divided into administration zones at regional, national and district levels. In most administration datasets, a numerical value is given to the level. This parameter is recorded in the metadata file so that all people looking at the data know which administration region was used.
*LAD_Name
  * Description: Future models need to know the name of the column from the dataset of Local Authority polygons which contains the name of each LAD.
*LAD_Code
  * Description: Future models need to know the name of the column from the dataset of Local Authority polygons which contains the code of each LAD.


## Input Files (data slots)
* Boundary File
  * Description: A .gpkg file containing the boundary of the country of interest.
  * Location: /data/inputs/boundary
* SSP Data Sets
  * Description: Zip files of the global datasets for each SSP.
  * Location: /data/inputs/ssps
* Local Authority Districts
  * Description: A .gpkg file containing the boundarys for each Local Authority District.
  * Location: /data/inputs/lads

## Outputs
* Boundary File
  * Description: A .gpkg file containing the boundary of the country of interest.
  * Location: /data/outputs/boundary
* SSP Data Sets
  * Description: Only the zip file for the selected ssp scneario is added to this folder.
  * Location: /data/outputs/ssp
* Local Authority Districts
  * Description: A .gpkg file containing the boundarys for each Local Authority District.
  * Location: /data/outputs/lads
* Parameters
  * Description: All parameters and their values are stored in a csv file.
  * Location: /data/outputs/parameters
