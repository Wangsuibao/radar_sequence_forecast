'''
关于模型的所有config
'''
import time
import os

arg_dict = {'stg_X':(38.66, 41.35),
			'stg_y':(114.92, 118.45),
			'interval':1,  # 小时
			'pixel':(800,800),
			'duration':(1,3),  # 1，2，3 整点
			'colors_sys':[(1,1,1),(0,0,1),(0,1,0),(1,1,0),(1,0,0),(1,0,1)],
			'radar_sys':[0,10,20,30,40,50,60],
			'meteo_path':'/home/data/meteo_path',
			'radar_path':'/home/data/radar_path',
			'save_affine_path':'/home/data/save_affine_path',
			'save_mix_path':'/home/data/save_mix_path',
			}
