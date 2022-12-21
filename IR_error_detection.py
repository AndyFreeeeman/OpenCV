import os

home_path = '/opt/product-recognition-711/record/'


os.chdir(home_path)
all_img_path = os.listdir(os.curdir)
all_img_path = all_img_path[1:]

for img_path_counter in range( 0 , len(all_img_path) - 1 ):
    for in_out_counter in range(0,2):
        current_path = home_path + str(all_img_path[img_path_counter])
        
        if not os.path.isdir(current_path+"\\slot_in"):
            print(str(all_img_path[img_path_counter]))
            print("no slot_in")
            
        if not os.path.isdir(current_path+"\\slot_out"):
            print(str(all_img_path[img_path_counter]))
            print("no slot_out")
