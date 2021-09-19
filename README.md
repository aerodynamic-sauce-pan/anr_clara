# General
This repository is the result of a master intership I carried out at the MIS laboratory of Amiens, France on the CLARA ANR project, under the supervision of Pascal VASSEUR. The purpose of this work is to provide new innovative tools for tree mapping in forest environnement based on 360° images taken from an UAV (Unmaned Autonomous Vehicle, a.k.a. drone). For more details about the project, our technical solutions and members involed in the project, see my internship report located at "Suivi_projet/Theo_2021/Rapport/Larcher_Theo_INSA.pdf". Several modules have been developped or enhanced based on previous work and are listed hereafter.

# Deep Learning models
Due to their large size, some models (AdapNet++, DenseDepth) have been saved and uploaded as archives under the Release "Deep Learning models Sept 2021".

## darknet-master
*DarkNet* is an open source neural network used for object detection, and backbone of the *YOLO* networks. The executable file for detection, `darknet.exe`, in located in `darknet-master\build\darknet\x64`. You should run it from console. 
- The network's weights trained on real forest images is located in `darknet-master\build\darknet\x64\backup`.
- The network's weights trained on the synthetic dataset locates in `darknet-master\build\darknet\x64\backup2`.

## DenseDepth
*DenseDepth* is a depth estimation network based on keras. The model has been trained on perspective synthetic images located in `TrainImages` (other than `SS_redwood`). The trained model has been saved and uploaded in Releases as an archive.

## AdapNet-pp
*AdapNet* is a semantic segmentation network based on Tensorflow which uses *ResNet50* as backbone. The trained model has been saved and uploaded in Releases as an archive. *AdapNet* is easily trainable on a single 12GB memory GPU card and has a fast inference time.

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
