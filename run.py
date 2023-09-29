import os
import glob
from glob import glob
import geopandas as gpd
import shutil
import math
from geojson import Polygon
from os.path import join, isdir, isfile
from datetime import datetime

### Using DAFNI we want to create output dataslots that include the name of the country chosen ###
### This code creates a metadata.json file which tells DAFNI what to name each output ###

def metadata_json(output_path, output_title, output_description, bbox, file_name):
    """
    Generate a metadata json file used to catalogue the outputs of the UDM model on DAFNI
    """

    # Create metadata file
    metadata = f"""{{
      "@context": ["metadata-v1"],
      "@type": "dcat:Dataset",
      "dct:language": "en",
      "dct:title": "{output_title}",
      "dct:description": "{output_description}",
      "dcat:keyword": [
        "UDM"
      ],
      "dct:subject": "Environment",
      "dct:license": {{
        "@type": "LicenseDocument",
        "@id": "https://creativecommons.org/licences/by/4.0/",
        "rdfs:label": null
      }},
      "dct:creator": [{{"@type": "foaf:Organization"}}],
      "dcat:contactPoint": {{
        "@type": "vcard:Organization",
        "vcard:fn": "DAFNI",
        "vcard:hasEmail": "support@dafni.ac.uk"
      }},
      "dct:created": "{datetime.now().isoformat()}Z",
      "dct:PeriodOfTime": {{
        "type": "dct:PeriodOfTime",
        "time:hasBeginning": null,
        "time:hasEnd": null
      }},
      "dafni_version_note": "created",
      "dct:spatial": {{
        "@type": "dct:Location",
        "rdfs:label": null
      }},
      "geojson": {bbox}
    }}
    """

    # write to file
    with open(join(output_path, '%s.json' % file_name), 'w') as f:
        f.write(metadata)
    return

### A couple of functions to calcualte round up and down the extents of the bounding box ###
### For the json file ###

def round_down(val, round_val):
    """Round a value down to the nearst value as set by the round val parameter"""
    return math.floor(val / round_val) * round_val

def round_up(val, round_val):
    """Round a value up to the nearst value as set by the round val parameter"""
    return math.ceil(val / round_val) * round_val

### Define the data paths for the input information and the required output folder ###
### The models are hard coded which means that the output datasets of one become ###
### the input data sets of the next. Therefore the folder structure is integral to the ###
### successful running of the models ###

# Set data paths
data_path = os.getenv('DATA','/data')

# Set up Data Input Paths
inputs_path = os.path.join(data_path, 'inputs')
ssps_path = os.path.join(inputs_path, 'ssps')
boundary_path = os.path.join(inputs_path, 'boundary')
lads_path = os.path.join(inputs_path,'lads')

# Set up and create data output paths for each of the datasets needed in the subqeuent models
outputs_path = os.path.join(data_path, 'outputs')
if not os.path.exists(outputs_path):
    os.mkdir(outputs_path)
boundary_outputs_path = os.path.join(outputs_path, 'boundary')
if not os.path.exists(boundary_outputs_path):
    os.mkdir(boundary_outputs_path)
ssp_outputs_path = os.path.join(outputs_path, 'ssp')
if not os.path.exists(ssp_outputs_path):
    os.mkdir(ssp_outputs_path)
lads_outputs_path = os.path.join(outputs_path, 'lads')
if not os.path.exists(lads_outputs_path):
    os.mkdir(lads_outputs_path)
parameter_outputs_path = os.path.join(outputs_path, 'parameters')
if not os.path.exists(parameter_outputs_path):
    os.mkdir(parameter_outputs_path)
meta_outputs_path = os.path.join(outputs_path, 'metadata')
if not os.path.exists(meta_outputs_path):
    os.mkdir(meta_outputs_path)


