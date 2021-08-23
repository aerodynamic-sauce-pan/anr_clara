"""Module for easy cubemap and equirectangular capture.

This module offers methods to capture perspective avec equirectangular images
of the UE4 scene in different view modes : RGB, Depth estimation, Semantic
Segmentation.

In settings.json first activate computer vision mode:
https://github.com/Microsoft/AirSim/blob/master/docs/image_apis.md#computer-vision-mode
"""
#import setup_path
import airsim

import os
import sys
import time
import argparse
#from sys import platform

import numpy as np
#import cv2
import pandas as pd
#from PIL import Image, ImageOps
import matplotlib.pyplot as plt

#import pprint


class cube2sph_2():
    def __init__(self, ti, save_dir, view, W):
        # camera_list = ["front", "left", "right", "top", "bottom", "back"]
        # camera_list = ["front_custom", "left_custom", "right_custom", "top_custom", "bottom_custom", "back_custom"]
        camera_list = ["front_custom", "back_custom", "right_custom",
                       "left_custom", "top_custom", "bottom_custom"]
        self.camera_list = camera_list
        # self.cam = ["4", "3", "1", "5", "2", "0"]
        # self.cam = ["0", "0", "0", "0", "0", "0"]

        self.view = view
        self.ti = ti
        self.Hcube = W
        self.Wcube = W
        self.Hequi = int(W/2)
        self.Wequi = W

        self.maxdep = 100

        # print("LOADING TABLE: "+'Lookup_Table_' +
                                    # str(self.Wequi)+'_'+str(self.Hequi)+'.npy')
        self.lookup_table = np.load('Lookup_Table_' +
                                    str(self.Wequi)+'_'+str(self.Hequi)+'.npy')
        # print(self.lookup_table)

        self.cube_rgb = np.zeros((len(camera_list), self.Hcube, self.Wcube, 3))
        self.cube_depth = np.zeros((len(camera_list), self.Hcube, self.Wcube))
        self.output = np.zeros((self.Hequi, self.Wequi, 3))
        # self.output = []
        self.responses_list = []

        self.save_dir = save_dir

    def build_img_request(self, mode):
        # pp = pprint.PrettyPrinter(indent=4)
        # for cam_elt in self.camera_list:
        #     camera_info = client.simGetCameraInfo(str(cam_elt))
        #     print("CameraInfo %s: %s" % (cam_elt, pp.pprint(camera_info)))
        if mode == 0:
            for cam_elt in self.camera_list:
                self.responses_list.append(
                    airsim.ImageRequest(str(cam_elt), 0, False, False))
        elif mode == 1:
            for cam_elt in self.camera_list:
                self.responses_list.append(
                    airsim.ImageRequest(str(cam_elt), 2, True, False))
        elif mode == 2:
            for cam_elt in self.camera_list:
                self.responses_list.append(
                    airsim.ImageRequest(str(cam_elt), 5, False, False))
        else:
            sys.exit("Feature mode not recognized.")

    def process_img_request(self):
        if self.view != -1:
            self.build_img_request(self.view)
        else:
            for mode_i in range(3):
                self.build_img_request(mode_i)

        # print(self.responses_list)
        responses = client.simGetImages(self.responses_list)
        # print(responses)

        for i, response in enumerate(responses):
            if response.pixels_as_float:
                if VERBOSE:
                    print("Type %d, size %d" % (response.image_type,
                                                len(response.image_data_float)))
                depth = np.array(airsim.get_pfm_array(
                    response), dtype=np.float32)
                self.cube_depth[i, :] = depth.reshape(
                    response.height, response.width)
            else:
                if VERBOSE:
                    print("Type %d, size %d" % (response.image_type,
                                                len(response.image_data_uint8)))
                rgb = np.frombuffer(response.image_data_uint8, dtype=np.uint8).reshape(
                    response.height, response.width, 3)
                rgb = np.fliplr(np.fliplr(rgb))
                self.cube_rgb[i, :] = rgb

        if self.view != -1:
            for U in range(0, self.Hequi):
                for V in range(0, self.Wequi):
                    self.getPixelInCube([U, V], self.view)

            self.recenter_equi()
            if self.view != 1:
                # for i in range(6):
                #     self.create_cub_rgb(i, self.save_dir)

                self.create_equi_rgb(self.save_dir)
            else:
                self.create_equi_depth(self.save_dir)
        else:
            sys.error("Error")

    def recenter_equi(self):
        cut_place = int(self.Wequi/2)
        pred_left = self.output[:, :cut_place, :]
        # print(pred_left.shape)
        pred_right = self.output[:, cut_place:, :]
        # print(pred_right.shape)
        self.output = np.hstack((pred_right, pred_left))

    def getPixelInCube(self, POS, mode):
        x = int(self.lookup_table[POS[0], POS[1], 1])
        y = int(self.lookup_table[POS[0], POS[1], 2])
        if mode != 1:
            self.output[POS[0], POS[1], :] = self.cube_rgb[int(
                self.lookup_table[POS[0], POS[1], 0]), y, x, :]
        else:
            self.output[POS[0], POS[1], 0] = self.cube_depth[int(
                self.lookup_table[POS[0], POS[1], 0]), y, x]

    def create_equi_rgb(self, save_dir):
        airsim.write_png(os.path.normpath(os.path.join(
            save_dir, str(self.ti)+'_'+str(self.view)+".png")), self.output)
        if VERBOSE:
            print("Done for "+str(self.ti)+'_'+str(self.view)+".png")

    def create_cub_rgb(self, idx, save_dir):
        airsim.write_png(os.path.normpath(os.path.join(save_dir, str(
            self.ti)+'_'+str(self.camera_list[idx])+'_'+str(self.view)+".png")), self.cube_rgb[idx, :])
        if VERBOSE:
            print("Done for "+str(self.ti)+'_' +
                  str(self.camera_list[idx])+'_'+str(self.view)+".png")

    def create_equi_depth(self, save_dir):
        pred = np.minimum(self.output[:, :, 0], self.maxdep)

        np.savetxt(os.path.normpath(os.path.join(
            save_dir, str(self.ti) + '_1.dep')), pred)

        # Depth image
        # my_dpi = 55
        # plt.figure(figsize=(1.3*pred.shape[1]/my_dpi,
        #                     1.3*pred.shape[0]/my_dpi), dpi=my_dpi)
        # fig = plt.imshow(pred, cmap='magma_r')
        # plt.axis('off')
        # fig.axes.get_xaxis().set_visible(False)
        # fig.axes.get_yaxis().set_visible(False)
        # plt.savefig(os.path.normpath(os.path.join(save_dir, str(
        #     self.ti) + '_1.png')), bbox_inches='tight', pad_inches=0, dpi=my_dpi)
        # plt.close()
        if VERBOSE:
            print("Done for "+str(self.ti)+'_'+str(self.view)+".png")

