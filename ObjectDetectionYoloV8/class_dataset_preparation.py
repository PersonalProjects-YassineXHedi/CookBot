import os
import yaml
import shutil

old_dataset_folder_path = '/home/yassine/GitRepo/Data/SaladDataset'
new_yaml_file = '/home/yassine/GitRepo/Data/test/new_data.yaml'

def create_dataset_from_classes(old_dataset_folder_path, new_yaml_file):
    with open(new_yaml_file, 'r') as new_file:
        new_yaml_file = yaml.safe_load(new_file)

    old_yaml_path = old_dataset_folder_path + "/data.yaml"
    with open(old_yaml_path, 'r') as old_file:
        old_yaml_file = yaml.safe_load(old_file)


    new_dataset_path = new_yaml_file['train'].replace('/train/images', '')
    if not os.path.exists(new_dataset_path):
        os.makedirs(new_dataset_path)

    idxs_to_leave = get_idxs_to_leave(old_yaml_file, new_yaml_file)
    
    dirs = ['val' ,'test', 'train']
    for dir in dirs:
        dir_path = new_yaml_file[dir].replace('/images', '')
        imgs_dir_path = dir_path + '/images' 
        lbls_dir_path = dir_path + '/labels' 
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if not os.path.exists(imgs_dir_path):
            os.makedirs(imgs_dir_path)
        if not os.path.exists(lbls_dir_path):
            os.makedirs(lbls_dir_path)

        path = old_yaml_file[dir].replace('images','labels')
        img_lbl_list = get_images_and_labels_to_keep(path, idxs_to_leave)
        for img_lbl in img_lbl_list:
            shutil.copy(img_lbl[0], imgs_dir_path)
            shutil.copy(img_lbl[1], lbls_dir_path)

def get_images_and_labels_to_keep(files_path, idxs_to_leave):
    img_lbl_list = []
    try:
        files = os.listdir(files_path)
        for file in files:
            lbl_path = files_path + '/' + file
            with open(lbl_path, 'r') as file:
                lines = file.readlines()
            to_add = True
            for line in lines:
                line = line.split()
                if int(line[0]) not in idxs_to_leave:
                    to_add = False
                    break
            if to_add:
                img_path = lbl_path.replace('labels','images').replace('.txt','.jpg')
                img_lbl_list.append((img_path, lbl_path))                   
    except:
        print("This path doesn't exist")
    return img_lbl_list


def get_idxs_to_leave(old_yaml_file, new_yaml_file):
    idxs_to_leave = []
    names = new_yaml_file['names']
    for name in names:
        idxs_to_leave.append( old_yaml_file['names'].index(name))
    return idxs_to_leave
    
create_dataset_from_classes(old_dataset_folder_path, new_yaml_file)