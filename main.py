import time
from afmodel import RadarWindAffine
from config_af import arg_dict


real_time = time.time()
radaraffine = RadarWindAffine(arg_dict,real_time)
radaraffine.mix()  # 完成一个real_time的向后预测（3张）。

'''
注意：需要一个实时启动文件。完成 main.py 的反复操作。
'''
