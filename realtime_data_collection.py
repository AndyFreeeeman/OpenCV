# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 09:53:24 2022

@author: andy
"""

import cv2
import pickle
import os
import PRFunctions


home_path = '..//product-record//'
save_path = './/sorted_class//'

rec = PRFunctions.Recognition(model='.//models//shufflenet10-512-221209-170.pkl',spSet='.//spData-711')

all_img_path = os.listdir(home_path)

IR_error_store = []

for img_path_counter in range( 0 , len(all_img_path) ):
    
    print("計數： " + str(img_path_counter) + " / " + str(len(all_img_path)))
    print("進度： " + str(int(img_path_counter/len(all_img_path)*100)) + " %")
    
    for in_out_counter in range(0,2):
        
        current_path = home_path + str(all_img_path[img_path_counter])
        
        if in_out_counter == 0:
            current_path = current_path + '//slot_in'
            print(str(all_img_path[img_path_counter]) + '_slotIn')
            
        else:
            current_path = current_path + '//slot_out'
            print(str(all_img_path[img_path_counter]) + '_slotOut')
            
        # lost slot_in or slot_out
        if not os.path.isfile(current_path + '//result.pickle'):
            IR_error_store.append(current_path)
            print("------------------IR Error Detected.----------------")
            
        else:
            with open(current_path + '//result.pickle', 'rb') as handle:
                (resultInfo,ir_locate) = pickle.load(handle)
            
            results , bbox , itemDict , targetItems = resultInfo
            
    
            for img_counter in range (0,10): # 10 images
            
                img = cv2.imread(current_path + '//' + str(img_counter) + '.jpg')
            
                temp = bbox[img_counter]
        
                x1 = temp[:,0]
                y1 = temp[:,1]
                x2 = temp[:,2]
                y2 = temp[:,3]
                
                for xy_counter in range (0 , len(x1)):
                    
                    if x1[xy_counter] != None:
                        
                        cut_img = img[int(y1[xy_counter]):int(y2[xy_counter]) , int(x1[xy_counter]):int(x2[xy_counter])]
                        
                        result = PRFunctions.Recognition.singleFrameInference(rec,cut_img)
                        
                        #print(result)
                        
                        if result != None:
                            result_Dict = dict(enumerate(result, start=1))
                            item = result_Dict[1]
                        
                        if result != None:
                            class_save_path = save_path + '//' + result_Dict[1] + '//'
                        else:
                            class_save_path = save_path + '//' + 'No_Result' + '//'
                        
                        
                        if not os.path.isdir(class_save_path):
                            os.makedirs(class_save_path)
                    
                        if in_out_counter == 0:
                            cv2.imwrite(os.path.join(class_save_path , str(all_img_path[img_path_counter]) + '_In' + str(img_counter) + "_" + str(xy_counter) + '.jpg'), cut_img)
                        else:
                            cv2.imwrite(os.path.join(class_save_path , str(all_img_path[img_path_counter]) + '_Out' + str(img_counter) + "_" + str(xy_counter) + '.jpg'), cut_img)
                        
print("-------------------------------------------")
print("缺少 Slot_In / Slot_Out 清單：")
print(IR_error_store)
