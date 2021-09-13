"""Module for easy cubemap and equirectangular capture.

This module offers methods to capture perspective avec equirectangular images
of the UE4 scene in different view modes : RGB, Depth estimation, Semantic
Segmentation.

In settings.json first activate computer vision mode:
https://github.com/Microsoft/AirSim/blob/master/docs/image_apis.md#computer-vision-mode
"""

import os
import time
import argparse
from sys import platform

import numpy as np
import cv2
import pandas as pd
from PIL import Image, ImageOps

import airsim
import dep_to_equi

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
                    default='./CAPTURES',
                    help='Source directory containing the cubemap images in a '
                         '\'CUBEMAP\' folder (defaults to ./CAPTURES).')
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
PARSER.add_argument('--view',
                    nargs='?',
                    type=int,
                    default=0,
                    help='View type of the capture. 0: RGB, 1: Depth,'
                         '2: Semantic Segmentation, -1: all views.'
                         'Defaults to 0')
PARSER.add_argument('-v', '--verbose',
                    nargs='*',
                    action='store',
                    help='If true, prints out additional info.')


def get_single_camera(camera_name, ti, cube_dir):
    """Capture images from a single camera (all views).

    Query and capture RGB, depth and semantic segmentation images
    of the scene from a single camera of ID 0.

    Args:
        camera_name (str): name of the cam orientation ('front', 'left' etc...)
        ti (int): iteration number (id of the capture)
        cube_dir (str): subdirectory of CAPTURES/ where to store the
                        (defaults to CUBEMAPS/)
    """
    responses = client.simGetImages([
        airsim.ImageRequest("0", airsim.ImageType.Scene),
        airsim.ImageRequest("0", 2, True, False),
        #airsim.ImageRequest("0", 5)
        ])
    write_responses(responses, cube_dir, camera_name, ti)


def get_full_scene(cube_dir, camera_list, ti, loc_feature='Scene'):
    """Capture images from 6 cameras (single view).

    Query and capture images of a single specified view of the scene,
    from each of the 6 cameras necessary to form a cubemap. By default,
    the RGB scene is captured.

    Args:
        cube_dir (str): path to the directory containing the cubemap images
        loc_feature (str): view type to query and capture (see airsim.ImageType)
        camera_list (list[str]): list of camera names (used for output file
                                 names) which length should match the number
                                 of queried cameras
    """
    airsim_feature = getattr(airsim.ImageType, loc_feature)
    responses = client.simGetImages([
        airsim.ImageRequest("0", airsim_feature),
        airsim.ImageRequest("1", airsim_feature),
        airsim.ImageRequest("2", airsim_feature),
        airsim.ImageRequest("3", airsim_feature),
        airsim.ImageRequest("4", airsim_feature),
        airsim.ImageRequest("5", airsim_feature),
        ])
    write_full_scene(responses, cube_dir, camera_list, ti)


def get_full_camera(cube_dir, camera_list):
    """Capture images from 6 cameras (all views).

    Query and capture images of a every views of the scene (RGB, Depth, Semantic
    Segmentation), from each of the 6 cameras necessary to form a cubemap.

    Args:
        cube_dir (str): path to the directory containing the cubemap images
        loc_feature (str): view type to query and capture (see airsim.ImageType)
        camera_list (list[str]): list of camera names (used for output file
                                 names) which length should match the number
                                 of queried cameras
    """
    responses = client.simGetImages([
        airsim.ImageRequest("0", airsim.ImageType.Scene),
        airsim.ImageRequest("0", 2, True, False),
        airsim.ImageRequest("0", 5),
        airsim.ImageRequest("1", airsim.ImageType.Scene),
        airsim.ImageRequest("1", 2, True, False),
        airsim.ImageRequest("1", 5),
        airsim.ImageRequest("2", airsim.ImageType.Scene),
        airsim.ImageRequest("2", 2, True, False),
        airsim.ImageRequest("2", 5),
        airsim.ImageRequest("3", airsim.ImageType.Scene),
        airsim.ImageRequest("3", 2, True, False),
        airsim.ImageRequest("3", 5),
        airsim.ImageRequest("4", airsim.ImageType.Scene),
        airsim.ImageRequest("4", 2, True, False),
        airsim.ImageRequest("4", 5),
        airsim.ImageRequest("5", airsim.ImageType.Scene),
        airsim.ImageRequest("5", 2, True, False),
        airsim.ImageRequest("5", 5)
        ])
    write_full_responses(responses, cube_dir, camera_list)


