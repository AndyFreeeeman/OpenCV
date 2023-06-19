# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 10:02:25 2022

@author: andy
"""

import pickle
import os
import numpy as np
import cv2
import time

home_path = 'Z:\\product-record\\2023-04-20\\'
save_path = 'Z:\\new_class_230420\\'

save_counter = 0
save_img_counter = 0


os.chdir(home_path)
all_img_path = os.listdir(os.curdir)

for img_path_counter in range( 1 , len(all_img_path) ):
    for in_out_counter in range(0,2):
        
        current_path = home_path + str(all_img_path[img_path_counter])
        
        if in_out_counter == 0:
            current_path = current_path + '\\slot_in'
            print(str(all_img_path[img_path_counter]) + '_slotIn')
            
        else:
            current_path = current_path + '\\slot_out'
            print(str(all_img_path[img_path_counter]) + '_slotOut')
            
        with open(current_path + '\\result.pickle', 'rb') as handle:
            (resultInfo,ir_locate) = pickle.load(handle)

        result , bbox , itemDict , targetItems = resultInfo

        for img_counter in range (0,20): # 5 img
            temp = bbox[img_counter]
    
            x1 = temp[:,0]
            y1 = temp[:,1]
            x2 = temp[:,2]
            y2 = temp[:,3]

            img = cv2.imread(current_path + '\\' + str(img_counter) + '.jpg')
            
            if result != None:
                result_Dict = dict(enumerate(result, start=1))
                item = result_Dict[1]
                
            for xy_counter in range (0 , len(x1)):
                
                if x1[xy_counter] != None:
                    
                    cut_img = img[int(y1[xy_counter]):int(y2[xy_counter]) , int(x1[xy_counter]):int(x2[xy_counter])]
                    
                    if result != None:
                        class_save_path = save_path + '\\' + str(result) + '\\'
                    else:
                        class_save_path = save_path + '\\' + 'No_Result' + '\\'
                    
                    if not os.path.isdir(class_save_path):
                        os.makedirs(class_save_path)
                
                    if in_out_counter == 0:
                        cv2.imwrite(os.path.join(class_save_path , str(all_img_path[img_path_counter]) + '_In' + str(img_counter) + '.jpg'), cut_img)
                        save_img_counter = save_img_counter + 1
                    else:
                        cv2.imwrite(os.path.join(class_save_path , str(all_img_path[img_path_counter]) + '_Out' + str(img_counter) + '.jpg'), cut_img)
                        save_img_counter = save_img_counter + 1
                    
        save_counter = save_counter + 1
            
        print("已處理資料夾 " + str(save_counter))
        print("已存圖片 " + str(save_img_counter))
    
        process = int((img_path_counter + 1) / len(all_img_path) * 100)
    
        print("進度：" + str(process) + '%')
    
        process_string = ''
        process_counter = 0
    
        for i in range(0,int(process/2.5)):
            process_string = process_string + '#'
            process_counter = process_counter + 1
        
        
        for j in range(0,int(40-process_counter)):
            process_string = process_string + '-'
    
        print(process_string)
