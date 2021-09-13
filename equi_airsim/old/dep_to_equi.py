

from PIL import Image    # Python Imaging Library
import math                # Maths functions
import sys                # Allows us to access function args
import os                # Allows us to split the text for saving the file
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
import parmap
import time

def unit3DToUnit2D(x,y,z,faceIndex):
    if(faceIndex=="X+"):
        x2D = y+0.5
        y2D = z+0.5
    elif(faceIndex=="Y+"):
        x2D = (x*-1)+0.5
        y2D = z+0.5
    elif(faceIndex=="X-"):
        x2D = (y*-1)+0.5
        y2D = z+0.5
    elif(faceIndex=="Y-"):
        x2D = x+0.5
        y2D = z+0.5
    elif(faceIndex=="Z+"):
        x2D = y+0.5
        y2D = (x*-1)+0.5
    else:
        x2D = y+0.5
        y2D = x+0.5

    # need to do this as image.getPixel takes pixels from the top left corner.

    y2D = 1-y2D

    return (x2D,y2D)

def projectX(theta,phi,sign):
    x = sign*0.5
    faceIndex = "X+" if sign==1 else "X-"
    rho = float(x)/(math.cos(theta)*math.sin(phi))
    y = rho*math.sin(theta)*math.sin(phi)
    z = rho*math.cos(phi)
    return (x,y,z,faceIndex)

def projectY(theta,phi,sign):
    y = sign*0.5
    faceIndex = "Y+" if sign==1 else "Y-"
    rho = float(y)/(math.sin(theta)*math.sin(phi))
    x = rho*math.cos(theta)*math.sin(phi)
    z = rho*math.cos(phi)
    return (x,y,z,faceIndex)

def projectZ(theta,phi,sign):
    z = sign*0.5
    faceIndex = "Z+" if sign==1 else "Z-"
    rho = float(z)/math.cos(phi)
    x = rho*math.cos(theta)*math.sin(phi)
    y = rho*math.sin(theta)*math.sin(phi)
    return (x,y,z,faceIndex)

def getColour(x,y,index,posx,negx,posy,negy,posz,negz):
    if(index=="X+"):
        return posx[y,x]
    elif(index=="X-"):
        return negx[y,x]
    elif(index=="Y+"):
        return posy[y,x]
    elif(index=="Y-"):
        return negy[y,x]
    elif(index=="Z+"):
        return posz[y,x]
    elif(index=="Z-"):
        return negz[y,x]


def convertEquirectUVtoUnit2D(theta,phi,squareLength):

    # calculate the unit vector

    x = math.cos(theta)*math.sin(phi)
    y = math.sin(theta)*math.sin(phi)
    z = math.cos(phi)

    # find the maximum value in the unit vector

    maximum = max(abs(x),abs(y),abs(z))
    xx = x/maximum
    yy = y/maximum
    zz = z/maximum

    # project ray to cube surface

    if(xx==1 or xx==-1):
        (x,y,z, faceIndex) = projectX(theta,phi,xx)
    elif(yy==1 or yy==-1):
        (x,y,z, faceIndex) = projectY(theta,phi,yy)
    else:
        (x,y,z, faceIndex) = projectZ(theta,phi,zz)

    (x,y) = unit3DToUnit2D(x,y,z,faceIndex)

    x*=squareLength
    y*=squareLength

    x = int(x)
    y = int(y)

    return {"index":faceIndex,"x":x,"y":y}

# 1. loop through all of the pixels in the output image



