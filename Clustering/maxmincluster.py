import os
import math
import numpy as np
import cv2

test_depth_result_dir = "DenseDepth/images/test_synthetic"
filtertrunkdir = "TestImages/filtertrunk_tlarcher"
cluster_trunk_dir = "TestImages/clustertrunk_tlarcher"

def calcuDistance(imagenum, data1, data2):
    '''
    计算两个模式样本之间的欧式距离
    Calculate the Euclidean distance between two model samples
    :param data1:
    :param data2:
    :return:
    '''
    image = cv2.imread(os.path.join(test_depth_result_dir, imagenum))
    distance = 0.7 * pow((image[data1[0],data1[1],0] - image[data2[0],data2[1],0]), 2) + 0.3*pow((data1[1]-data2[1]),2)
    return math.sqrt(distance)
 
def maxmin_distance_cluster(file, data, Theta):
    '''
    :param data: 输入样本数据,每行一个特征
    :param Theta:阈值，一般设置为0.5，阈值越小聚类中心越多
    :return:样本分类，聚类中心
    '''
    maxDistance = 0
    start = 0#初始选一个中心点
    index = start#相当于指针指示新中心点的位置
    k = 0 #中心点计数，也即是类别
 
    dataNum=len(data)
    distance=np.zeros((dataNum,))
    minDistance=np.zeros((dataNum,))
    classes =np.zeros((dataNum,))
    centerIndex=[index]
 
    # 初始选择第一个为聚类中心点
    ptrCen=data[dataNum//10]
    # 寻找第二个聚类中心，即与第一个聚类中心最大距离的样本点
    for i in range(dataNum):
        ptr1 =data[i]
        d=calcuDistance(file, ptr1,ptrCen)
        distance[i] = d
        classes[i] = k + 1
        if (maxDistance < d):
            maxDistance = d
            index = i #与第一个聚类中心距离最大的样本
 
    minDistance=distance.copy()
    maxVal = maxDistance
    while maxVal > (maxDistance * Theta):
        k = k + 1
        centerIndex+=[index] #新的聚类中心
        for i in range(dataNum):
            ptr1 = data[i]
            ptrCen=data[centerIndex[k]]
            d = calcuDistance(file, ptr1, ptrCen)
            distance[i] = d
            #按照当前最近临方式分类，哪个近就分哪个类别
            if minDistance[i] > distance[i]:
                minDistance[i] = distance[i]
                classes[i] = k + 1
        # 寻找minDistance中的最大距离，若maxVal > (maxDistance * Theta)，则说明存在下一个聚类中心
        index=np.argmax(minDistance)
        maxVal=minDistance[index]
    return classes,centerIndex
 
if __name__=='__main__':
    dirs = os.listdir(filtertrunkdir)
    print('dirs : ', dirs)
    for file in dirs:
        print('file : ', file)
        image = cv2.imread(os.path.join(filtertrunkdir, file))
        data = []
        for i in range(image.shape[0]):
            for j  in range(image.shape[1]):
                if image[i,j,0] < 128:
                    data.append([i,j])
        Theta = 0.55
        classes,centerIndex = maxmin_distance_cluster(file, data, Theta)
        colorpalette = [[0,0,0],[255,255,255],[255,0,0],[0,255,0],[0,0,255],\
                        [255,255,0],[255,0,255],[0,255,255],[128,0,0],[0,128,0],\
                        [0,0,128],[128,128,0],[128,0,128],[0,128,128],[128,128,128],\
                        [128,255,0],[255,128,0],[0,128,255],[0,255,128],[128,0,255],\
                        [255,0,128],[128,255,255],[255,128,255],[255,255,128],[128,128,255],\
                        [128,255,128],[255,128,128],[64,0,0],[0,64,0],[0,0,64],\
                        [64,64,0],[0,64,64],[64,0,64],[64,255,255],[255,64,255],\
                        [255,255,64],[64,64,255],[255,64,64],[64,255,64],[64,64,64],\
                        [0,64,255],[64,0,255],[64,255,0],[0,255,64],[255,0,64],\
                        [255,64,0]]
        print(classes)
        print(centerIndex)
        for i in range(len(data)):
            image[data[i][0],data[i][1]] = colorpalette[int(classes[i])]
            
        cv2.imshow(file,image)
        cv2.imwrite(os.path.join(cluster_trunk_dir, file),image)
        cv2.waitKey(0)
