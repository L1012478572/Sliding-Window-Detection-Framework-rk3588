import cv2
import numpy as np
import platform


'''
滑窗区分功能
 通过设置的滑窗大小和步长，对图像进行滑窗分区
 将滑窗图像暂存到列表中
'''
class SlidingWindow:
    def __init__(self):
        self.sliding_window_list = []   # 滑窗图像列表 列表中每个元素为(滑窗图像, 滑窗x坐标起始, 滑窗y坐标起始)
        self.window_size_x = 640  # 滑窗大小x
        self.window_size_y = 640  # 滑窗大小y
        self.image_size_x = 0  # 图像大小x
        self.image_size_y = 0  # 图像大小y
        
        # 默认参数
        self.overlap_rate = 0.5  # 重合率
        # 缩放倍数
        # 缩放倍数用于在分配滑框之前，对原始图像进行缩放
        self.scale_factor_x = 1.0  # 图像的缩放倍数
        self.scale_factor_y = 1.0  # 图像的缩放倍数
        
        # 是否启动中心化 
        # 启动中心化后，根据滑框大小 自动去除图像的边缘 以减少滑框数量
        self.center_flag = False  # 是否启动中心化
    
    def sliding_window(self, image : np.ndarray):
        '''
        滑窗函数 实现滑窗截图功能
            image : 输入图像
        '''
        try:
            image_scale = np.copy(image)
            if self.scale_factor_x != 1.0 or self.scale_factor_y != 1.0:
                image_scale = cv2.resize(image, (int(image.shape[1] * self.scale_factor_x), int(image.shape[0] * self.scale_factor_y)))
            # 获取图像大小
            self.image_size_x = image_scale.shape[1]
            self.image_size_y = image_scale.shape[0]
            if self.center_flag == False:
                # 计算横向滑窗数量
                self.window_num_x = (self.image_size_x - self.window_size_x) / (self.window_size_x * (1 - self.overlap_rate)) + 1
                # 若是window_num_x为小数，则向上取整
                self.window_num_x = int(self.window_num_x) if self.window_num_x % 1 == 0 else int(self.window_num_x) + 1
                # 计算纵向滑窗数量
                self.window_num_y = (self.image_size_y - self.window_size_y) / (self.window_size_y * (1 - self.overlap_rate)) + 1
                # 若是window_num_y为小数，则向上取整
                self.window_num_y = int(self.window_num_y) if self.window_num_y % 1 == 0 else int(self.window_num_y) + 1
                print(f'window_num_x: {self.window_num_x}, window_num_y: {self.window_num_y}')
                # 清空滑窗列表
                self.sliding_window_list.clear()
                # 计算有效区域的起始位置和大小
                # y方向有效区域
                y_redundance = int(self.image_size_y - (self.window_size_y + (self.window_num_y - 1) * self.window_size_y * (1 - self.overlap_rate)))
                y_start_offset = int(y_redundance / 2) if y_redundance > 0 else 0
                # x方向有效区域
                x_redundance = int(self.image_size_x - (self.window_size_x + (self.window_num_x - 1) * self.window_size_x * (1 - self.overlap_rate)))
                x_start_offset = int(x_redundance / 2) if x_redundance > 0 else 0
                
                # 计算滑窗列表
                for y in range(self.window_num_y):
                    # 滑框y坐标起始和结束
                    sliding_y_start = y_start_offset + int(y * self.window_size_y * (1 - self.overlap_rate))
                    sliding_y_end = sliding_y_start + self.window_size_y
                    if sliding_y_end > self.image_size_y:
                        sliding_y_end = self.image_size_y
                        sliding_y_start = sliding_y_end - self.window_size_y
                    
                    for x in range(self.window_num_x):
                        # 滑框x坐标起始和结束
                        sliding_x_start = x_start_offset + int(x * self.window_size_x * (1 - self.overlap_rate))
                        sliding_x_end = sliding_x_start + self.window_size_x
                        if sliding_x_end > self.image_size_x:
                            sliding_x_end = self.image_size_x
                            sliding_x_start = sliding_x_end - self.window_size_x
                        
                        # 滑框截取图像
                        sliding_window_image = np.copy(image_scale[sliding_y_start:sliding_y_end, sliding_x_start:sliding_x_end])   
                        # 将滑框图像添加到滑窗列表
                        self.sliding_window_list.append((sliding_window_image, sliding_x_start, sliding_y_start))
            else:
                # 启动中心化
                # 计算横向滑窗数量
                self.window_num_x = (self.image_size_x - self.window_size_x) / (self.window_size_x * (1 - self.overlap_rate)) + 1
                # 若是window_num_x为小数，则向下取整
                self.window_num_x = int(self.window_num_x)
                # 计算纵向滑窗数量
                self.window_num_y = (self.image_size_y - self.window_size_y) / (self.window_size_y * (1 - self.overlap_rate)) + 1
                # 若是window_num_y为小数，则向下取整
                self.window_num_y = int(self.window_num_y)
                print(f'window_num_x: {self.window_num_x}, window_num_y: {self.window_num_y}')
                # 清空滑窗列表
                self.sliding_window_list.clear()
                # 计算有效区域的起始位置和大小
                # y方向有效区域
                y_redundance = int(self.image_size_y - (self.window_size_y + (self.window_num_y - 1) * self.window_size_y * (1 - self.overlap_rate)))
                y_start_offset = int(y_redundance / 2) if y_redundance > 0 else 0
                # x方向有效区域
                x_redundance = int(self.image_size_x - (self.window_size_x + (self.window_num_x - 1) * self.window_size_x * (1 - self.overlap_rate)))
                x_start_offset = int(x_redundance / 2) if x_redundance > 0 else 0
                
                # 计算滑窗列表
                for y in range(self.window_num_y):
                    # 滑框y坐标起始和结束
                    sliding_y_start = y_start_offset + int(y * self.window_size_y * (1 - self.overlap_rate))
                    sliding_y_end = sliding_y_start + self.window_size_y
                    if sliding_y_end > self.image_size_y:
                        sliding_y_end = self.image_size_y
                        sliding_y_start = sliding_y_end - self.window_size_y
                    
                    for x in range(self.window_num_x):
                        # 滑框x坐标起始和结束
                        sliding_x_start = x_start_offset + int(x * self.window_size_x * (1 - self.overlap_rate))
                        sliding_x_end = sliding_x_start + self.window_size_x
                        if sliding_x_end > self.image_size_x:
                            sliding_x_end = self.image_size_x
                            sliding_x_start = sliding_x_end - self.window_size_x
                        
                        # 滑框截取图像
                        sliding_window_image = np.copy(image_scale[sliding_y_start:sliding_y_end, sliding_x_start:sliding_x_end])   
                        # 将滑框图像添加到滑窗列表
                        self.sliding_window_list.append((sliding_window_image, sliding_x_start, sliding_y_start))
                        
        except Exception as e:
            print(e)
            return False
        return True

    def set_sliding_window_params(self, window_size_x : int, window_size_y : int):
        '''
        设置滑窗大小和步长
            window_size_x : 滑窗大小x
            window_size_y : 滑窗大小y
        '''
        self.window_size_x = window_size_x
        self.window_size_y = window_size_y
        
    def set_scale_factor(self, scale_factor_x : float, scale_factor_y : float):
        '''
        设置图像缩放倍数
            scale_factor_x : 图像缩放倍数x
            scale_factor_y : 图像缩放倍数y
        '''
        self.scale_factor_x = scale_factor_x
        self.scale_factor_y = scale_factor_y
        
    def set_center_flag(self, center_flag : bool):
        '''
        设置是否启动中心化
            center_flag : 是否启动中心化
        '''
        self.center_flag = center_flag
        
    