
from PIL import Image    # Python Imaging Library
import math                # Maths functions
import sys                # Allows us to access function args
import os                # Allows us to split the text for saving the file
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
import parmap
import time


class cube2sph():
    def __init__(self, ti, working_dir, num_feature, equi_dir):
        camera_list = ["front", "left", "right", "top", "bottom", "back"]
        self.camera_list = camera_list
        self.num_feature = num_feature
        self.ti = ti
        if num_feature != 1:
            self.posx = Image.open(os.path.normpath(os.path.join(
                working_dir, 'CUBEMAPS/' + str(num_feature) + '_' + camera_list[0] + '.png')))
            self.negx = Image.open(os.path.normpath(os.path.join(
                working_dir, 'CUBEMAPS/' + str(num_feature) + '_' + camera_list[-1] + '.png')))
            self.posy = Image.open(os.path.normpath(os.path.join(
                working_dir, 'CUBEMAPS/' + str(num_feature) + '_' + camera_list[2] + '.png')))
            self.negy = Image.open(os.path.normpath(os.path.join(
                working_dir, 'CUBEMAPS/' + str(num_feature) + '_' + camera_list[1] + '.png')))
            self.posz = Image.open(os.path.normpath(os.path.join(
                working_dir, 'CUBEMAPS/' + str(num_feature) + '_' + camera_list[3] + '.png')))
            self.negz = Image.open(os.path.normpath(os.path.join(
                working_dir, 'CUBEMAPS/' + str(num_feature) + '_' + camera_list[4] + '.png')))
            self.outputWidth = int(self.posx.size[0])
        else:
            self.posx = np.loadtxt(os.path.normpath(os.path.join(
                working_dir, 'CUBEMAPS/' + '1_' + camera_list[0] + '.dep')))
            self.negx = np.loadtxt(os.path.normpath(os.path.join(
                working_dir, 'CUBEMAPS/' + '1_' + camera_list[-1] + '.dep')))
            self.posy = np.loadtxt(os.path.normpath(os.path.join(
                working_dir, 'CUBEMAPS/' + '1_' + camera_list[2] + '.dep')))
            self.negy = np.loadtxt(os.path.normpath(os.path.join(
                working_dir, 'CUBEMAPS/' + '1_' + camera_list[1] + '.dep')))
            self.posz = np.loadtxt(os.path.normpath(os.path.join(
                working_dir, 'CUBEMAPS/' + '1_' + camera_list[3] + '.dep')))
            self.negz = np.loadtxt(os.path.normpath(os.path.join(
                working_dir, 'CUBEMAPS/' + '1_' + camera_list[4] + '.dep')))
            self.outputWidth = int(self.posx.shape[0])
        self.outputHeight = int(self.outputWidth/2)
        self.lookup_table = np.load('Lookup_Table_' +
                                    str(self.outputWidth)+'_'+str(self.outputHeight)+'.npy')
        self.output = np.zeros((self.outputHeight, self.outputWidth, 4))

    def getPixelInCube(self, POS):
        x = int(self.lookup_table[POS[0], POS[1], 1])
        y = int(self.lookup_table[POS[0], POS[1], 2])
        if self.num_feature != 1:
            if(self.lookup_table[POS[0], POS[1], 0] == 0):
                self.output[POS[0], POS[1], :] = self.posx.getpixel((x, y))
            elif(self.lookup_table[POS[0], POS[1], 0] == 1):
                self.output[POS[0], POS[1], :] = self.negx.getpixel((x, y))
            elif(self.lookup_table[POS[0], POS[1], 0] == 2):
                self.output[POS[0], POS[1], :] = self.posy.getpixel((x, y))
            elif(self.lookup_table[POS[0], POS[1], 0] == 3):
                self.output[POS[0], POS[1], :] = self.negy.getpixel((x, y))
            elif(self.lookup_table[POS[0], POS[1], 0] == 4):
                self.output[POS[0], POS[1], :] = self.posz.getpixel((x, y))
            elif(self.lookup_table[POS[0], POS[1], 0] == 5):
                self.output[POS[0], POS[1], :] = self.negz.getpixel((x, y))
        else:
            if(self.lookup_table[POS[0], POS[1], 0] == 0):
                self.output[POS[0], POS[1], 0] = self.posx[y, x]
            elif(self.lookup_table[POS[0], POS[1], 0] == 1):
                self.output[POS[0], POS[1], 0] = self.negx[y, x]
            elif(self.lookup_table[POS[0], POS[1], 0] == 2):
                self.output[POS[0], POS[1], 0] = self.posy[y, x]
            elif(self.lookup_table[POS[0], POS[1], 0] == 3):
                self.output[POS[0], POS[1], 0] = self.negy[y, x]
            elif(self.lookup_table[POS[0], POS[1], 0] == 4):
                self.output[POS[0], POS[1], 0] = self.posz[y, x]
            elif(self.lookup_table[POS[0], POS[1], 0] == 5):
                self.output[POS[0], POS[1], 0] = self.negz[y, x]

    def recenter_equi(self):
        cut_place = int(self.outputWidth/2)
        pred_left = self.output[:, :cut_place, :]
        pred_right = self.output[:, cut_place:, :]
        self.output = np.hstack((pred_right, pred_left))

    def create_equi_rgb(self, save_dir):
        outputImage = Image.fromarray(np.uint8(self.output))
        outputImage.save(os.path.normpath(os.path.join(
            save_dir, str(self.ti)+'_'+str(self.num_feature)+".png")))
        print("Done for "+str(self.ti)+'_'+str(self.num_feature)+".png")

    def create_equi_depth(self, save_dir, maxdep):
        pred = np.minimum(self.output[:, :, 0], maxdep)

        np.savetxt(os.path.normpath(os.path.join(save_dir, 'DEPTH/' +
                                                 str(self.ti) + '_1.dep')), pred)

        my_dpi = 55
        plt.figure(figsize=(1.3*pred.shape[1]/my_dpi,
                            1.3*pred.shape[0]/my_dpi), dpi=my_dpi)
        fig = plt.imshow(pred, cmap='magma_r')
        plt.axis('off')
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        plt.savefig(os.path.normpath(os.path.join(save_dir, 'DEPTH/' +
                                                  str(self.ti) + '_5.png')), bbox_inches='tight', pad_inches=0, dpi=my_dpi)
        plt.close()


