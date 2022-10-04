# 把label .txt檔的class全部改為0

import os
from IPython.display import clear_output

home_path = 'E:\\helmet_detect\\all_data\\all_label\\'

os.chdir(home_path)
all_txt_path = os.listdir(os.curdir)

for txt_counter in range( 0 , len(all_txt_path) ):
    
    clear_output(wait=True)
    current_path = home_path + str(all_txt_path[txt_counter])
    
    text = []
    f = open(current_path,'r')
    
    for line in f.readlines(): # each row
        # 1 0.113 0.1746987951807229 0.078 0.1566265060240964
        text.append('0' + line[1:])
        
    f.close()
    
    f = open(current_path,'w')
    f.writelines(text)
    f.close()
    
    print("進度：" + str(int(txt_counter/len(all_txt_path)*100+1)) + "%")
    print("目前檔案：" + str(current_path))
