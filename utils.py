import numpy as np 
import cv2
from PIL import Image
import os
import json
import netCDF4
from netCDF4 import Dataset
from config_af import config_dict

def resize(src, dstsize):
    dst = np.zeros(dstsize)
    fac = src.shape[0]/float(dstsize[0])
    for i in range(dstsize[0]):
        for j in range(dstsize[1]):
            y = float(i)*fac
            x = float(j)*fac
            if y+1 > src.shape[0]:
                y-=1
            if x+1 > src.shape[1]:
                x-=1
            cy = np.ceil(y)
            fy = cy -1
            cx = np.ceil(x)
            fx=cx-1
            w1=(cx-x)*(cy-y)
            w2=(x-fx)*(cy-y)
            w3=(cx-x)*(y-fy)
            w4=(x-fx)*(y-fy)
            if (x-np.floor(x)>1e-6 or y-np.floor(y)>1e-6):
                fy, fx, cx, cy = int(fy), int(fx), int(cx), int(cy)
                t=src[fy][fx]*w1+src[fy][cx]*w2+src[cy][fx]*w3+src[cy][cx]*w4
                dst[i][j]=t
            else:
                dst[i][j]=src[int(y)][int(x)]
    return dst

def plot(data, image_name):
    data_shape = data.shape
    fig = Image.new(mode='RGBA', size=(data_shape[0],data_shape[1]), color='white')
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data[i][j] <= 5:
                fig.putpixel((i, j), (255, 255, 255,0))
            elif data[i][j] <= 10 and data[i][j] >5:
                fig.putpixel((i, j), (122, 114, 238))
            elif data[i][j] <= 15 and data[i][j] > 10:
                fig.putpixel((i, j), (30, 38, 208))
            elif data[i][j] <= 20 and data[i][j] > 15:
                fig.putpixel((i, j), (166, 252, 168))
            elif data[i][j] <= 25 and data[i][j] > 20:
                fig.putpixel((i, j), (0, 234, 0))
            elif data[i][j] <= 30 and data[i][j] > 25:
                fig.putpixel((i, j), (16, 146, 26))
            elif data[i][j] <= 35 and data[i][j] > 30:
                fig.putpixel((i, j), (252, 244, 100))
            elif data[i][j] <= 40 and data[i][j] > 35:
                fig.putpixel((i, j), (200, 200, 2))
            elif data[i][j] <= 45 and data[i][j] > 40:
                fig.putpixel((i, j), (144, 144, 0))
            elif data[i][j] <= 50 and data[i][j] > 45:
                fig.putpixel((i, j), (254, 172, 172))
            elif data[i][j] <= 55 and data[i][j] > 50:
                fig.putpixel((i, j), (254, 100, 92))
            elif data[i][j] <= 60 and data[i][j] > 55:
                fig.putpixel((i, j), (238, 2, 48))
            elif data[i][j] <= 65 and data[i][j] > 60:
                fig.putpixel((i, j), (212, 142, 254))
            elif data[i][j] > 65:
                fig.putpixel((i, j), (170, 36, 250))
            else:
                continue
    fig = fig.rotate(90)
    fig.save(image_name, 'PNG')

def read_json(path,pixel):
    '''
    # 注意path是通过构建好的路径(读取固定格式的json文件)
    '''
    try:
        with open(path,'r') as f:
            temp = json.loads(f.read())
            data_radar = np.array(temp[0]['data']).reshape(pixel)
    except OSError:
        print('the file open fail')
    return data_radar

def read_nc(target, path, pixel):
    '''
    需要构建路径，读取数值预报nc数据,并存其中获取对应（风速，降雨量）数据。
    '''
    nc_object = Dataset(path, target)
    keys = nc_object.variables.keys()
    if target in keys:
        tar = nc_object.variables[target][:]
    else:
        print('the target not in file')
    if len(tar.shape) == 3:
        tar_index = tar[0,:,:]
    elif len(tar.shape) == 2:
        tar_index = tar[:,:]
    elif len(tar.shape) == 4:
        tar_index = tar[0,0,:,:]
    else:
        print('the target data is not mix data')
    tar_reshape = resize(tar_index,pixel)
    return tar_reshape

def read_affine_picture(affine_image_path):
    '''
    功能是读取仿射的结果
    '''
    picture = plt.imread(affine_image_path)[:,:,:3]
    print('这是直接读入的显示')
    print('读取仿射变换后的图像shape:',picture.shape)
    picture_ys = np.zeros(self.pixel, dtype=float)
    for i in range(self.pixel[0]):
        for j in range(self.pixel[1]):
            if list(picture[i,j,:]) == [1,0,1]:
                picture_ys[i,j] = 52.
            elif list(picture[i,j,:]) == [1,0,0]:
                picture_ys[i,j] = 42.
            elif list(picture[i,j,:]) == [1,1,0]:
                picture_ys[i,j] = 32.  
            else:
                picture_ys[i,j] = 0.
    print('这是像素值映射后的图，三维')
    return picture_ys[::-1,:]

