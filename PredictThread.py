import cv2
import threading
import queue

'''
推理线程模块
    1.  推理子线程 
    2.  推理线程管理模块
'''


'''
推理子线程
    1. 
'''
class PredictChildThread(threading.Thread):
    def __init__(self, input_queue : queue.Queue, output_queue : queue.Queue):
        super().__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue
    
    def run(self):
        pass
