import setup_path 
import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2
import time 

from cube2sphere import cube2sphere
from sys import platform

def get_single_camera(camera_name,ti,cube_dir):
    responses = client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene)
            ])
    write_responses(responses,cube_dir,camera_name,ti)

def get_single_camera_full(camera_name,ti,cube_dir):
    responses = client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene),
            airsim.ImageRequest("0", airsim.ImageType.DepthPerspective, True, False),
            airsim.ImageRequest("0", airsim.ImageType.Segmentation)
            ])
    write_responses(responses,cube_dir,camera_name,ti)

def get_full_camera(cube_dir,camera_list,cam_num):
    responses = client.simGetImages([
            # airsim.ImageRequest("0", airsim.ImageType.Scene),
            # airsim.ImageRequest("0", airsim.ImageType.DepthPerspective, True, False),
            # airsim.ImageRequest("0", airsim.ImageType.Segmentation)
            airsim.ImageRequest("0", 0),
            airsim.ImageRequest("0", 2, True, False),
            airsim.ImageRequest("0", 5)
        ])
    write_full_responses(responses,cube_dir,camera_list,cam_num)

def write_responses(responses,cube_dir,camera_name,ti):
    for i, response in enumerate(responses):
        if response.pixels_as_float:
            print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
            depth = np.array(airsim.get_pfm_array(response), dtype=np.float32)
            depth = depth.reshape(response.height, response.width)
            np.savetxt(os.path.normpath(os.path.join(cube_dir, str(i) + '_' + camera_name + '.dep')), depth)
            cv2.imwrite(os.path.normpath(os.path.join(cube_dir, str(i) + '_' + camera_name + '.png')), depth)
        else:
            print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            airsim.write_file(os.path.normpath(os.path.join(cube_dir, str(i) + '_' + camera_name + '.png')), response.image_data_uint8)

def write_full_responses(responses,cube_dir,camera_list,cam_num):
    for i, response in enumerate(responses):
        # print(os.path.join(cube_dir, str(ti) + '_' + str(i%3) + '_' + camera_list[int(i/3)] + '.png'))
        if response.pixels_as_float:
            # print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
            depth = np.array(airsim.get_pfm_array(response), dtype=np.float32)
            depth = depth.reshape(response.height, response.width)
            # np.savetxt(os.path.normpath(os.path.join(cube_dir, str(i%3) + '_' + camera_list[cam_num] + '.dep')), depth)
            cv2.imwrite(os.path.normpath(os.path.join(cube_dir, str(i%3) + '_' + camera_list[cam_num] + '.png')), depth)
        else:
            # print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            airsim.write_file(os.path.normpath(os.path.join(cube_dir, str(i%3) + '_' + camera_list[cam_num] + '.png')), response.image_data_uint8)
           

def get_cubemap_single(ti,cube_dir,loc_feature,camera_list):
    angle90 = np.deg2rad(90)
    z=-1
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, z), airsim.to_quaternion(0, 0, 0))
    client.simSetCameraPose(0, camera_pose)
    get_single_camera("front",ti,cube_dir)
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, z), airsim.to_quaternion(0, 0, angle90))  #PRY in radians
    client.simSetCameraPose(0, camera_pose)
    get_single_camera("right",ti,cube_dir)
#    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0, 0, 0))
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, z), airsim.to_quaternion(0, 0, -angle90))  #PRY in radians
    client.simSetCameraPose(0, camera_pose)
    get_single_camera("left",ti,cube_dir)
#    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0, 0, 0))
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, z), airsim.to_quaternion(angle90, 0, 0))  #PRY in radians
    client.simSetCameraPose(0, camera_pose)
    get_single_camera("top",ti,cube_dir)
#    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0, 0, 0))
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, z), airsim.to_quaternion(-angle90, 0, 0))  #PRY in radians
    client.simSetCameraPose(0, camera_pose)
    get_single_camera("bottom",ti,cube_dir)
#    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0, 0, 0))
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, z), airsim.to_quaternion(0, 0, -2*angle90))  #PRY in radians
    client.simSetCameraPose(0, camera_pose)
    get_single_camera("back",ti,cube_dir)

camera_list = ["front","left","right","top","bottom","back"]

def get_cubemap_multiple(ti,cube_dir,camera_list,z):
    angle90 = np.deg2rad(90)
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, z), airsim.to_quaternion(0, 0, 0))
    client.simSetCameraPose(0, camera_pose)
    get_full_camera(cube_dir,camera_list,0)
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, z), airsim.to_quaternion(0, 0, angle90))  #PRY in radians
    client.simSetCameraPose(0, camera_pose)
    get_full_camera(cube_dir,camera_list,2)
#    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0, 0, 0))
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, z), airsim.to_quaternion(0, 0, -angle90))  #PRY in radians
    client.simSetCameraPose(0, camera_pose)
    get_full_camera(cube_dir,camera_list,1)
#    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0, 0, 0))
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, z), airsim.to_quaternion(angle90, 0, 0))  #PRY in radians
    client.simSetCameraPose(0, camera_pose)
    get_full_camera(cube_dir,camera_list,3)
#    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0, 0, 0))
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, z), airsim.to_quaternion(-angle90, 0, 0))  #PRY in radians
    client.simSetCameraPose(0, camera_pose)
    get_full_camera(cube_dir,camera_list,4)
#    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0, 0, 0))
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, z), airsim.to_quaternion(0, 0, -2*angle90))  #PRY in radians
    client.simSetCameraPose(0, camera_pose)
    get_full_camera(cube_dir,camera_list,5)

from PIL import Image, ImageOps
def flip_mirror_img(img_file):
    im = Image.open(img_file)
    im_mirror = ImageOps.mirror(ImageOps.flip(im))
    im_mirror.save(img_file)    