def create_dep_to_equi(ti,dir_gt):
    os.makedirs(os.path.join(dir_gt, 'DEPTH'), exist_ok=True)

    # Tglo0 = time.time()
    camera_list = ["front","left","right","top","bottom","back"]
    posx = np.loadtxt(os.path.normpath(os.path.join(dir_gt, 'CUBEMAPS/' + str(ti) + '_1_' + camera_list[0] + '.dep')))
    negx = np.loadtxt(os.path.normpath(os.path.join(dir_gt, 'CUBEMAPS/' + str(ti) + '_1_' + camera_list[-1] + '.dep')))
    posy = np.loadtxt(os.path.normpath(os.path.join(dir_gt, 'CUBEMAPS/' + str(ti) + '_1_' + camera_list[2] + '.dep')))
    negy = np.loadtxt(os.path.normpath(os.path.join(dir_gt, 'CUBEMAPS/' + str(ti) + '_1_' + camera_list[1] + '.dep')))
    posz = np.loadtxt(os.path.normpath(os.path.join(dir_gt, 'CUBEMAPS/' + str(ti) + '_1_' + camera_list[3] + '.dep')))
    negz = np.loadtxt(os.path.normpath(os.path.join(dir_gt, 'CUBEMAPS/' + str(ti) + '_1_' + camera_list[4] + '.dep')))
    # Tglo1 = time.time() - Tglo0
    # print("Load in: ",Tglo1)

    posz = np.fliplr(np.flipud(posz))
    negz = np.fliplr(np.flipud(negz))

    squareLength = posx.shape[0]
    halfSquareLength = squareLength/2

    outputWidth = squareLength
    outputHeight = squareLength/2
    # outputWidth = squareLength*2
    # outputHeight = squareLength*1
    maxdep = 100

    output = []
    # 6. write the output array to a new image file
    for loopY in range(0,int(outputHeight)):        # 0..height-1 inclusive

        for loopX in range(0,int(outputWidth)):

            # 2. get the normalised u,v coordinates for the current pixel

            U = float(loopX)/(outputWidth-1)        # 0..1
            V = float(loopY)/(outputHeight-1)        # no need for 1-... as the image output needs to start from the top anyway.

            # 3. taking the normalised cartesian coordinates calculate the polar coordinate for the current pixel

            theta = U*2*math.pi
            phi = V*math.pi

            # 4. calculate the 3D cartesian coordinate which has been projected to a cubes face

            cart = convertEquirectUVtoUnit2D(theta,phi,squareLength)

            # 5. use this pixel to extract the colour

            output.append(getColour(cart["x"],cart["y"],cart["index"],posx,negx,posy,negy,posz,negz))

    pred = np.array(output).reshape(int(outputHeight),int(outputWidth))
    pred = np.minimum(pred, maxdep)
    cut_place = int(outputWidth/2)
    pred_left = pred[:,:cut_place]
    # print(pred_left.shape)
    pred_right = pred[:,cut_place:]
    # print(pred_right.shape)
    pred = np.hstack((pred_right,pred_left))
    # Tglo2 = time.time() - Tglo0
    # print("Compute in: ",Tglo2-Tglo1)

    np.savetxt(os.path.normpath(os.path.join(dir_gt, 'DEPTH/' + str(ti) + '_1_' + camera_list[0] + '.dep')),pred)

    # print(pred.shape)
    my_dpi = 55
    plt.figure(figsize=(1.3*pred.shape[1]/my_dpi, 1.3*pred.shape[0]/my_dpi), dpi=my_dpi)
    fig = plt.imshow(pred, cmap='magma_r')
    plt.axis('off')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.savefig(os.path.normpath(os.path.join(dir_gt, 'DEPTH/' + str(ti) + '_5_' + camera_list[0] + '.png')), bbox_inches='tight', pad_inches=0, dpi=my_dpi)
    plt.close()

    # Tglo3 = time.time() - Tglo0
    # print("SAVE in: ",Tglo3-Tglo2)

    # outputImage = Image.new("RGB",((int(outputWidth)),(int(outputHeight))), None)
    # outputImage.putdata(output)
    # filePath = '.'
    # outputImage.save(filePath+str(ti)+"_EQUI.png")
    # print("Done for "+str(ti)+"_EQUI.png")

