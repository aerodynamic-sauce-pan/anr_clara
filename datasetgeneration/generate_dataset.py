import sys, time
from unrealcv import client
from unrealcv.util import read_png, read_npy
import matplotlib.pyplot as plt
import cv2

def capture_depth():
    res = client.request('vget /camera/{id}/depth npy'.format(id = 0))
    depth = read_npy(res)
    depth[depth>255] = 255
    return depth

def capture_img():
    res = client.request('vget /camera/{id}/lit png'.format(id = 0))
    img = read_png(res)
    return img

def get_ss_gt():
    import numpy as np, os   
    for filename in os.listdir('../TrainImages/IS2'):
        if filename[-4:] == '.png':
            img = cv2.imread('../TrainImages/IS2/' + filename)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            ss_label = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
            ss_mask = np.zeros(img.shape, dtype=np.uint8)
            ss_label[(img[:,:,0]==0) & (img[:,:,1]==0) & (img[:,:,2]==0)] = 0 
            ss_label[(img[:,:,0]==12) & (img[:,:,1]==243) & (img[:,:,2]==12)] = 1
            ss_label[(img[:,:,0]==33) & (img[:,:,1]==38) & (img[:,:,2]==108)] = 2
            ss_label[(img[:,:,0]%16==15) & (img[:,:,1]%16==15)] = 3      
            ss_mask[(img[:,:,0]==0) & (img[:,:,1]==0) & (img[:,:,2]==0)] = [0,0,255] 
            ss_mask[(img[:,:,0]==12) & (img[:,:,1]==243) & (img[:,:,2]==12)] = [255,128,0]
            ss_mask[(img[:,:,0]==33) & (img[:,:,1]==38) & (img[:,:,2]==108)] = [0,255,0]
            ss_mask[(img[:,:,0]%16==15) & (img[:,:,1]%16==15)] = [192,64,64]
              
            assert(np.sum((ss_mask[:,:,0]==0) & (ss_mask[:,:,1]==0) & (ss_mask[:,:,2]==0)) == 0)
            cv2.imwrite('../TrainImages/SS2/label_{0}'.format(filename), ss_label)
            plt.imsave('../TrainImages/SS2/mask_{0}'.format(filename), ss_mask)
            print('The image label_%s is saved' %(filename))
            print('The image mask_%s is saved' %(filename))
'''    
client.connect()
if not client.isconnected():
    print('UnrealCV server is not running. Run the game downloaded from http://unrealcv.github.io first.')
    sys.exit(-1)
   
f = open("trajectory.txt")
RGB = False
num = 0 
line = f.readline()  
while line:  
    num += 1
    print(line)
    pose = line.split(" ")
    client.request('vset /camera/0/pose {0[0]} {0[1]} {0[2]} {0[3]} {0[4]} {0[5]}'.format(pose))
    time.sleep(3)
    img = capture_img()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    save_dir = 'RGB2' if RGB == True else 'IS2'
    #plt.imsave('../TrainImages/{0}/{1}.png'.format(save_dir, num), img)
    cv2.imwrite('../TrainImages/{0}/{1}.png'.format(save_dir, num), img)
    print('The image %d is saved' %(num))
    #depth = capture_depth()
    #plt.imsave('../TrainImages/Depth2/{0}.png'.format(num), depth, cmap = 'gray')
    #print('The depth %d is saved' %(num))
    line = f.readline()  
f.close()
'''
get_ss_gt()