# Scene = 0,
# DepthPlanner = 1,
# DepthPerspective = 2,# DepthVis = 3,
# DisparityNormalized = 4,
# Segmentation = 5,
# SurfaceNormals = 6,
# Infrared = 7


PARSER = argparse.ArgumentParser()
PARSER.add_argument('-s', '--source',
                    nargs='?',
                    type=str,
                    default='./OUTPUT',
                    help='Source directory containing the cubemap images in a '
                         '\'CUBEMAP\' folder (defaults to ../resources/CAPTURES).')
PARSER.add_argument('-p', '--shape',
                    nargs=2,
                    type=int,
                    default=[1000, 500],
                    metavar=('width', 'height'),
                    help='Target equirectangular shape (defaults to 1000x500).')
PARSER.add_argument('-m', '--method',
                    nargs='?',
                    type=str,
                    default='single_cam',
                    help='Cubemap images acquisition method. single_cam: use 1'
                         ' camera that rotates. multi_cam: use 6 independantly'
                         'fixed cameras.')
PARSER.add_argument('--pose_record',
                    nargs='?',
                    type=str,
                    default='airsim_rec.csv',
                    help='Path to an airsim pos record csv file.')
PARSER.add_argument('--view',
                    nargs='*',
                    type=int,
                    default=[0],
                    help='View type of the capture. 0: RGB, 1: Depth,'
                         '2: Semantic Segmentation, -1: all views.'
                         'Defaults to 0')
