import os
from config_af import arg_dict

class AffineModel():
    def __init__(self):
        pass
        '''
        模型的初始化,移动的转换，涉及到风速-->风移动的转换
        '''

    def __call__(self):
        fx = (self.feng_x*3.6/85)*0.382
        fy = (self.feng_y*3.6/111)*0.382
        return fx,fy