class LookUpTable():
    def __init__(self, Wcube):
        self.Hcube = Wcube
        self.Wcube = Wcube
        self.Hequi = int(Wcube/2)
        self.Wequi = Wcube
        self.lookup_table = np.zeros((self.Hequi , self.Wequi, 3)) - 1 # -1 to get error if table not correctly filled

    def unit3DToUnit2D(self, x, y, z, faceIndex):
        if(faceIndex == "X+"):
            x2D = y+0.5
            y2D = z+0.5
        elif(faceIndex == "Y+"):
            x2D = (x*-1)+0.5
            y2D = z+0.5
        elif(faceIndex == "X-"):
            x2D = (y*-1)+0.5
            y2D = z+0.5
        elif(faceIndex == "Y-"):
            x2D = x+0.5
            y2D = z+0.5
        elif(faceIndex == "Z+"):
            x2D = y+0.5
            y2D = (x*-1)+0.5
        else:
            x2D = y+0.5
            y2D = x+0.5

        y2D = 1-y2D

        return (x2D, y2D)

    def projectX(self, theta, phi, sign):
        x = sign*0.5
        faceIndex = "X+" if sign == 1 else "X-"
        rho = float(x)/(math.cos(theta)*math.sin(phi))
        y = rho*math.sin(theta)*math.sin(phi)
        z = rho*math.cos(phi)
        return (x, y, z, faceIndex)

    def projectY(self, theta, phi, sign):
        y = sign*0.5
        faceIndex = "Y+" if sign == 1 else "Y-"
        rho = float(y)/(math.sin(theta)*math.sin(phi))
        x = rho*math.cos(theta)*math.sin(phi)
        z = rho*math.cos(phi)
        return (x, y, z, faceIndex)

    def projectZ(self, theta, phi, sign):
        z = sign*0.5
        faceIndex = "Z+" if sign == 1 else "Z-"
        rho = float(z)/math.cos(phi)
        x = rho*math.cos(theta)*math.sin(phi)
        y = rho*math.sin(theta)*math.sin(phi)
        return (x, y, z, faceIndex)

    def getLookUpTable(self, x, y, index):
        if(index == "X+"):
            return [0, x, y]
        elif(index == "X-"):
            return [1, x, y]
        elif(index == "Y+"):
            return [2, x, y]
        elif(index == "Y-"):
            return [3, x, y]
        elif(index == "Z+"):
            return [4, x, y]
        elif(index == "Z-"):
            return [5, x, y]

    def convertEquirectUVtoUnit2D(self, theta, phi, squareLength):

        # calculate the unit vector

        x = math.cos(theta)*math.sin(phi)
        y = math.sin(theta)*math.sin(phi)
        z = math.cos(phi)

        # find the maximum value in the unit vector

        maximum = max(abs(x), abs(y), abs(z))
        xx = x/maximum
        yy = y/maximum
        zz = z/maximum

        # project ray to cube surface

        if(xx == 1 or xx == -1):
            (x, y, z, faceIndex) = self.projectX(theta, phi, xx)
        elif(yy == 1 or yy == -1):
            (x, y, z, faceIndex) = self.projectY(theta, phi, yy)
        else:
            (x, y, z, faceIndex) = self.projectZ(theta, phi, zz)

        (x, y) = self.unit3DToUnit2D(x, y, z, faceIndex)

        x *= squareLength
        y *= squareLength

        x = int(x)
        y = int(y)

        return {"index": faceIndex, "x": x, "y": y}

    def create_table(self, save_dir):
        if self.Wequi != self.Wcube:
            print("Warning: not same width for cube and equi!!!")

        for loopY in range(0, self.Hequi):
            for loopX in range(0, self.Wequi):
                U = float(loopX)/(self.Wequi-1)
                V = float(loopY)/(self.Hequi-1)
                theta = U*2*math.pi
                phi = V*math.pi
                cart = self.convertEquirectUVtoUnit2D(theta, phi, self.Wequi)
                
                self.lookup_table[loopY, loopX, :] = self.getLookUpTable(
                    cart["x"], cart["y"], cart["index"])
                # print(loopY,loopX,self.lookup_table[loopY, loopX, :],cart)

        np.save(os.path.join(save_dir, 'Lookup_Table_' +
                             str(self.Wequi)+'_'+str(self.Hequi)+'.npy'), self.lookup_table)


