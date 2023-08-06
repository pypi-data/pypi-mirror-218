import cv2
from pylab import *
import pyzjr.TrackBar as Trace
import pyzjr.Z as Z

from skimage.morphology import skeletonize
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray

def repairImg(img,r=5,flags=Z.repair_NS,mode=0):
    """
    * 用于修复图像
    :param img: 输入图像
    :param r: 修复半径，即掩膜的像素周围需要参考的区域半径
    :param flags: 修复算法的标志,有Z.repair_NS、Z.repair_TELEA,默认为Z.repair_NS
    :param mode: 是否采用HSV例模式,默认为0,自定义模式,可通过Color下的TrackBar文件中获得
    :return: 返回修复后的图片
    """
    hsvvals = Trace.HSV(mode)
    tr=Trace.getMask()
    if hsvvals == 0:
        hmin, smin, vmin, hmax, smax, vmax = map(int, input().split(','))
        hsvval=[[hmin, smin, vmin],[hmax, smax, vmax]]
        imgResult, mask, imgHSV = tr.MaskZone(img, hsvval)
        dst = cv2.inpaint(img, mask, r, flags)
        return dst
    else:
        imgResult, mask, imgHSV = tr.MaskZone(img, hsvvals)
        dst = cv2.inpaint(img, mask, r, flags)
        return dst
    
def labelpoint(im, click=4):
    """
    交互式标注
    :param im: 图像,采用im = Image.open(?)的方式打开，颜色空间才是正常的
    :param click: 点击次数、默认为4
    :return: 返回点的坐标
    """
    imshow(im)
    print(f'please click {click} points')
    x=ginput(click)
    print('you clicked:',x)
    return x


def transImg(img,targetW,targetH):
    """
    标注方式按照先上后下，先左后右的顺序
    :param img: 图像
    :param targetW: 已知目标物体的宽度
    :param targetH: 已知目标物体的长度
    :return: 修正后的图像
    """
    width, height = targetW, targetH
    pts1 = np.float32(labelpoint(img))
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (width, height))
    return imgOutput


def ske_information(crack):
    """
    获取骨架图的信息
    :param crack: 目标图
    :return: 骨架图与一个数组，其中每一行表示一个非零元素的索引(y,x)，包括行索引和列索引
    """
    gray = rgb2gray(crack)
    thresh = threshold_otsu(gray)
    binary = gray > thresh
    skeimage = skeletonize(binary)
    skepoints = np.argwhere(skeimage)
    return skeimage, skepoints