def transform_cube_to_equi(cube_dir, equi_dir, idx, width, height, ti, camera_list):
    if platform == "linux" or platform == "linux2":
        blender_exe = "blender"
        #print((int)(os.popen('grep -c cores /proc/cpuinfo').read()))
    elif platform == "win32" or platform == "win64":
            blender_exe = str(os.path.join("C:\Program Files\Blender Foundation\Blender 2.92","blender.exe"))
    equi_dir = equi_dir + str(ti) + '_' + str(idx)
    cube_dir = cube_dir + str(ti) + '_' + str(idx)
    cam_list = [cube_dir + '_' + i +'.png' for i in camera_list]
    # print(cam_list)
    
    flip_mirror_img(cam_list[3])
    flip_mirror_img(cam_list[4])
    os.system("cube2sphere "+cam_list[0]+" "+cam_list[5]+" "+cam_list[1]+" "+cam_list[2]+" "+cam_list[3]+" "+cam_list[4]+' -t 10 -f PNG -o '+equi_dir+'_equi -b "'+blender_exe+'" -r '+str(width)+' '+str(height))

def transform_cube_to_equi_v2(cube_dir, equi_dir, idx, width, height, ti, camera_list):
    if platform == "linux" or platform == "linux2":
        blender_exe = "blender"
        #print((int)(os.popen('grep -c cores /proc/cpuinfo').read()))
    elif platform == "win32" or platform == "win64":
            blender_exe = str(os.path.join("C:\Program Files\Blender Foundation\Blender 2.92","blender.exe"))
    equi_dir = equi_dir + str(ti) + '_' + str(idx)
    cube_dir = cube_dir + str(idx)
    cam_list = [cube_dir + '_' + i +'.png' for i in camera_list]
    # print(cam_list)
    
    flip_mirror_img(cam_list[3])
    flip_mirror_img(cam_list[4])
    os.system("cube2sphere "+cam_list[0]+" "+cam_list[5]+" "+cam_list[1]+" "+cam_list[2]+" "+cam_list[3]+" "+cam_list[4]+' -t 10 -f PNG -o '+equi_dir+'_equi -b "'+blender_exe+'" -r '+str(width)+' '+str(height))


def capture_scene(ti,cube_dir,equi_dir,camera_list):
    t_get_cube = time.time()
    get_cubemap_single(ti,cube_dir,camera_list)
    t_get_cube = time.time() - t_get_cube
    print("Cube in ",t_get_cube)
    
    t_cub2sph = time.time()
    transform_cube_to_equi(cube_dir, equi_dir, 0, 1000, 500, ti, camera_list)
    t_cub2sph = time.time() - t_cub2sph
    print("Cube2sphere in ",t_cub2sph)

def capture_scene_full(ti,cube_dir,equi_dir,camera_list):
    t_get_cube = time.time()
    get_cubemap_multiple(ti,cube_dir,camera_list,-1)
    t_get_cube = time.time() - t_get_cube
    print("Cube in ",t_get_cube)
    
    for idx in range(3):
        t_cub2sph = time.time()
        transform_cube_to_equi_v2(cube_dir, equi_dir, idx, 1000, 500, ti, camera_list)
        t_cub2sph = time.time() - t_cub2sph
        print("Cube2sphere in ",t_cub2sph)

tmp_dir = "./OUTPUT/"
#tmp_dir = os.path.join(tempfile.gettempdir(), "airsim_drone")

case_name = "FOREST_200"
cube_dir = os.path.join(tmp_dir,case_name) + '/CUBEMAPS/'
equi_dir = os.path.join(tmp_dir,case_name) + '/EQUI/'
os.makedirs(cube_dir, exist_ok=True)
os.makedirs(equi_dir, exist_ok=True)

print ("Saving images to %s" % equi_dir)

camera_list = ["front","left","right","top","bottom","back"]

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

airsim.wait_key('Press any key to takeoff')
# client.takeoffAsync().join()

Tsim0 = client.getMultirotorState().timestamp

print(client.getMultirotorState())

alt=-2
tfin_sim=10
position0 = airsim.Vector3r(0 , 0, alt)
heading0 = airsim.utils.to_quaternion(0, 0, 0)
pose0 = airsim.Pose(position0, heading0)
client.simSetVehiclePose(pose0, True)
client.hoverAsync().join()
client.simPause(True)
time.sleep(2)
client.simPause(False)

# state = client.getMultirotorState()
# print("state: %s" % pprint.pformat(state))

# # airsim.wait_key('Press any key to move vehicle ')
# client.moveToPositionAsync(0, 0, -1, 1).join()
# client.hoverAsync().join()

Tcollision0 = client.simGetCollisionInfo().time_stamp

v=5
vx=1
vy=0.2
vz=0

duration=1
time_global=0

while Tcollision0 == client.simGetCollisionInfo().time_stamp and time_global!=tfin_sim:
    print("Moving")
    client.simPause(True)
    #capture_scene(time_global,cube_dir,equi_dir,camera_list)
    capture_scene_full(time_global,cube_dir,equi_dir,camera_list)
    client.simPause(False)
    client.moveByVelocityZAsync(vx*v, vy*v, alt, duration, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False, 0)).join()
    time_global += duration
    # client.hoverAsync().join()

# client.simPause(True)
# capture_scene(time_global,cube_dir,equi_dir,camera_list)
# client.simPause(False)

Tcollision1 = client.simGetCollisionInfo().time_stamp
if Tcollision1 != Tcollision0:
    print("Collision with ",client.simGetCollisionInfo().object_name,' at ',(Tcollision1-Tsim0)//pow(10,9))

print("Going Back To Start")

client.armDisarm(False)
client.reset()

# that's enough fun for now. let's quit cleanly
client.enableApiControl(False)