def get_cubemap_single(ti, cube_dir):
    """Rotate and capture images from a single camera.

    Angles for Pitch, Roll and Yaw in airsim.to_quaternions are given in
    radians.

    Args:
        ti (int): iteration index (id of the capture)
        cube_dir (str): path to the directory containing the cubemap images
    """
    t_single_cubemap = time.time()
    angle90 = np.deg2rad(90)
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0),
                              airsim.to_quaternion(0, 0, 0))
    client.simSetCameraPose(0, camera_pose)
    get_single_camera("front", ti, cube_dir)

    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0),
                              airsim.to_quaternion(0, 0, angle90))
    client.simSetCameraPose(0, camera_pose)
    get_single_camera("right", ti, cube_dir)

    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0),
                              airsim.to_quaternion(0, 0, -angle90))
    client.simSetCameraPose(0, camera_pose)
    get_single_camera("left", ti, cube_dir)

    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0),
                              airsim.to_quaternion(angle90, 0, 0))
    client.simSetCameraPose(0, camera_pose)
    get_single_camera("top", ti, cube_dir)

    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0),
                              airsim.to_quaternion(-angle90, 0, 0))
    client.simSetCameraPose(0, camera_pose)
    get_single_camera("bottom", ti, cube_dir)

    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0),
                              airsim.to_quaternion(0, 0, -2*angle90))
    client.simSetCameraPose(0, camera_pose)
    get_single_camera("back", ti, cube_dir)
    print("Cubemap computed in : {0}s".format(time.time() - t_single_cubemap))


def write_responses(responses, cube_dir, camera_name, ti):
    """Write captured images into files (single cam / all view mode).

    Args:
        responses (list[ImageResponse]): list of scene images captured from
                                         the cameras
        cube_dir (str): path to the directory containing the cubemap images
        camera_name (str): name of the cam orientation ('front', 'left' etc...)
        ti (int): iteration index (id of the capture)
    """
    if VERBOSE:
        print("============== write_responses ==============")
    for i, response in enumerate(responses):
        fp = str(ti) + '_' + str(i) + '_' + camera_name
        if response.pixels_as_float:
            if VERBOSE:
                print("Type %d, size %d" % (response.image_type,
                                            len(response.image_data_float)))
            depth = np.array(airsim.get_pfm_array(response), dtype=np.float32)
            depth = depth.reshape(response.height, response.width)
            np.savetxt(os.path.normpath(os.path.join(cube_dir, fp + '.dep')),
                       depth)
            cv2.imwrite(os.path.normpath(os.path.join(cube_dir, fp + '.png')),
                        depth)
        else:
            if VERBOSE:
                print("Type %d, size %d" % (response.image_type,
                                            len(response.image_data_uint8)))
            airsim.write_file(os.path.normpath(os.path.join(cube_dir,
                                                            fp + '.png')),
                              response.image_data_uint8)


def write_full_scene(responses, cube_dir, camera_list, ti):
    """Write captured images into files (multi cam / mono view mode).

    Args:
        responses (list[ImageResponse]): list of scene images captured from
                                         the cameras
        cube_dir (str): path to the directory containing the cubemap images
        camera_list (str): list of camera names used for output file names
    """
    if VERBOSE:
        print("============== write_full_scene ==============")
    for i, response in enumerate(responses):
        fp = cube_dir, str(ti) + '_0_' + camera_list[int(i)]
        if response.pixels_as_float:
            if VERBOSE:
                print("Type %d, size %d" % (response.image_type,
                                            len(response.image_data_float)))
            depth = np.array(airsim.get_pfm_array(response), dtype=np.float32)
            depth = depth.reshape(response.height, response.width)
            np.savetxt(os.path.normpath(os.path.join(fp + '.dep')),
                       depth)
            cv2.imwrite(os.path.normpath(os.path.join(fp + '.png')),
                        depth)
        else:
            if VERBOSE:
                print("Type %d, size %d" % (response.image_type,
                                            len(response.image_data_uint8)))
            airsim.write_file(os.path.normpath(os.path.join(fp + '.png')),
                              response.image_data_uint8)