def create_dep_to_equi_v2(ti, dir_gt):
    os.makedirs(os.path.join(dir_gt, 'DEPTH'), exist_ok=True)

    # Tglo0 = time.time()
    camera_list = ["front","left","right","top","bottom","back"]
    posx = np.loadtxt(os.path.normpath(os.path.join(dir_gt, 'CUBEMAPS/' + str(ti) + '_1_' + camera_list[0] + '.dep')))
    negx = np.loadtxt(os.path.normpath(os.path.join(dir_gt, 'CUBEMAPS/' + str(ti) + '_1_' + camera_list[-1] + '.dep')))
    posy = np.loadtxt(os.path.normpath(os.path.join(dir_gt, 'CUBEMAPS/' + str(ti) + '_1_' + camera_list[2] + '.dep')))
    negy = np.loadtxt(os.path.normpath(os.path.join(dir_gt, 'CUBEMAPS/' + str(ti) + '_1_' + camera_list[1] + '.dep')))
    posz = np.loadtxt(os.path.normpath(os.path.join(dir_gt, 'CUBEMAPS/' + str(ti) + '_1_' + camera_list[3] + '.dep')))
    negz = np.loadtxt(os.path.normpath(os.path.join(dir_gt, 'CUBEMAPS/' + str(ti) + '_1_' + camera_list[4] + '.dep')))
    # Tglo1 = time.time() - Tglo0
    # print("Load in: ",Tglo1)

    # posz = np.fliplr(np.flipud(posz))
    # negz = np.fliplr(np.flipud(negz))

    squareLength = posx.shape[0]
    halfSquareLength = squareLength/2

    outputWidth = squareLength
    outputHeight = squareLength/2
    # outputWidth = squareLength*2
    # outputHeight = squareLength*1
    maxdep = 100

    output = []
    # 6. write the output array to a new image file
    for loopY in range(0,int(outputHeight)):        # 0..height-1 inclusive

        for loopX in range(0,int(outputWidth)):

            # 2. get the normalised u,v coordinates for the current pixel

            U = float(loopX)/(outputWidth-1)        # 0..1
            V = float(loopY)/(outputHeight-1)        # no need for 1-... as the image output needs to start from the top anyway.

            # 3. taking the normalised cartesian coordinates calculate the polar coordinate for the current pixel

            theta = U*2*math.pi
            phi = V*math.pi

            # 4. calculate the 3D cartesian coordinate which has been projected to a cubes face

            cart = convertEquirectUVtoUnit2D(theta,phi,squareLength)

            # 5. use this pixel to extract the colour

            output.append(getColour(cart["x"],cart["y"],cart["index"],posx,negx,posy,negy,posz,negz))

    pred = np.array(output).reshape(int(outputHeight),int(outputWidth))
    pred = np.minimum(pred, maxdep)
    cut_place = int(outputWidth/2)
    pred_left = pred[:,:cut_place]
    # print(pred_left.shape)
    pred_right = pred[:,cut_place:]
    # print(pred_right.shape)
    pred = np.hstack((pred_right,pred_left))
    # Tglo2 = time.time() - Tglo0
    # print("Compute in: ",Tglo2-Tglo1)

    np.savetxt(os.path.normpath(os.path.join(dir_gt, 'DEPTH/' + str(ti) + '_1_' + camera_list[0] + '.dep')),pred)

    # print(pred.shape)
    my_dpi = 55
    plt.figure(figsize=(1.3*pred.shape[1]/my_dpi, 1.3*pred.shape[0]/my_dpi), dpi=my_dpi)
    fig = plt.imshow(pred, cmap='magma_r')
    plt.axis('off')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.savefig(os.path.normpath(os.path.join(dir_gt, 'DEPTH/' + str(ti) + '_5_' + camera_list[0] + '.png')), bbox_inches='tight', pad_inches=0, dpi=my_dpi)
    plt.close()

    # Tglo3 = time.time() - Tglo0
    # print("SAVE in: ",Tglo3-Tglo2)

    # outputImage = Image.new("RGB",((int(outputWidth)),(int(outputHeight))), None)
    # outputImage.putdata(output)
    # filePath = '.'
    # outputImage.save(filePath+str(ti)+"_EQUI.png")
    # print("Done for "+str(ti)+"_EQUI.png")


def multi_dep_to_equi(dir_gt):
    list_file_gt = [file for file in sorted(os.listdir(dir_gt+'/CUBEMAPS/')) if (file.endswith('.dep'))]
    nb_idx = int(len(list_file_gt)/6)
    print("Working in: ",dir_gt)
    print("Iterations: ",nb_idx)
    os.makedirs(os.path.join(dir_gt, 'DEPTH'), exist_ok=True)
    parmap.map(create_dep_to_equi, range(nb_idx), dir_gt, pm_processes=multiprocessing.cpu_count()-2, pm_pbar=True)
