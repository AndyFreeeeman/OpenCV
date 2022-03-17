import pickle
import os
import numpy as np
import cv2
import keyboard
from IPython.display import clear_output

home_path = 'C:\\Users\\460442\\Desktop\\up_down_data\\level123_data\\raw_data\\'
save_path = 'C:\\Users\\460442\\Desktop\\up_down_data\\level123_data\\'

os.chdir(home_path)
all_img_path = os.listdir(os.curdir)

for img_path_counter in range( 0 , len(all_img_path) ):
    
    print(str(all_img_path[img_path_counter]))
    current_path = home_path + str(all_img_path[img_path_counter])
    
    img = cv2.imread(current_path)

    cv2.imshow('img', img)
    
    key = cv2.waitKey(0)
    
    if key == ord('w'): # up
        cv2.imwrite(os.path.join(save_path + 'up\\' , str(all_img_path[img_path_counter]) ), img)
        print("saved up image " + str(all_img_path[img_path_counter]))
        
    elif key == ord('s'): # down
        cv2.imwrite(os.path.join(save_path + 'down\\' , str(all_img_path[img_path_counter]) ), img)
        print("saved down image " + str(all_img_path[img_path_counter]))
        
    elif key == ord('d'): # none
        cv2.imwrite(os.path.join(save_path + 'none\\' , str(all_img_path[img_path_counter]) ), img)
        print("saved none image " + str(all_img_path[img_path_counter]))
        
    else:
        print('error')
        
    os.remove(home_path + str(all_img_path[img_path_counter]))
    
    clear_output(wait=True)
    
    print('進度: ' + str(int(img_path_counter/len(all_img_path)*100) + 1) + ' %' )