def write_full_responses(responses, cube_dir, camera_list):
    """Write captured images into files (multi cam / all views mode).

    Args:
        responses (list[ImageResponse]): list of scene images captured from
                                         the cameras
        cube_dir (str): path to the directory containing the cubemap images
        camera_list (str): list of camera names used for output file names
    """
    if VERBOSE:
        print("============== write_full_responses ==============")
    for i, response in enumerate(responses):
        fp = cube_dir, str(i % 3) + '_' + camera_list[int(i/3)]
        if response.pixels_as_float:
            if VERBOSE:
                print("Type %d, size %d" % (response.image_type,
                                            len(response.image_data_float)))
            depth = np.array(airsim.get_pfm_array(response), dtype=np.float32)
            depth = depth.reshape(response.height, response.width)
            np.savetxt(os.path.normpath(os.path.join(fp + '.dep')),
                       depth)
            cv2.imwrite(os.path.normpath(os.path.join(fp + '.png')),
                        depth)
        else:
            if VERBOSE:
                print("Type %d, size %d" % (response.image_type,
                                            len(response.image_data_uint8)))
            airsim.write_file(os.path.normpath(os.path.join(fp + '.png')),
                              response.image_data_uint8)


def flip_mirror_img(img_file):
    """Overwrite an image with flip and mirror transformations.

    Args:
        img_file (str): path to input image
    """
    im = Image.open(img_file)
    im_mirror = ImageOps.mirror(ImageOps.flip(im))
    im_mirror.save(img_file)


def transform_cube_to_equi(cube_dir, equi_dir, width, height, ti,
                           cam_list, view=0):
    """Generate equirectangular images from cubemaps.

    Using Blender, this method outputs an equirectangular image of a specified
    scene cubemap view. If the selected view mode if set to Depth, also
    generates a depth map from the .dep files are more accurate than png depth
    because they are storing real values.

    Args:
        cube_dir (str): path to the directory containing the cubemap images
        equi_dir (str): output directory
        width (int): output width
        height (int): output height
        ti (int):  iteration index (id of the capture)
        cam_list (list[str]): list of camera names used for output file names
        view (int): id characterizing the scene view (0: RGB, 1: Depth,
                    2: Semantic Segmentation); defaults to RGB only
    """
    if platform in ("linux", "linux2"):
        if VERBOSE:
            print('Linux detected...\n',
                  (int)(os.popen('grep -c cores /proc/cpuinfo').read()))
        blender_exe = "blender"
    elif platform in ("win32", "win64"):
        if VERBOSE:
            print('Windows detected...')
        blender_exe = str(os.path.join("C:\\Program Files\\Blender Foundation"
                                       "\\Blender 2.92", "blender.exe"))

    depth_dir = cube_dir.split('/')[0] + '/'
    print('depth_dir: ', depth_dir)
    equi_dir = equi_dir + str(ti) + '_' + str(view)
    print('equi_dir: ', equi_dir)
    cube_dir = cube_dir + str(ti)
    print('cube_dir: ', cube_dir)
    img_list = [cube_dir + '_' + str(view) + '_' + i + '.png' for i in cam_list]
    print('img_list: ', img_list)
    if VERBOSE:
        print('cube_dir : {0}\nimg_list : {1}'.format(cube_dir, img_list))

    flip_mirror_img(img_list[3])
    flip_mirror_img(img_list[4])

    os.system("cube2sphere " + img_list[0] + " " + img_list[5] + " " +
              img_list[1] + " " + img_list[2] + " " + img_list[3] + " " +
              img_list[4] + ' -t 20 -f PNG -o ' + equi_dir + '_equi -b "' +
              blender_exe + '" -r ' + str(width) + ' ' + str(height))

    # If view mode is Depth, also generate depth map from .dep files
    if view == 1:
        dep_to_equi.create_dep_to_equi_v2(ti, depth_dir)


def capture_scene_full(ti, cube_dir, equi_dir, camera_list):
    """Capture and generate equirectangular images for all views.

    Args:
        ti (int):  iteration index (id of the capture)
        cube_dir (str): path to the directory containing the cubemap images
        equi_dir (str): output directory
        camera_list (list[str]): list of camera names used for output file names
    """
    t_get_cube = time.time()
    get_full_camera(cube_dir, camera_list)
    t_get_cube = time.time() - t_get_cube
    print("Cube in ", t_get_cube)

    for idx in range(3):
        t_cub2sph = time.time()
        transform_cube_to_equi(cube_dir, equi_dir, OUT_SHAPE[0], OUT_SHAPE[1],
                               ti, camera_list, view=idx)
        t_cub2sph = time.time() - t_cub2sph
        print("Cube2sphere in {0}s".format(t_cub2sph))


