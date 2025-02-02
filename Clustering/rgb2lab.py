import numpy as np, math
import cv2
import os


# region 辅助函数
# RGB2XYZ空间的系数矩阵
M = np.array([[0.412453, 0.357580, 0.180423],
              [0.212671, 0.715160, 0.072169],
              [0.019334, 0.119193, 0.950227]])


# im_channel取值范围：[0,1]
def _f(im_channel):
    if im_channel > 0.008856:       
        return np.power(im_channel, 1 / 3)  
    else: 
        return 7.787 * im_channel + 0.137931


def anti_f(im_channel):
    return np.power(im_channel, 3) if im_channel > 0.206893 else (im_channel - 0.137931) / 7.787
# endregion


# region RGB 转 Lab
# 像素值RGB转XYZ空间，pixel格式:(B,G,R)
# 返回XYZ空间下的值
def __rgb2xyz__(pixel):
    b, g, r = pixel[0], pixel[1], pixel[2]
    rgb = np.array([r, g, b])
    # rgb = rgb / 255.0
    # RGB = np.array([gamma(c) for c in rgb])
    XYZ = np.dot(M, rgb.T)
    XYZ = XYZ / 255.0
    return (XYZ[0] / 0.95047, XYZ[1] / 1.0, XYZ[2] / 1.08883)


def __xyz2lab__(xyz):
    """
    XYZ空间转Lab空间
    :param xyz: 像素xyz空间下的值
    :return: 返回Lab空间下的值
    """
    #F_XYZ = [f(x) for x in xyz]
    if xyz[1] > 0.008856:
        L = 116 * _f(xyz[0]) - 16  
    else:
        L = 903.3 * xyz[1]
    a = 500 * (_f(xyz[0]) - _f(xyz[1]))
    b = 200 * (_f(xyz[1]) - _f(xyz[2]))
    return (L, a, b)


def RGB2Lab(pixel):
    """
    RGB空间转Lab空间
    :param pixel: RGB空间像素值，格式：[G,B,R]
    :return: 返回Lab空间下的值
    """
    xyz = __rgb2xyz__(pixel)
    Lab = __xyz2lab__(xyz)
    return Lab


# endregion

# region Lab 转 RGB
def __lab2xyz__(Lab):
    fY = (Lab[0] + 16.0) / 116.0
    fX = Lab[1] / 500.0 + fY
    fZ = fY - Lab[2] / 200.0

    x = anti_f(fX)
    y = anti_f(fY)
    z = anti_f(fZ)

    x = x * 0.95047
    y = y * 1.0
    z = z * 1.0883

    return (x, y, z)


def __xyz2rgb(xyz):
    xyz = np.array(xyz)
    xyz = xyz * 255
    rgb = np.dot(np.linalg.inv(M), xyz.T)
    # rgb = rgb * 255
    rgb = np.uint8(np.clip(rgb, 0, 255))
    return rgb


def Lab2RGB(Lab):
    xyz = __lab2xyz__(Lab)
    rgb = __xyz2rgb(xyz)
    return rgb
# endregion
'''
if __name__ == '__main__':
    img = cv2.imread(r'E:\code\collor_recorrect\test_1.jpg')
    w = img.shape[0]
    h = img.shape[1]
    img_new = np.zeros((w,h,3))
    lab = np.zeros((w,h,3))
    for i in range(w):
        for j in range(h):
            Lab = RGB2Lab(img[i,j])
            lab[i, j] = (Lab[0], Lab[1], Lab[2])

    for i in range(w):
        for j in range(h):
            rgb = Lab2RGB(lab[i,j])
            img_new[i, j] = (rgb[2], rgb[1], rgb[0])

	cv2.imwrite(r'E:\code\collor_recorrect\test.jpg', img_new)
'''
def gaussian_mle(data):                                                                                                                                                                               
    mu = data.mean(axis=0)                                                                                                                                                                            
    var = ((data-mu)*(data-mu)).sum(axis=0) / data.shape[0] #  this is slightly suboptimal, but instructive

    return mu, var 
