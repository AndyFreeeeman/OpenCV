# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 18:58:45 2023

@author: andy4
"""

"""
 1. 複製原本的dataset: product-single
 2. 把 val 的 img 和 label 全部丟回 train
 3. 新蒐集的Data丟到train裡面
 4. 新dataset的train資料夾看總共dataset有多少
 5. 切分新的val data 10%
 6. 創建新的.yaml

"""

import os
import random
import datetime
import shutil


home_path = "./"


all_dataset_path = os.listdir(home_path)

new_dataset_path = home_path + "product-single-" + str(datetime.date.today())

if not os.path.isdir( new_dataset_path ):
    
    os.makedirs( new_dataset_path )
    
    os.makedirs( new_dataset_path + "/train/images" )
    os.makedirs( new_dataset_path + "/train/labels" )
    os.makedirs( new_dataset_path + "/val/images" )
    os.makedirs( new_dataset_path + "/val/labels" )


print( "---- 生成新的dataset: " "product-single-" + str(datetime.date.today()) + " ----" )

# 1.複製原本的dataset: product-single 
# 2.把 val 的 img 和 label 全部丟回 train

old_dataset_name = "product-single-2000-00-00"

for file_name in all_dataset_path:
    
    if file_name[0] == "p":
        if int(file_name[15:19]) >= int(old_dataset_name[15:19]):
            if int(file_name[20:22]) >= int(old_dataset_name[20:22]):
                if int(file_name[23:25]) >= int(old_dataset_name[23:25]):
                    old_dataset_name = file_name

old_dataset = home_path + old_dataset_name

print("判定目前最新的dataset為: " + old_dataset)

files = os.listdir(old_dataset + "/train/images")
for f in files:
    shutil.copyfile(old_dataset + "/train/images/" + f, new_dataset_path + "/train/images/" + f)
    
print("---- 已轉移train的images ----")

    
files = os.listdir(old_dataset + "/train/labels")
for f in files:
    shutil.copyfile(old_dataset + "/train/labels/" + f, new_dataset_path + "/train/labels/" + f)

print("---- 已轉移train的labels ----")

    
files = os.listdir(old_dataset + "/val/images")
for f in files:
    shutil.copyfile(old_dataset + "/val/images/" + f, new_dataset_path + "/train/images/" + f)

print("---- 已轉移val的images ----")   

 
files = os.listdir(old_dataset + "/val/labels")
for f in files:
    shutil.copyfile(old_dataset + "/val/labels/" + f, new_dataset_path + "/train/labels/" + f)

print("---- 已轉移val的labels ----")


# 3. 新蒐集的Data丟到train裡面

new_label_path = home_path + "new_label"


files = os.listdir(new_label_path + "/images")
for f in files:
    shutil.copyfile(new_label_path + "/images/" + f, new_dataset_path + "/train/images/" + f)

print("---- 已轉移新label的images ----")


files = os.listdir(new_label_path + "/labels")
for f in files:
    shutil.copyfile(new_label_path + "/labels/" + f, new_dataset_path + "/train/labels/" + f)

print("---- 已轉移新label的labels ----")


# 4. 新dataset的train資料夾看總共dataset有多少

all_img = os.listdir(new_dataset_path + "/train/images")
all_label = os.listdir(new_dataset_path + "/train/labels")

new_dataset_number = len(os.listdir(new_dataset_path + "/train/labels"))

print("新的dataset共有 " + str(new_dataset_number) + "張")


# 5. 切分新的val data 10%

val_num = int(new_dataset_number * 0.1)

selected = random.sample(all_label,val_num)

for s in selected:
    tid = s[:-4]
    os.rename(new_dataset_path + '/train/labels/'+s,new_dataset_path + '/val/labels/'+s)
    os.rename(new_dataset_path + '/train/images/'+tid+'.jpg',new_dataset_path + '/val/images/'+tid+'.jpg')
    
print("已切分 " + str(val_num) + " 至validation")


# 6. 更新.yaml

yaml = open( "../" + "product-single-" + str(datetime.date.today()) + '.yaml', 'w')

yaml.write("train: dataset/product-single-" + str(datetime.date.today()) + "/train/images\n")
yaml.write("val: dataset/product-single-" + str(datetime.date.today()) + "/val/images")
yaml.write("\n\nnc: 1\nnames: ['0',]")

yaml.close()

print("已創建新yaml檔 : " + "product-single-" + str(datetime.date.today()) + '.yaml')