def capture_scene(ti, cube_dir, equi_dir, camera_list, loc_feature="Scene"):
    """Capture and generate equirectangular images for a specific view.

    By default, captures and generates equirectangular images for RGB views of
    the scene.

    Args:
        ti (int):  iteration index (id of the capture)
        cube_dir (str): path to the directory containing the cubemap images
        equi_dir (str): output directory
        camera_list (list[str]): list of camera names used for output file names
        loc_feature (str): scene view mode to capture (defaults to RGB)
    """
    t_get_cube = time.time()
    get_full_scene(cube_dir, camera_list, ti, loc_feature=loc_feature)
    t_get_cube = time.time() - t_get_cube
    print("Cube in {0}s".format(t_get_cube))

    t_cub2sph = time.time()
    transform_cube_to_equi(cube_dir, equi_dir, OUT_SHAPE[0], OUT_SHAPE[1],
                           ti, camera_list, view=0)
    t_cub2sph = time.time() - t_cub2sph
    print("Cube2sphere in {0}s".format(t_cub2sph))


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

    # client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(0, 0, 0),
    #                          airsim.to_quaternion(0, 0, 0)), True)
    # client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(0, 0, 0),
    #                          airsim.to_quaternion(0, 0, np.deg2rad(90))),
    #                          True)

    # SRC_DIR = os.path.join(tempfile.gettempdir(), "airsim_drone")
    cube_dir = SRC_DIR + '/CUBEMAPS/'
    equi_dir = SRC_DIR + '/EQUI/'
    pose_dir = SRC_DIR + '/POSE/'
    os.makedirs(cube_dir, exist_ok=True)
    os.makedirs(equi_dir, exist_ok=True)
    os.makedirs(pose_dir, exist_ok=True)

    print("Saving images to %s" % equi_dir)

    # Load pose from a previously saved manual path
    rec_pos = pd.read_csv('airsim_rec_pos.csv',
                          sep='\t')[['POS_X', 'POS_Y', 'POS_Z']]
    nb_case = 1  # rec_pos.shape[0]
    camera_list = ["front", "left", "right", "top", "bottom", "back"]
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

        yaw = 0
        roll = 0
        if ti == 0:
            pose = [ti, 0, 0, z, 0, 0, 0, 0]
        else:
            pose = [ti, x, y, z, yaw, pitch, roll,
                    client.simGetCollisionInfo().time_stamp]
        pose_list.append(pose)

        # client.moveByVelocity(vx, vy, vz, duration)
        client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(pose[1],
                                                             pose[2],
                                                             pose[3]),
                                             airsim.to_quaternion(pose[4],
                                                                  pose[5],
                                                                  pose[6])),
                                 True)
        # Capture from 1 camera that rotates
        if METHOD == 'single_cam':
            get_cubemap_single(ti, cube_dir)

        # Capture from 6 fixed cameras
        elif METHOD == 'multi_cam':
            # capture_scene_full(ti, cube_dir, equi_dir, camera_list)
            # capture_scene(ti, cube_dir, equi_dir, camera_list,
            #               loc_feature="scene")
            # print(client.simGetCollisionInfo().time_stamp)
            print('Not implemented yet !')
        else:
            print('Unknown method. Terminating...')
            break

    if METHOD == 'single_cam':
        np.savetxt(pose_dir+'pose_list.txt', pose_list)
        client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(0, 0, 0),
                                             airsim.to_quaternion(0, 0, 0)),
                                 True)

        t_cub2sph = time.time()
        if VIEW == -1:
            transform_cube_to_equi(cube_dir, equi_dir, OUT_SHAPE[0],
                                   OUT_SHAPE[1], ti, camera_list, view=0)
            transform_cube_to_equi(cube_dir, equi_dir, OUT_SHAPE[0],
                                   OUT_SHAPE[1], ti, camera_list, view=1)
            transform_cube_to_equi(cube_dir, equi_dir, OUT_SHAPE[0],
                                   OUT_SHAPE[1], ti, camera_list, view=2)
        else:
            transform_cube_to_equi(cube_dir, equi_dir, OUT_SHAPE[0],
                                   OUT_SHAPE[1], ti, camera_list, view=VIEW)
        t_cub2sph = time.time() - t_cub2sph
        print("Cube2sphere in {0}s".format(t_cub2sph))


if __name__ == '__main__':
    args = PARSER.parse_args()
    SRC_DIR = args.source
    METHOD = args.method
    OUT_SHAPE = args.shape
    VERBOSE = args.verbose is not None
    VIEW = args.view
    client = airsim.VehicleClient()
    main()
