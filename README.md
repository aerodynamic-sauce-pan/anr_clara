# General
This repository is the result of my work carried out during my master's internship at the MIS laboratory in Amiens, France as a contribution to the ANR project CLARA. Following previous work on deep learning models used for depth estimation and trees segmentation on RGB forest scenes, this repository contains a solution for 2D tree mapping based on RGB scenes and depth maps as well as a collection of useful scripts intended for image captures in Unreal Engine 4 and various data transformation. More details about the project can be found at `Suivi_projet/Theo_2021/` (french).

See latest development and documentation on the **sandbox branch**.

# Unreal Engine 4
The directory `equi_airsim` contains scripts used to create our databases from the UE4 Editor running the `RedwoodForest` environment.
- `augment_airsim_rec.py` : Interpolates values of raw airsim drone pose captures to augment them.
- `capture_dataset_8_tlarcher.py` : Scene capture script to run while the RedwoodForest simulation is running either through the UE4Editor or an independant package.
- `capture_dataset_8_tlarcher.py` : Module used by `capture_dataset_8_tlarcher.py` to perform geometric computations between perspective and equirectangular projections.
- `cluster_color.py` : Applying manual or k-means clustering on label data to correct bad segmentation.
- `tree_label_colors.py` : Small script that outputs an image containing unique colors used for the labels.


# Tree detection
## DarkNet
*DarkNet* is an open source neural network used for object detection, and backbone of the *YOLO* networks. The executable file for detection, `darknet.exe`, in located in `darknet-master\build\darknet\x64`. You should run it from console. 
- The network's weights trained on real forest images is located in `darknet-master\build\darknet\x64\backup`.
- The network's weights trained on the synthetic dataset locates in `darknet-master\build\darknet\x64\backup2`.

## DenseDepth
*DenseDepth* is a depth estimation network based on keras. The model used for training on the syhthetic dataset is uploaded in Releases. 
The test script file `test.py` is located in `DenseDepth-master`.

## AdapNet
*AdapNet* is a semantic segmentation network based on Tensorflow which uses *ResNet50* as backbone. The model used for training on the syhthetic dataset is uploaded in Releases
in the following directory : `init_checkpoint\synthia_rgb`. The test file `evaluate.py` is located in `AdapNet-pp-master/`. The test result is in `AdapNet-pp-master\images\test_synthetic`.
*AdapNet* is easily trainable on a single 12GB memory GPU card and has a fast inference time.

## Mapping
Contains the 2D tree mapping solution named 'bitterlich', inspired from the german tree density estimation method [Bitterlich Relaskop](https://www.youtube.com/watch?v=VggN0uWfEtQ). This solution uses Semantic segmentation images and depth maps of forest scenes to estimation the positions of tree relative to camera (drone).
- `tree_pos_to_csv.py` : Parses raw text data of trees in UE4 world Redwood Forest to a CSV file
- `bitterlich.py` : Localize trees around the drone for a given scene
- `bitterlich_batch.py` : Localize trees around the drone for a given directory of scenes
- `display_map.py` : Demonstration tool used for plotting a map of both estimated trees and their corresponding ground truth around a drone, in real time.
- `evaluate.py` : Computes several evaluation metrics of the estimated trees with respect to the corresponding ground truth.
- `gt_distance.py` : Extracts ground truth positions of trees from a source csv file (created with `tree_pos_to_csv.py`) and computes the ground truth distances.
- `geometry.py` : Collection of geometry related methods.



# Quality of code
## Linters
In order to guarantee quality of code approaching PEP8 and PEP257 requirements, popular linters (listed in the following sections) are used. To simplify their usage, a script named `checkMyCode.sh` and located in the project root folder has been created.

##### Configuration & usage
The available options for `checkMyCode.sh` are listed in its first `case in`. In a future version of the script, this help page could be included in it and made accessible via a `--help` argument.

The script runs the **linters** over any `.py` file located in the `src/` directory as well as all its sub-directories, and which name is different from `__init__.py`.

The script runs the **testers** over any `.py` file located in the `tests/` directory as well as all its sub-directories, and which name is different from `__init__.py`.

- Run all linters and testers:
```bash
./checkMyCode.sh all
```

- Run testers only :
```bash
./checkMyCode.sh t
```

- Run linters only :
```bash
./checkMyCode.sh [l]
```

- Run only linters or only testers on a specific file or directory (depending on its location) :
```bash
./checkMyCode.sh <FILE_OR_DIRECTORY>
```

## Linters
Linters are static code analysis tools used to flag programming errors, bugs, stylistic errors, and suspicious constructs. In doing so, they help to ensure the good quality of code. Furthemore, the 3 linters used in this project and listed in the following sections, help approaching the PEP8 and PEP257 norms with a few exceptions.

The following rules were ignored/modified/added so as to avoid excessive constraints :

- The max line length has been increased to 81
- The max complexity of Flake8 has been increased to 12 so as to match Pylint's default configuration
- The following Pydocstyle errors have been ignord : D107, D203, D204, D213, D407, D406, D413

#### Flake8
Flake8 is a python wrapper around PyFlakes, Pydocstyle and Ned Batchelder’s McCabe script, used to verify the code and pick up on styling deviations from the PEP8 norm, programatic errors (_e.g._ unused imports) and conduct complexity checks.

Flake8 is complementary to Pylint.

##### Configuration & usage
The Flake8 config file `tox.ini` is shared with other linters and is located at the project root directory.

- Run flake8 :
```bash
flake8 [<FILE_OR_DIRECTORY>]
```

#### Pylint
Pylint is a quality checker for Python picking up on styling deviations from the PEP8 norm, code duplication, bugs... It also suggests alternatives to the code structure.

##### Configuration & usage
The Pylint config file `pylintrc` is located at the project root directory.

- Run pylint :
```bash
pylint [<FILE_OR_DIRECTORY>]
```

#### Pydocstyle
Pydocstyle is a static analysis tool for checking compliance with Python docstring conventions. Pydocstyle supports most of PEP 257 out of the box, but it should not be considered a reference implementation.

##### Configuration & usage
The Pydocstyle config file `tox.ini` is shared with other linters and is located at the project root directory.

- Run pydocstyle :
```bash
pydocstyle [<FILE_OR_DIRECTORY>]
```
