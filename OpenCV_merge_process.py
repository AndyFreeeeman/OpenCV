import pickle
import os
import numpy as np
import cv2
import keyboard
import time

home_path = 'C:\\Users\\460442\\itri_img\\'
save_path = 'C:\\Users\\460442\\Desktop\\after_img\\'

save_counter = 0

img_0 = 0
img_1 = 0
img_2 = 0
img_3 = 0
img_4 = 0


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

        for img_counter in range (0,5): # 5 img
            temp = bbox[img_counter]
    
            x1 = temp[:,0]
            y1 = temp[:,1]
            x2 = temp[:,2]
            y2 = temp[:,3]
            

            img = cv2.imread(current_path + '\\' + str(img_counter) + '.jpg')
            
            if img_counter == 0:
                cv2.putText(img, 'IR: ' + str(IR) , (20, 680), cv2.FONT_HERSHEY_SIMPLEX,2, (0, 255, 255), 3, cv2.LINE_AA)
            
                print(result)
            
                if result != None:
                    #result_Dict = dict(enumerate(result, start=1))
                    #item = result_Dict[1]
                    #confidence = result_Dict[2]
                
                    cv2.putText(img, str(result) , (20, 60), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 2, cv2.LINE_AA)
                    #cv2.putText(img, 'Confidence: ' +  confidence, (20, 120), cv2.FONT_HERSHEY_SIMPLEX,2, (0, 255, 255), 2, cv2.LINE_AA)

                else:
                    cv2.putText(img, 'No Result', (20, 60), cv2.FONT_HERSHEY_SIMPLEX,2, (0, 255, 255), 3, cv2.LINE_AA)

            for xy_counter in range (0 , len(x1)):
                cv2.rectangle(img, (int(x1[xy_counter]), int(y1[xy_counter])), (int(x2[xy_counter]), int(y2[xy_counter])), (230, 0, 230), 3)
            
            cv2.line(img, (int(imgPointX) , 0), (int(imgPointX) , 720), (125, 255, 0), 7)
            
            if img_counter == 0:
                img_0 = img
            elif img_counter == 1:
                img_1 = img
            elif img_counter == 2:
                img_2 = img
            elif img_counter == 3:
                img_3 = img
            elif img_counter == 4:
                img_4 = img
    
    
    final_img = np.vstack((img_0 , img_1))
    final_img = np.vstack((final_img , img_2))
    final_img = np.vstack((final_img , img_3))
    final_img = np.vstack((final_img , img_4))
    
    
    cv2.imwrite(os.path.join(save_path , str(all_img_path[img_path_counter]) + '.jpg'), final_img)
            
    save_counter = save_counter + 1
            
    print("save image. " + str(save_counter))
    
    os.system('cls')
    
    process = int((img_path_counter + 2) / len(all_img_path) * 100)
    
    print("進度：" + str(process) + '%')
    
    process_string = ''
    process_counter = 0
    
    for i in range(0,int(process/5)):
        process_string = process_string + '##'
        process_counter = process_counter + 1
        
        
    for j in range(0,int(20-process_counter)):
        process_string = process_string + '--'
    
    print(process_string)
