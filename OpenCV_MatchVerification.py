# OpenCV_MatchVerification.py 
# 把沒辦法匹配的圖片或label檔刪除

import os
import numpy as np
import cv2
from IPython.display import clear_output

file_path = 'D:\\label_3\\label3\\temp\\'

os.chdir(file_path)
all_file = os.listdir(os.curdir)

for file_counter in range( 0 , int(len(all_file)/2) ):

    os.chdir(file_path)
    all_file = os.listdir(os.curdir)
    
    clear_output(wait=True)
    print('進度: ' + str(int(file_counter/len(all_file)*100) + 1) + ' %' )
    
    for file_counter in range( 0 , int(len(all_file)/2) ):

        img_name = all_file[2 * file_counter]
        img_name = img_name[:-4]
    
        txt_name = all_file[2 * file_counter + 1]
        txt_name = txt_name[:-4]
    
        print("file_counter: " + str(file_counter))

    
        if img_name == txt_name:
        
            
            print(img_name)
            print(txt_name)
            print("匹配")
        
        else:
        
            os.remove( file_path + all_file[2 * file_counter] )

            print(img_name)
            print(txt_name)
            print("------------刪除------------")
            
            break
