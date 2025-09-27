import os
import yaml
import shutil
from annotation_adapter import change_class_number

def create_dataset_from_classes(old_dataset_folder_path, new_yaml_path):
    """
    Creates a new YOLO dataset by extracting only the classes defined in a new YAML file
    from an old dataset, keeping only matching classes and their corresponding images/labels.

    Args:
        old_dataset_folder_path (str): Path to the original dataset folder (contains data.yaml).
        new_yaml_path (str): Path to the new YAML file defining the subset of classes to keep.
    """
    with open(new_yaml_path, 'r') as new_file:
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
    change_class_number(old_yaml_path, new_yaml_path)
    shutil.copy(new_yaml_path, new_dataset_path)
    old_name = new_dataset_path + '/' + os.path.basename(new_yaml_path)
    new_name = new_dataset_path + '/data.yaml'
    os.rename(old_name,new_name)

def get_images_and_labels_to_keep(files_path, idxs_to_leave):
    """
    Returns a list of (image_path, label_path) tuples for label files that contain
    only classes we want to keep.

    Args:
        files_path (str): Path to the folder containing label (.txt) files.
        idxs_to_leave (list[int]): List of class indices to keep.

    Returns:
        list[tuple[str, str]]: List of image and label file paths to include.
    """
    img_lbl_list = []
    #to remove
    x = []

    try:
        files = os.listdir(files_path)
        for file in files:
            lbl_path = files_path + '/' + file
            with open(lbl_path, 'r') as file:
                lines = file.readlines()
            if not lines:
                img_path = lbl_path.replace('labels','images').replace('.txt','.jpg')
                x.append((img_path, lbl_path))
                img_lbl_list.append((img_path, lbl_path))
                continue
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
    print(x)
    return img_lbl_list


def get_idxs_to_leave(old_yaml_file, new_yaml_file):
    """
    Gets the class indices from the old dataset that match the class names in the new dataset.

    Args:
        old_yaml_file (dict): Parsed YAML data of the old dataset.
        new_yaml_file (dict): Parsed YAML data of the new dataset.

    Returns:
        list[int]: List of class indices from the old dataset to keep.
    """
    idxs_to_leave = []
    names = new_yaml_file['names']
    for name in names:
        idxs_to_leave.append( old_yaml_file['names'].index(name))
    return idxs_to_leave
    
old_dataset_folder_path = '/home/yassine/GitRepo/Data/SaladDataset-v3'
new_yaml_file = '/home/yassine/GitRepo/Data/new_data.yaml'
create_dataset_from_classes(old_dataset_folder_path, new_yaml_file)