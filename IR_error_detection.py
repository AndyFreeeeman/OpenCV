# 樓下cv2版串流

from Detection import Detection,drawBbox
detection = Detection(weight="./product-detect-single-best-221208.pt",im0_shape=(720,1280))

import numpy as np
import cv2
import time
import os

class_path = 'F:\\7-11\\train\\'
error_path = 'E:\\output_img1\\'

all_class_path = os.listdir(class_path)

for class_counter in range(len(all_class_path)):
    
    print(all_class_path[class_counter])
    print(str(class_counter) + " / " + str(len(all_class_path)))
    all_img_path = os.listdir(class_path + all_class_path[class_counter])
    
    for all_img_counter in range(len(all_img_path)):
        
        current_path = class_path + all_class_path[class_counter] + "//" + all_img_path[all_img_counter]
        
        frame = cv2.imread(current_path)
            
        bbox = detection.inference(frame)
        
        print(bbox)
