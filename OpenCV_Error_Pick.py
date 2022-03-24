import pickle
import os
import numpy as np
import cv2
import time
from IPython.display import clear_output

home_path = 'C:\\Users\\460442\\Desktop\\error_img\\'
read_path = 'G:\\record\\'
save_path = 'C:\\Users\\460442\\Desktop\\img\\'

counter = 0

os.chdir(home_path)
all_img_path = os.listdir(os.curdir)

for img_path_counter in range( 0 , len(all_img_path) ):
    
    print(str(all_img_path[img_path_counter]))
        
    pick_path = str(all_img_path[img_path_counter]).split('_')
    file_end = pick_path[1]
    pick_path[1] = file_end[:-4]
    
    current_path = read_path + str(pick_path[0]) + '\\slot' + str(pick_path[1]) + '\\'
    
    for img_counter in range (0,5):
        img = cv2.imread(current_path + str(img_counter) + '.jpg')
        print(current_path + str(img_counter) + '.jpg')
        cv2.imshow('img', img)
        cv2.imwrite(os.path.join(save_path , str(time.strftime('%m%d_%H_%M_%S', time.localtime())) + str(counter) + '.jpg'), img)
        counter = counter + 1
        clear_output(wait=True)
    
    print('進度: ' + str(int(img_path_counter/len(all_img_path)*100) + 1) + ' %' )
