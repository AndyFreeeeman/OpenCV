# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 14:13:28 2021

@author: maomao
"""
from models.experimental import attempt_load
import torch
import cv2
from utils.general import non_max_suppression
import numpy as np
def image_resize(image, width, height, inter = cv2.INTER_AREA, pad_value=(0, 0, 0)):

    dim = None 
    (h, w) = image.shape[:2]
    r_h = height/float(h)
    r_w = width/float(w)

    if(r_h<r_w):
        dim = (int(w * r_h), height) 
    elif(r_h>r_w):
        dim = (width, int(h * r_w)) 
    else:
        dim = (width, height)
    
    pad_w = int((width - dim[0]) /2)
    pad_h = int((height - dim[1]) /2)

    resized = cv2.resize(image, dim, interpolation = inter) 
    pad_img = cv2.copyMakeBorder(resized, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_CONSTANT, value=pad_value)

    return pad_img


def drawBbox(img,bbox):#,T0):
    #T = time.time()-T0
    #cv2.putText(img, "fps: "+str(1/T), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
    for box in bbox:
        x0,y0,x1,y1 = box[0:4].astype(int)
        cv2.rectangle(img, (x0, y0), (x1, y1), (0, 255, 0), 2)
        cv2.putText(img, str(int(box[-1])), (x0, y0+10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
        #cv2.putText(img, str((x0,y0)), (x0, y0), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
    return img    

class Detection():
    def __init__(self,model='YOLOv5',weight='./weights/yolov5s.pt',im0_shape=(720,960)):
        if(model=='YOLOv5'):
            self.Model = attempt_load(weight).cuda()
        self.Model.eval()
        self.im0_size = np.linalg.norm(im0_shape)
        self.img_shape = 640,640
        self.img0_shape = im0_shape
        self.gain = max(self.img_shape) / max(self.img0_shape)
        self.pad = (self.img_shape[1] - self.img0_shape[1] * self.gain) / 2, (self.img_shape[1] - self.img0_shape[0] * self.gain) / 2
    def inference(self,img):
        img = image_resize(img, 640, 640)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = torch.from_numpy(img).to(torch.device('cuda:0'))/ 255.0
        img = img.unsqueeze(0).permute(0,3,1,2).float()  
        pred = self.Model(img)[0]
        pred = non_max_suppression(pred, 0.8, 0.6)
        if(pred[0] != None):
            pred = pred[0]
            pred[:, [0, 2]] -= self.pad[0]  # x padding
            pred[:, [1, 3]] -= self.pad[1]  # y padding
            pred[:, :4] /= self.gain
            pred[:, [0,2]] = pred[:, [0,2]].clamp(0, self.img0_shape[1])  # x1
            pred[:, [1,3]] = pred[:, [1,3]].clamp(0, self.img0_shape[0])  # y1
            #pred = pred[pred[:,5]<10] 
        return pred.cpu().data.numpy()
    
    def batchInference(self,imgList):
        for i,img in enumerate(imgList):
            img = image_resize(img, 640, 640)
            imgList[i] = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.stack(imgList, axis=0)
        img = torch.from_numpy(img).to(torch.device('cuda:0'))/ 255.0
        img = img.permute(0,3,1,2).float() 
        with torch.no_grad():
            preds = self.Model(img)[0]
        preds = non_max_suppression(preds, 0.85, 0.6)
        result = []
        for pred in preds:
            if(pred != None):
                pred[:, [0, 2]] -= self.pad[0]  # x padding
                pred[:, [1, 3]] -= self.pad[1]  # y padding
                pred[:, :4] /= self.gain
                pred[:, [0,2]] = pred[:, [0,2]].clamp(0, self.img0_shape[1])  # x1
                pred[:, [1,3]] = pred[:, [1,3]].clamp(0, self.img0_shape[0])  # y1
                size = torch.norm(pred[:,2:4] - pred[:,0:2],dim=1,keepdim=True)/self.im0_size
                cxy = (pred[:,2:4] + pred[:,0:2])/2
                pred = torch.cat((pred,size,cxy),1)
            result.append(pred.cpu().data.numpy())
        return result #x0,y0,x1,y1,conf,cls,size,cx,cy
    
