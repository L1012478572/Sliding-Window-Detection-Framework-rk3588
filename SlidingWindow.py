import cv2
import numpy as np
import platform
# import torch

# X86_PLATFORM = 0
# ARM_PLATFORM = 1

# # 判断系统架构是x86还是arm
# architecture = platform.machine()
# if architecture == 'x86_64':
#     PLATFROM = X86_PLATFORM
#     print('x86平台')
# else:
#     PLATFROM = ARM_PLATFORM
#     print('arm平台')
    
# if PLATFROM == X86_PLATFORM:
#     import ultralytics
# else:
#     from rknnlite.api import RKNNLite

'''
滑窗区分功能
 通过设置的滑窗大小和步长，对图像进行滑窗分区
 将滑窗图像暂存到列表中
'''
class SlidingWindow:
    def __init__(self):
        self.sliding_window_list = []   # 滑窗图像列表
        self.window_size_x = 640  # 滑窗大小x
        self.window_size_y = 640  # 滑窗大小y
        self.image_size_x = 0  # 图像大小x
        self.image_size_y = 0  # 图像大小y
        
        # 默认参数
        self.overlap_rate = 0.5  # 重合率
        pass
    
    '''
    滑窗函数
    '''
    def sliding_window(self, image : np.ndarray):
        # 获取图像大小
        self.image_size_x = image.shape[1]
        self.image_size_y = image.shape[0]
        # 计算横向滑窗数量
        self.window_num_x = (self.image_size_x - self.window_size_x) / (self.window_size_x * (1 - self.overlap_rate)) + 1
        # 计算纵向滑窗数量
        self.window_num_y = (self.image_size_y - self.window_size_y) / (self.window_size_y * (1 - self.overlap_rate)) + 1
        
    
    '''
    设置滑窗大小和步长
        window_size_x : 滑窗大小x
        window_size_y : 滑窗大小y
    '''
    def set_sliding_window_params(self, window_size_x : int, window_size_y : int):
        self.window_size_x = window_size_x
        self.window_size_y = window_size_y
        
    