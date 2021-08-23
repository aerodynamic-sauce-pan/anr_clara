# EQUI_AIRSIM

## Python ENV
Python env desribed in:  _airsim_env.yml_

## Create the LUT
To create the LookUpTable CubemapImage Wcube x Wcube to EquiImage Wcube x (Wcube/2):

`import dep_to_equi_v3 as d2e`

`d2e.create_lookup_table(Wcube, save_dir)`

## Capture Images
To run the dataset_capture:

`python capture_dataset_8.py -s CAPTURES -p 1000 500 -m multi_cam --view 0`

