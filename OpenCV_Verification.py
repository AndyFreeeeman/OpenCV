import pickle
import os
import numpy as np
import cv2
import keyboard
import time

home_path = 'C:\\Users\\andy4\\itri_img\\'
error_path = 'E:\\itri_bad_img'

error_counter = 24

os.chdir(home_path)
all_img_path = os.listdir(os.curdir)
all_img_path = all_img_path[1:]

for img_path_counter in range( 0 , len(all_img_path) - 1 ):
    for in_out_counter in range(0,1):
        print(str(all_img_path[img_path_counter]))
        current_path = home_path + str(all_img_path[img_path_counter])
        
        if in_out_counter == 0:
            current_path = current_path + '\\slotIn'
        else:
            current_path = current_path + '\\slotOut'
            
        with open(current_path + '\\result.pickle', 'rb') as handle:
            b = pickle.load(handle)
    
        result,bbox,boxList,imgPointX,cam,IR = b

        for img_counter in range (0,4): # 5 img
            temp = bbox[img_counter]
    
            x1 = temp[:,0]
            y1 = temp[:,1]
            x2 = temp[:,2]
            y2 = temp[:,3]

            img = cv2.imread(current_path + '\\' + str(img_counter) + '.jpg')
            img_copy = cv2.imread(current_path + '\\' + str(img_counter) + '.jpg')

            for xy_counter in range (0 , len(x1)):
                cv2.rectangle(img, (int(x1[xy_counter]), int(y1[xy_counter])), (int(x2[xy_counter]), int(y2[xy_counter])), (230, 0, 230), 3)

            cv2.imshow('img', img)
    
            if cv2.waitKey(0) == 13:
                cv2.imwrite(os.path.join(error_path , 'error_' + str(time.strftime('%m%d_%H_%M_%S', time.localtime())) + '.jpg'), img_copy)
                error_counter = error_counter + 1
                print("saved bad image")
        
            else:
                print("change image")
