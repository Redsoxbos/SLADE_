import os

img_root = '/root/share/KITTI360/data_2d_raw'
depth_root = '/root/share/KITTI360/data_distance_map'

train_txt = open('./train_test_inputs/kitti360_train_files_with_gt.txt', 'w')
eval_txt = open('./train_test_inputs/kitti360_eval_files_with_gt.txt', 'w')
test_txt = open('./train_test_inputs/kitti360_test_files_with_gt.txt', 'w')

date_list = os.listdir(img_root) # 2013_05_28_drive_0000_sync, 2013_05_28_drive_0003_sync...



for date_folder in date_list:  
    t = 0
    e = 0
    test = 0

    date_path = os.path.join(img_root, date_folder) # root/share/KITTI360/data_2d_raw/2013_05_28_drive_0000_sync
    img_num_list = os.listdir(date_path) # image_02, image03
    for img_num_folder in img_num_list:
        img_num_path = os.path.join(date_path, img_num_folder) # root/share/KITTI360/data_2d_raw/2013_05_28_drive_0000_sync/image_02
        rgb_path = os.path.join(img_num_path, 'data_rgb') # root/share/KITTI360/data_2d_raw/2013_05_28_drive_0000_sync/image_02/data_rgb
        img_list = os.listdir(rgb_path) #0000001223.png, 0000001124.png, ...
        



        for img_file in img_list:
            img_path = os.path.join(rgb_path, img_file)
            depth_file = img_file[:-4]+'.npy'
            depth_path = os.path.join(depth_root, date_folder, img_num_folder) # /root/share/KITTI360/data_distance_map/2013_05_28_drive_0000_sync/image_02
            data_depth = os.listdir(depth_path)[0] # data_depth
            depth_path = os.path.join(depth_path, data_depth, depth_file) # /root/share/KITTI360/data_distance_map/2013_05_28_drive_0000_sync/image_02/data_depth

            relative_img_path = img_path.split("/")[5:]
            relative_depth_path = depth_path.split("/")[5:]
            relative_img_path = "/".join(relative_img_path)
            relative_depth_path = "/".join(relative_depth_path)

            lines = relative_img_path + " " + relative_depth_path + " 700\n"
            if os.path.exists(depth_path):
                # train set: 00, 02 ,03, eval set: 09, test set: 10
                date_folder_num = date_folder[-7:-5]
                if date_folder_num == "10":
                    if test < 1000:  
                        test_txt.write(lines)
                        test += 1

                    
                elif date_folder_num == "09":
                    if e < 1000:
                        eval_txt.write(lines)
                        e += 1
                elif (date_folder_num == "00"):
                    if t < 5000:
                        train_txt.write(lines)
                        t += 1

train_txt.close()
test_txt.close()
eval_txt.close()


    