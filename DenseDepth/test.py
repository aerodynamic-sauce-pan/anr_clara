"""Test module for the DenseNet model.

This module is used to run depth maps predictions on test images, using the
trained DenseNet model. Input images should have the same ratio of 1:3,
similar to 640x480.
"""

import os
import argparse
import cv2
from tqdm import tqdm
from matplotlib import pyplot as plt

# Keras / TensorFlow
from keras.models import load_model
from layers import BilinearUpSampling2D
from utils import predict, load_images  # display_images
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'


# Argument Parser
parser = argparse.ArgumentParser(description='High Quality Monocular Depth'
                                             'Estimation via Transfer Learning')
parser.add_argument('--model',
                    default='models/1589218727-n53-e20-bs4-lr0.0001'
                            '-densedepth_nyu/weights.20-12.08.hdf5',
                    type=str,
                    help='Trained Keras model file.')
parser.add_argument('--input',
                    default='../TestImages/synthetic/RGB/*.png',
                    nargs='*',
                    type=str,
                    help='Input filename or folder.')
parser.add_argument('--output',
                    default='../TestImages/synthetic/RGB/'
                            'DenseNet_maps_synthetic',
                    type=str,
                    nargs='?',
                    help='Output folder.')
parser.add_argument('-v', '--verbose',
                    action='store',
                    nargs='*',
                    help='If true, display the depth maps for each image.')

args = parser.parse_args()
verbose = args.verbose is not None
out_dir = args.output

# Custom object needed for inference and training
custom_objects = {'BilinearUpSampling2D': BilinearUpSampling2D,
                  'depth_loss_function': None}

# Load model into GPU / CPU
print('Loading model...')
model = load_model(args.model, custom_objects=custom_objects, compile=False)
print('\nModel loaded ({0}).'.format(args.model))
if verbose:
    model.summary()

# Input images
print('Loading images...')
inputs = load_images(args.input)
inputs = inputs[:, :, :, 0:3]
# inputs = cv2.resize(inputs,(480,640))
print('\nLoaded ({0}) images of size {1}.'.format(inputs.shape[0],
                                                  inputs.shape[1:]))

# Compute results
print('Computing predictions...')
outputs = predict(model, inputs, 0, 255)
if verbose:
    print('Predictions size : ', outputs.shape)

# Display results
# matplotlib problem on ubuntu terminal fix : matplotlib.use('TkAgg')
print('Saving results...')
for i in tqdm(range(inputs.shape[0])):
    if outputs[i, :, :, :].shape != (1024, 512):
        output = cv2.resize(outputs[i, :, :, :], (1024, 512),
                            interpolation=cv2.INTER_CUBIC)
        # output = resize(outputs[i, :, :, :], inputs.shape[1:],
        #                 preserve_range=True, mode='reflect',
        #                 anti_aliasing=True)
    plt.figure(figsize=(24,24))
    plt.axis('off')
    plt.imshow(output, cmap='gray')
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    plt.savefig('{0}/{1}.png'.format(out_dir, i+1), bbox_inches='tight',
                dpi=100, pad_inches=0.0)
    if verbose:
        plt.show()