PARSER.add_argument('-v', '--VERBOSE',
                    nargs='*',
                    action='store',
                    help='If true, prints out additional info.')


def main():
    """Run main function and handle airsim client."""
    client.confirmConnection()
    seg_obj = {'PFS_RW_Redwood_SmallTrees': 120,
               'Brush_0': 40,
               'Landscape_0': 20,
               'BP_Sky_Sphere_2': 50,
               'InstancedFoliageActor_0': 120}
    for obj_name, obj_id in seg_obj.items():
        success = client.simSetSegmentationObjectID(obj_name, obj_id)
        if VERBOSE:
            print('Found mesh \'{0}\' : {1}'.format(obj_name, success))
    if VERBOSE:
        print('Objects present in the environment : ',
              client.simListSceneObjects())
        print('Target equirectangular shape : ({0},{1})'.format(OUT_SHAPE[0],
                                                                OUT_SHAPE[1]))

    print("Saving images to %s" % SRC_DIR)

    # Load pose from a previously saved manual path
    rec_pos = pd.read_csv(POSE_REC_FILE,
                          sep='\t')[['POS_X', 'POS_Y', 'POS_Z']]
    nb_case = rec_pos.shape[0]
    pose_list = []
    sig = 0.4
    for ti in range(nb_case):
        print("Iteration n°", ti, "/", nb_case)

        # Values picked from a recorded path
        x = rec_pos['POS_X'][ti]
        y = rec_pos['POS_Y'][ti]
        z = rec_pos['POS_Z'][ti]
        pitch = 0*np.pi/2*np.random.normal(0.0, sig)

        # Randomly values
        # x = 0*int(200*np.random.normal(0.0, sig))+ti
        # y = 0*int(200*np.random.normal(0.0, sig))
        # pitch = 0*np.pi/2*np.random.normal(0.0, sig)

        yaw = 0.
        roll = 0.
        if ti == 0:
            pose = [ti, 0., 0., 0., 0., 0., 0., 0.]
        else:
            pose = [ti, x, y, z, yaw, pitch, roll,
                    client.simGetCollisionInfo().time_stamp]
        pose_list.append(pose)
        print(pose)
        # client.moveByVelocity(vx, vy, vz, duration)
        # client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(pose[1],
        #                                                      pose[2],
        #                                                      pose[3]),
        #                                      airsim.to_quaternion(pose[4],
        #                                                           pose[5],
        #                                                           pose[6])),
        #                          True)
        client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(
            pose[1], pose[2], pose[3]), airsim.to_quaternion(pose[4], pose[5], pose[6])), True)

        if VIEW == -1:
            for mode in range(3):
                t_cub2sph = time.time()
                cube2sph_2_elt = cube2sph_2(ti, SRC_DIR, mode, OUT_SHAPE[0])
                cube2sph_2_elt.process_img_request()
                t_cub2sph = time.time() - t_cub2sph
                print("Cube2sphere in {0}s".format(t_cub2sph))
        else:
            for view in VIEW:
                t_cub2sph = time.time()
                cube2sph_2_elt = cube2sph_2(ti, SRC_DIR, view, OUT_SHAPE[0])
                cube2sph_2_elt.process_img_request()
                t_cub2sph = time.time() - t_cub2sph
                print("Cube2sphere in {0}s".format(t_cub2sph))

        # # Capture from 1 camera that rotates
        # if METHOD == 'single_cam':
        #     get_cubemap_single(ti, cube_dir)

        # # Capture from 6 fixed cameras
        # elif METHOD == 'multi_cam':
        #     cube2sph_2
        #     # capture_scene_full(ti, cube_dir, equi_dir, camera_list)
        #     # capture_scene(ti, cube_dir, equi_dir, camera_list,loc_feature="scene")
        #     # print(client.simGetCollisionInfo().time_stamp)
        #     #print('Not implemented yet !')
        # else:
        #     print('Unknown method. Terminating...')
        #     break


if __name__ == '__main__':
    args = PARSER.parse_args()
    SRC_DIR = args.source
    METHOD = args.method
    OUT_SHAPE = args.shape
    VERBOSE = args.VERBOSE is not None
    VIEW = args.view
    POSE_REC_FILE = args.pose_record
    client = airsim.VehicleClient()
    main()