'''
trunk = cv2.imread("trunk2.PNG")
with open('TrunkColor.txt','a') as f:
    for i in range(trunk.shape[0]//10):
        for j in range(trunk.shape[1]//10):
            f.write('\n')
            f.write(str(trunk[10*i,10*j,2])+' '+str(trunk[10*i,10*j,1])+' '+str(trunk[10*i,10*j,0]))
'''
TrunkLab = []
with open('TrunkColor.txt') as f:
    line = f.readline()
    while line:
        color = line.split(' ')
        Lab = RGB2Lab([float(color[2]), float(color[1]), float(color[0])])
        #HSV = cv2.cvtColor(np.array([color(2),color[1],color(0)],dtype = np.uint8), cv2.COLOR_BGR2HSV)
        print(Lab)
        #print(HSV)
        TrunkLab.append(Lab)
        line = f.readline()
TrunkLab = np.array(TrunkLab,dtype=np.float)

mu, var = gaussian_mle(TrunkLab)
print(mu)
print(var)

#rgbdir = 'E:\\UE_4.16\\Engine\\Binaries\\Win64\\TrainImages_L\\'
rgbdir = "F:\\ZHD\\TN10\\mytrain\\TestImages\\clip"  
filtertrunkdir = "F:\\ZHD\\TN10\\mytrain\\TestImages\\filtertrunk"      
for img_name in os.listdir(rgbdir):
    if os.path.splitext(img_name)[1] == '.png':  
    #if img_name == '1.png':
        img = cv2.imread(os.path.join(rgbdir, img_name))
        '''
        imghsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        ret,th1 = cv2.threshold(imghsv[:,:,0],0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
        ret,th2 = cv2.threshold(imghsv[:,:,1],0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
        ret,th3 = cv2.threshold(imghsv[:,:,2],0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
        cv2.imshow(img_name[0],th1)
        cv2.waitKey(0)
        cv2.imshow(img_name[0],th2)
        cv2.waitKey(0)
        cv2.imshow(img_name[0],th3)
        cv2.waitKey(0)
        '''
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
        #img = cv2.erode(img,kernel)
        #img = cv2.GaussianBlur(img,(5,5),0)
        #img = cv2.bilateralFilter(img, 0, 100, 5)
        #img = cv2.cvtColor(img,cv2.COLOR_BGR2LAB)
        w = img.shape[0]
        h = img.shape[1]
        #img_new = np.zeros((w,h,3),np.uint8)
        for i in range(w):
            for j in range(h):
                Lab = RGB2Lab(img[i,j])
                #Lab = img[i,j]
                #print(Lab)
                Disa = (Lab[1] - mu[1])*(Lab[1]-mu[1])/var[1]
                Disb = (Lab[2] - mu[2])*(Lab[2]-mu[2])/var[2]
                Dis = 0.1*math.exp(Disa)*math.exp(Disb)
                #Dis = Disa+Disb
                if Dis>255:
                    Dis=255
                img[i, j] = [Dis, Dis, Dis]
                
                #else:
                    #img[i, j] = [0, 0, 0]
        
        '''
        x=cv2.Sobel(img,cv2.CV_16S,1,0)
        y=cv2.Sobel(img,cv2.CV_16S,0,1)
        absx=cv2.convertScaleAbs(x)
        absy=cv2.convertScaleAbs(y)
        img=cv2.addWeighted(absx,1,absy,0,0)
        '''
        
        GrayImage=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #图片灰度化处理

        ret,binary = cv2.threshold(GrayImage,128,255,cv2.THRESH_BINARY_INV) #图片二值化,灰度值大于40赋值255，反之0

        threshold = h/40 * w/40   #设定阈值

        #cv2.fingContours寻找图片轮廓信息
        """提取二值化后图片中的轮廓信息 ，返回值contours存储的即是图片中的轮廓信息，是一个向量，内每个元素保存
        了一组由连续的Point点构成的点的集合的向量，每一组Point点集就是一个轮廓，有多少轮廓，向量contours就有
        多少元素"""
        contours,hierarch=cv2.findContours(binary,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

        for i in range(len(contours)):
            area = cv2.contourArea(contours[i]) #计算轮廓所占面积
            if area < threshold:                         #将area小于阈值区域填充背景色，由于OpenCV读出的是BGR值
                cv2.drawContours(img,[contours[i]],-1, (255,255,255), thickness=-1)     #原始图片背景BGR值(84,1,68)
                continue
        cv2.imshow(img_name[0],img)
        cv2.imwrite(os.path.join(filtertrunkdir,img_name),img)
        cv2.waitKey(0)

