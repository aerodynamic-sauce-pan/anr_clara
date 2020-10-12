import cv2,os
import numpy as np
import matplotlib.pyplot as plt


def get_img(input_Path):
    img_paths = []
    for (path, dirs, files) in os.walk(input_Path):
        for filename in files:
            if filename.endswith(('.jpg','.png')):
                img_paths.append(path+'/'+filename)
    return img_paths,filename[:-3]


#构建Gabor滤波器
def build_filters():
     filters = []
     ksize = [40,50,60,70,80,90] # gabor尺度，6个
     lamda = 20         # 波长
     for theta in np.arange(0, np.pi, np.pi / 4): #gabor方向，0°，45°，90°，135°，共四个
         for K in range(len(ksize)):
             kern = cv2.getGaborKernel((ksize[K], ksize[K]), 10, theta, lamda, 0.5, 0, ktype=cv2.CV_32F)
             kern /= 1.5*kern.sum()
             filters.append(kern)
     plt.figure(1)

     #用于绘制滤波器
     for temp in range(len(filters)):
         plt.subplot(4, len(ksize), temp + 1)
         plt.imshow(filters[temp])
     plt.show()
     return filters

#Gabor特征提取
def getGabor(filename,img,filters):
    res = [] #滤波结果
    for j in range(len(filters)):
        # res1 = process(img, filters[i])
        accum = np.zeros_like(img)
        for kern in filters[j]:
            fimg = cv2.filter2D(img, cv2.CV_8UC1, kern)
            accum = np.maximum(accum, fimg, accum)
        res.append(np.asarray(accum))
   
    #用于绘制滤波效果
    plt.figure(2)
    for temp in range(len(res)):
        plt.subplot(4,6,temp+1)
        plt.imshow(res[temp], cmap='gray' )
    plt.show()
    cv2.imshow(filename,res[12])
    cv2.waitKey(0)
    cv2.imshow(filename,res[13])
    cv2.waitKey(0)
    cv2.imshow(filename,res[14])
    cv2.waitKey(0)
    cv2.imshow(filename,res[15])
    cv2.waitKey(0)
    cv2.imshow(filename,res[16])
    cv2.waitKey(0)
    cv2.imshow(filename,res[17])
    cv2.waitKey(0)
    return res  #返回滤波结果,结果为24幅图，按照gabor角度排列


if __name__ == '__main__':
    input_Path = 'E:\\UE_4.16\\Engine\\Binaries\\Win64\\TrainImages_L\\' 
    filters = build_filters()
    img_paths,filename = get_img(input_Path)
    i=0
    for img in img_paths:
        i = i+1
        img = cv2.imread(img)
        getGabor(filename, img, filters)
