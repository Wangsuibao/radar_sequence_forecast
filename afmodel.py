import numpy as np 
import matplotlib.pyplot as plt 
import json
import netCDF4
from netCDF4 import Dataset
import scipy.ndimage
from matplotlib import colors
import matplotlib.pylab as pb
from PIL import Image
import cv2
import time

from utils import *
from config_af import arg_dict
from affine_model import AffineModel

class RadarWindAffine(object):
    '''
    每一个时刻，都需要从新实例化一次类，用于更新类的信息
    '''
    def __init__(self,arg_dict,real_time):
        self.real_time = real_time  # 需要更新,这个不能实时的传入。
        # 这个时间更新是在调用类的外边

        self.stg_X = arg_dict['stg_X']
        self.stg_Y = arg_dict['stg_Y']
        self.pixel = arg_dict['pixel']
        self.interval = arg_dict['interval']  # 间隔
        self.duration = arg_dict['duration']  # 区间
        self.colors_sys = arg_dict['colors_sys']
        self.radar_sys = arg_dict['radar_sys']

        self.radar_path = arg_dict['radar_path']
        self.meteo_path = arg_dict['meteo_path']
        self.save_affine_path = arg_dict['save_affine_path']
        self.save_mix_path = arg_dict['save_mix_path']

    def read_json_data(self, ptime):
        path_json = self.radar_path + self.real_time + ptime + '.json'
        json_data = read_json(path_json, self.pixel)
        return json_data

    def read_nc_data(self, target, ptime):
        path_nc = self.meteo_path + self.real_time + ptime + '.nc'
        nc_data = read_nc(target, path_nc, self.pixel)
        return nc_data

    def dtr2time(self,str_time):
        time = str_time.strftime('%Y%m%d%H%M')
        return time

    def time2str(self, time):
        str = datetime.strptime(time,'%Y%m%d%H%M')
        return str

    def timesum(self, time, minute):
        ztime = time + datetime.timedelta(minutes=minute)
        return ztime
    

    def wind_radar_affine(self):
        '''
        功能是生成仿射，并保存。
        把函数直接当属性用的方法：
        '''
        x = np.round(np.linspace(self.stg_X[0],self.stg_X[1],self.pixel[0]),4)
        y = np.round(np.linspace(self.stg_Y[0],self.stg_Y[1],self.pixel[1]),4)
        [X,Y] = np.meshgrid(x,y)

        # 得把时间传进来
        start_time = self.real_time
        end_time = self.real_time + self.duration
        self.time_split = 3  # (end_time - start_time)/self.interval

        for i in range(self.time_split):
            ptime = self.real_time + (i+1)*interval
            Z = self.read_json_data(self.real_time)  # 只读取此刻真实的radar.
            feng_x = self.read_nc_data('U', ptime)
            feng_y = self.read_nc_data('V', ptime)

            model = AffineModel()
            fx,fy = model(feng_x,feng_y)

            cmaps = colors.LinearSegmentedColormap.from_list('mylist', self.colors_sys, N=6)
            fig = pb.gcf()
            fig.set_size_inches(4,4)
            X += fx*1  # 这里是interval,按小时计算的interval,数值预报默认是1小时出
            Y += fy*1
            pb.contourf(X, Y, Z, radar_sys, cmap=cmaps, extend='both')  # 循环的生成
            pb.xlim(self.stg_X[0],self.stg_X[1])
            pb.ylim(self.stg_Y[0],self.stg_Y[1])
            pb.gca().xaxis.set_major_locator(plt.NullLocator())
            pb.gca().yaxis.set_major_locator(plt.NullLocator())
            pb.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
            pb.margins(0,0)
            affine_image_path = self.save_affine_path + self.real_time + ptime + 'affine' + '.png'
            fig.savefig(affine_image_path,format='png',transparent=True,dpi=200,pad_inches=0)

    def mix(self,affine=True):
        '''
        完成radar+affine
        返回一个二位数组
        '''
        self.wind_radar_affine()
        for i in range(self.time_split):
            ptime = self.real_time + (i+1)*interval
            radar = self.read_json_data(ptime)
            windaffine = read_affine_picture(ptime)
            assert data_nc.shape == data_json.shape ,'shape not equal'
            if affine == True:
                mix_data = (radar*0.88 + windaffine*1.0)
            else:
                mix_data = K*radar*0.88
            print('radar with 数值预报数据融合的shape:',mix_data.shape)
            return mix_data