def create_dep_to_equi_v3(ti, working_dir, num_feature, equi_dir):
    os.makedirs(os.path.join(working_dir, 'DEPTH'), exist_ok=True)

    Tglo0 = time.time()
    cube2sph_elt = cube2sph(ti, working_dir, num_feature, equi_dir)
    Tglo1 = time.time() - Tglo0
    print("Load in: ", Tglo1)

    for U in range(0, cube2sph_elt.outputHeight):
        for V in range(0, cube2sph_elt.outputWidth):
            cube2sph_elt.getPixelInCube([U, V])

    cube2sph_elt.recenter_equi()

    # loopU = np.arange(0,cube2sph_elt.outputHeight,1)
    # loopV = np.arange(0,cube2sph_elt.outputWidth,1)
    # UU, VV = np.meshgrid(loopU, loopV)
    # listUV = np.dstack([UU, VV]).reshape(-1, 2)
    # parmap.map(cube2sph_elt.getPixelInCube, listUV, pm_processes=multiprocessing.cpu_count()-2, pm_pbar=True)

    # print(cube2sph_elt.output)

    Tglo2 = time.time() - Tglo0
    print("Compute in: ", Tglo2-Tglo1)

    if cube2sph_elt.num_feature != 1:
        cube2sph_elt.create_equi_rgb(os.path.join(working_dir, 'EQUI'))
    else:
        maxdep = 100
        cube2sph_elt.create_equi_depth(working_dir, maxdep)

    Tglo3 = time.time() - Tglo2
    print("SAVE in: ", Tglo3)

def create_lookup_table(Wcube, save_dir):
    LUT = LookUpTable(Wcube)
    print("Creating LookUp Table Cube "+str(LUT.Wcube)+"x"+str(LUT.Hcube)+" to Equi "+str(LUT.Wequi)+"x"+str(LUT.Hequi))
    
    LUT.create_table(save_dir)
    # print(LUT.lookup_table)
    
# def multi_dep_to_equi(working_dir):
#     list_file_gt = [file for file in sorted(os.listdir(
#         working_dir+'/CUBEMAPS/')) if (file.endswith('.dep'))]
#     nb_idx = int(len(list_file_gt)/6)
#     print("Working in: ", working_dir)
#     print("Iterations: ", nb_idx)
#     os.makedirs(os.path.join(working_dir, 'DEPTH'), exist_ok=True)
#     parmap.map(create_dep_to_equi, range(nb_idx), working_dir,
#                pm_processes=multiprocessing.cpu_count()-2, pm_pbar=True)
