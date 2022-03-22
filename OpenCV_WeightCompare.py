# data collection
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 09:19:52 2021

@author: maomao
"""

from Detection import Detection,drawBbox

import numpy as np
import cv2
import os
import time
from IPython.display import clear_output

old_detection = Detection(weight="C:\\Users\\andy4\\inference test\\weights\\product-detect-single-best-211203.pt",im0_shape=(720,1280))
detection = Detection(weight="C:\\Users\\andy4\\inference test\\weights\\product-detect-single-best-220316.pt",im0_shape=(720,1280))

home_path = 'D:\\input_img\\'
save_path = 'D:\\output_img\\'

save_counter = 0
img__counter = 0

os.chdir(home_path)
all_img_path = os.listdir(os.curdir)


for img_path_counter in range( 0 , len(all_img_path) ):
    
    
    current_path = home_path + str(all_img_path[img_path_counter])
    
    frame = cv2.imread(current_path)
    old_frame = cv2.imread(current_path)
    
    bbox = detection.inference(frame)
    old_bbox = old_detection.inference(frame)
    
    if bbox.shape[0]!=0:
        for box in bbox:
            stamp = str(int(time.time()*1000))
            x0,y0,x1,y1, _, Cls = box.astype(int)
            
    if old_bbox.shape[0]!=0:
        for old_box in bbox:
            stamp = str(int(time.time()*1000))
            old_x0,old_y0,old_x1,old_y1, old__, old_Cls = old_box.astype(int)
            
    boxframe = drawBbox(frame,bbox)
    cv2.putText(boxframe, 'New (2022.03.16)', (20, 65), cv2.FONT_HERSHEY_SIMPLEX,  1.5, (0, 0, 255), 2, cv2.LINE_AA)
    
    old_boxframe = old_drawBbox(old_frame,old_bbox)
    cv2.putText(old_boxframe, 'Old (2021.12.03)', (20, 65), cv2.FONT_HERSHEY_SIMPLEX,  1.5, (0, 0, 255), 2, cv2.LINE_AA)
    
    img__counter = img__counter + 1
    
    if img__counter == 1:
        img1 = np.hstack((boxframe , old_boxframe))
    elif img__counter == 2:
        img2 = np.hstack((boxframe , old_boxframe))
    elif img__counter == 3:
        img3 = np.hstack((boxframe , old_boxframe))
    elif img__counter == 4:
        img4 = np.hstack((boxframe , old_boxframe))
    elif img__counter == 5:
        img5 = np.hstack((boxframe , old_boxframe))
        
    else :
        img__counter = 0
        
        final_img = np.vstack((img1 , img2))
        final_img = np.vstack((final_img , img3))
        final_img = np.vstack((final_img , img4))
        final_img = np.vstack((final_img , img5))
        
        cv2.imwrite(os.path.join(save_path , str(all_img_path[img_path_counter])), final_img)
        
        clear_output(wait=True)
    
        print("save image. " + str(save_counter))
        save_counter = save_counter + 1
    
        process = int((img_path_counter + 2) / len(all_img_path) * 100)
        print("進度：" + str(process) + '%')
    
        process_string = ''
        process_counter = 0
    
        for i in range(0,int(process/2.5)):
            process_string = process_string + '#'
            process_counter = process_counter + 1
            
        for j in range(0,int(40-process_counter)):
            process_string = process_string + '-'
    
        print(process_string)


