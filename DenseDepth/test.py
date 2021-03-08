import os
import glob
import argparse
import matplotlib
import cv2
import skimage
from skimage.transform import resize
# Keras / TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'
from keras.models import load_model
from layers import BilinearUpSampling2D
from utils import predict, load_images, display_images
from matplotlib import pyplot as plt

# Argument Parser
parser = argparse.ArgumentParser(description='High Quality Monocular Depth Estimation via Transfer Learning')
parser.add_argument('--model', default='models/1589218727-n53-e20-bs4-lr0.0001-densedepth_nyu/weights.20-12.08.hdf5', type=str, help='Trained Keras model file.')
parser.add_argument('--input', default='..\TestImages\synthetic\RGB\*.png', type=str, help='Input filename or folder.')
#parser.add_argument('--input', default='E:/UE_4.16/Engine/Binaries/Win64/4.jpg', type=str, help='Input filename or folder.')
args = parser.parse_args()

# Custom object needed for inference and training
custom_objects = {'BilinearUpSampling2D': BilinearUpSampling2D, 'depth_loss_function': None}

print('Loading model...')

# Load model into GPU / CPU
model = load_model(args.model, custom_objects=custom_objects, compile=False)

print('\nModel loaded ({0}).'.format(args.model))

# Input images
inputs = load_images( glob.glob(args.input) )
inputs = inputs[:,:,:,0:3]
#inputs = cv2.resize(inputs,(480,640))
print('\nLoaded ({0}) images of size {1}.'.format(inputs.shape[0], inputs.shape[1:]))

# Compute results
outputs = predict(model, inputs, 0, 255)
print(outputs.shape)

#matplotlib problem on ubuntu terminal fix
#matplotlib.use('TkAgg')   

# Display results

for i in range(inputs.shape[0]):
    print(i)
    '''
    viz = display_images(outputs[i,:,:,:].copy(), inputs[i,:,:,:].copy())
    plt.figure(figsize=(10,5))
    plt.imshow(viz)
    #plt.savefig('images/test_synthetic/test{0}.png'.format(i+1))
    plt.savefig('images/test.png')
    plt.show()
    '''
    output = cv2.resize(outputs[i,:,:,:],(640,480),interpolation=cv2.INTER_CUBIC)
    #output = resize(outputs[i,:,:,:], inputs.shape[1:], preserve_range=True, mode='reflect', anti_aliasing=True )
    plt.figure(figsize=(4.8*480/279,6.4*480/279)) 
    plt.imshow(output,cmap='gray')   
    plt.axis('off') 
    plt.savefig('images/test_synthetic/{0}.png'.format(i+1),bbox_inches='tight',dpi=100,pad_inches=0.0)
    plt.show()