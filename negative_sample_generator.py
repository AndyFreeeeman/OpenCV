
from Detection import Detection,drawBbox
detection = Detection(weight="./weights/product-detect-single-best-220308.pt",im0_shape=(720,1280))

import numpy as np
import cv2
import redis
import time
import os

img_save_path = 'E:\\output_img1\\'
txt_save_path = 'E:\\output_txt\\'

counter = 0

record = 0

camDict = {'1-6-1':['cam.1-6-1-L','cam.1-6-1-M','cam.1-6-1-R'],
           '1-6-2':['cam.1-6-2-L','cam.1-6-2-M','cam.1-6-2-R'],
           '1-6-3':['cam.1-6-3-L','cam.1-6-3-M','cam.1-6-3-R'],
           #'1-6-4':['cam.1-6-4-L','cam.1-6-4-M','cam.1-6-4-R'],
           '1-5-1':['cam.1-5-1-L','cam.1-5-1-M','cam.1-5-1-R'],
           '1-5-2':['cam.1-5-2-L','cam.1-5-2-M','cam.1-5-2-R'],
           '1-5-3':['cam.1-5-3-L','cam.1-5-3-M','cam.1-5-3-R']
           }


product = 0
get_data_mode = False

if __name__ == "__main__":

    pool = redis.ConnectionPool(host='redis-shelf.itri.go', port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    
shelfList = list(camDict.keys())
shelf = 0
cam = 0
while True:

    buffer_name = camDict[shelfList[shelf]][cam]
    buffer = r.xread({buffer_name: "$"}, count=None, block=0)
    
    data = buffer[0][1][0]
    tid = data[0].decode("utf-8").split('-')[0]

    cam1_bytes = data[1][b'frame']
    
    frame = cv2.imdecode(np.frombuffer(cam1_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)

    cv2.imshow('frame', frame)
    
    key = cv2.waitKey(1)
    # w
    if key == 119:
        shelf = shelf-1
    # s -> down
    elif key == 115:
        shelf = shelf+1
    # a -> left
    elif key == 97:
        cam = cam-1
    # d -> rights
    elif key == 100:
        cam=cam+1
    # z    
    elif key==122:
        product = product-1 
    # c
    elif key==99:
        product = product+1        
    elif key==109:
        get_data_mode = not get_data_mode
        
    # enter
    elif key==13:
        record = record + 1
        
    if record%2 == 1:
        file_name =  str(time.strftime('%m%d_%H_%M_%S', time.localtime())) + str(counter)
        
        cv2.imwrite(os.path.join(img_save_path , file_name + '.jpg'), frame)
        file = open(txt_save_path + file_name + '.txt' , 'a+')
        print("save img" + str(counter))
        
        counter = counter + 1
        
    if cam>2:
        cam=2
    if cam<0:
        cam=0
    if shelf>5:
        shelf=5
    if shelf<0:
        shelf=0
