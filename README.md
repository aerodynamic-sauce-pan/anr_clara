
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
