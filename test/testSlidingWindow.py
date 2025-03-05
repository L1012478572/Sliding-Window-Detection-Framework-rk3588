import cv2
import numpy as np
import sys
import os
# 添加特定目录到路径
# sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
sys.path.append(os.getcwd())
from SlidingWindow import SlidingWindow

# 不需要添加路径
# import sys
# import os
# sys.path.append(os.getcwd())

if __name__ == "__main__":
    # 读取图像
    image = cv2.imread("/home/ljl/share/Sliding-Window-Detection-Framework-rk3588/test/frame3.png")
    # 创建滑窗对象
    sliding_window = SlidingWindow()
    # 设置滑窗大小和步长
    sliding_window.set_sliding_window_params(640, 640)
    # 设置图像缩放倍数
    sliding_window.set_scale_factor(1, 1)
    # 设置中心化
    sliding_window.set_center_flag(True)
    # 滑窗
    sliding_window.sliding_window(image)
    # 打印滑窗数量
    print(len(sliding_window.sliding_window_list))
    # 打印滑窗列表
    for i in range(len(sliding_window.sliding_window_list)):
        print(sliding_window.sliding_window_list[i][0].shape)

    # 显示滑窗图像
    for i in range(len(sliding_window.sliding_window_list)):
        cv2.imshow(f'sliding_window_{i}', sliding_window.sliding_window_list[i][0])
    cv2.imshow('image', image)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

