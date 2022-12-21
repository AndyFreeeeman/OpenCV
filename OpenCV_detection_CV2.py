from Detection import Detection,drawBbox
detection = Detection(weight="./product-detect-single-best-221208.pt",im0_shape=(720,1280))

import numpy as np
import cv2
import time

product = 0

# 205 206 207 208
ip = 205

# 8080 8081 8082
port = 8080

camera_ip = "http://192.168.1." + str(ip) + ":" + str(port) + "/?action=stream"

cap = cv2.VideoCapture(camera_ip)

shelf = 0
cam = 0
change_flag = False

while(True):
    
    if change_flag == True:
        
        change_flag = False
        camera_ip = "http://192.168.1." + str(ip) + ":" + str(port) + "/?action=stream"
        cap = cv2.VideoCapture(camera_ip)
        
    
    # 讀取一幅影格
    ret, frame = cap.read()
    
    # 若讀取至影片結尾，則跳出
    if ret == False:
        break

    t0 = time.time()
    bbox = detection.inference(frame)
    t1 = time.time()
    print(t1-t0)
    if bbox.shape[0]!=0:
        for box in bbox:
            stamp = str(int(time.time()*1000))
            x0,y0,x1,y1, _, Cls = box.astype(int)
            cv2.imwrite('temp/'+stamp+'.jpg',frame[y0:y1,x0:x1])
            
    boxframe = drawBbox(frame,bbox)
    cv2.imshow('frame', boxframe)
    
    
    key = cv2.waitKey(1)

    # w -> up
    if key == 119:
        
        change_flag = True
        if ip < 208:
            ip = ip + 1
            print(ip)
        else:
            ip = 205
            print(ip)
            
    # s -> down
    elif key == 115:
        
        change_flag = True
        if ip > 205:
            ip = ip - 1
            print(ip)
        else:
            ip = 208
            print(ip)
            
    # a -> left
    elif key == 97:
        
        change_flag = True
        if port < 8082:
            port = port + 1
            print(port)
        else:
            port = 8080
            print(port)
            
    # d -> rights
    elif key == 100:
        
        change_flag = True
        if port > 8080:
            port = port - 1
            print(port)
        else:
            port = 8082
            print(port)
            
    elif key == 13: # Enter
    
        cap.release()
        cv2.destroyAllWindows()
