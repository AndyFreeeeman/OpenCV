# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 10:24:17 2022

@author: andy4
"""

# OpenCV_dezipimg.py 
# 逐一儲存圖片

import os
import cv2
import random


img_path = '..//product-record//'
save_path = './/'


all_img_path = os.listdir(img_path)

for pack_counter in range( int(len(all_img_path)*20/500) ):
    if not os.path.isdir(".//" + str(pack_counter)):
        os.makedirs( ".//" + str(pack_counter) )
    
print("已生成 " + str(pack_counter) + " 包資料.")

error_list = []
save_img_counter = 0


for img_path_counter in range( 0 , len(all_img_path) ):
    
    for in_out_counter in range(0,2):
        
        current_path = img_path + str(all_img_path[img_path_counter])
        
        if in_out_counter == 0:
            current_path = current_path + '//slot_in'
        else:
            current_path = current_path + '//slot_out'
            
        if os.path.isfile(current_path + '//result.pickle'):

            for img_counter in range (0,10): # 10 img
                
                print(str(all_img_path[img_path_counter]))
                print("計數:" + str(save_img_counter))
                
                img = cv2.imread(current_path + '//' + str(img_counter) + '.jpg')
                
                
                print('進度: ' + str(int(img_path_counter/len(all_img_path)*100) + 1) + ' %' )
                
                if in_out_counter == 0:
                    cv2.imwrite(os.path.join(save_path + str(random.randrange(45)) + "//" , str(all_img_path[img_path_counter]) + '_slotIn_' + str(img_counter) + '.jpg'), img)
                    
                else:
                    cv2.imwrite(os.path.join(save_path + str(random.randrange(45)) + "//" , str(all_img_path[img_path_counter]) + '_slotOut_' + str(img_counter) + '.jpg'), img)
                    
                save_img_counter = save_img_counter + 1
                
        else:
            error_list.append(all_img_path[img_path_counter])
            print("------------------IR Error Detected.----------------")
            
print("-------------------------------------------")
print("缺少 Slot_In / Slot_Out 清單：")
print(error_list)