### The user must define a number of key variables which will carry through each model ###
### These dictate the chosen SSP scenario, the country of interest ###
### Administation regions vary from country to country, with different levels of administation ###
### Future models will pull the name of the LAD and the code for each LAD from the dataset and therefore ###
### it is important to copy the name of these exactly from the dataset column header, failure to do so will ###
### prevent future models from pulling the correct data from the dataset. ###

# Read environment variables
ssp = os.getenv('SSP')
country = os.getenv('COUNTRY')
level = os.getenv('LEVEL')
lad_name = os.getenv('LAD_NAME')
lad_code = os.getenv('LAD_CODE')

### To improve the user experience on DAFNI, all input files and details are added in this model. ###
### They are then moved to the correct output folder ###

# Locate the boundary file and move into the correct output folder
# Rename based on the location of the city of interest
boundary = glob(boundary_path + "/*.*", recursive = True)
src=boundary[0]
print('src:',src)
dst=os.path.join(boundary_outputs_path, country + '.gpkg')
print('dst:',dst)
shutil.copy(src,dst)

# Locate the lad file and move into the correct output folder
# Rename based on the location of the city of interest
lad = glob(lads_path + "/*.*", recursive = True)
src=lad[0]
print('src:',src)
dst=os.path.join(lads_outputs_path, country + '_LADS.gpkg')
print('dst:',dst)
shutil.copy(src,dst)

### This model will only consider one SSP at a time, but can be used as part of a looped workflow ###

# Identify which of the SSP datasets is needed and move into the correct output folder
# Retain the file name containing the SSP and year
ssps = glob(ssps_path + "/*.*",recursive = True)
print('ssp_data:',ssps)

filename=[]
filename=['xx' for n in range(len(ssps))]
print('filename:',filename)

# Create a list of all of the files in the folder
for i in range(0,len(ssps)):
    test = ssps[i]
    file_path = os.path.splitext(test)
    print('Filepath:',file_path)
    filename[i]=file_path[0].split("/")
    print('Filename:',filename[i])

file =[]

# Identify which file in the list relates to the chosen year / SSP
for i in range(0,len(ssps)):
    if ssp in filename[i][-1]:
        file = ssps[i]
        dst = os.path.join(ssp_outputs_path, filename[i][-1] + '.zip')

print('File:',file)

# Move that file into the correct folder.
src=file
print('src:',src)
print('dst:',dst)
shutil.copy(src,dst)

### For consistency and full transparency, the selected parameters are written in csv form ###
### This document will pass through each model ###

# Print all of the input parameters to an excel sheet to be read in later
with open(os.path.join(parameter_outputs_path,country + '-' + ssp + '-parameters.csv'), 'w') as f:
    f.write('PARAMETER,VALUE\n')
    f.write('COUNTRY,%s\n' %country)
    f.write('SSP,%s\n' %ssp)
    f.write('ADMIN_LEVEL,%s\n'%level)
    f.write('LAD_NAME,%s\n'%lad_name)
    f.write('LAD_CODE,%s\n'%lad_code)

### To create the bounding box for the .json file, the following code reads the country boundary ###

boundary_1 = glob(boundary_path + "/*.*", recursive = True)
boundary = gpd.read_file(boundary_1[0])
bbox = boundary.bounds
extents = 1000
left = round_down(bbox.minx,extents)
bottom = round_down(bbox.miny,extents)
right = round_down(bbox.maxx,extents)
top = round_down(bbox.maxy,extents)
geojson = Polygon([[(left,top), (right,top), (right,bottom), (left,bottom)]])
    
SSP=ssp.upper()

title_for_output = country + ' - ' + SSP

description_for_data_prep = 'This dataset contains three files detailing urban, rural and population change for ' + country + ' under the ' + ssp + ' scenario. Generated using the downscaled SSP datasets (https://www.nature.com/articles/s41597-021-01052-0) data is collated at the Local Authority level selected by the user.'
# write a metadata file so outputs properly recorded on DAFNI
metadata_json(output_path=meta_outputs_path, output_title=title_for_output, output_description=description_for_data_prep, bbox=geojson, file_name='metadata_ssp_data')