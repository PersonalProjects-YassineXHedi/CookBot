from ultralytics.utils import yaml_load
import os 
import random
import shutil
import math 

DATA_PATH = '/home/yassine/GitRepo/Data'
YOLO_DATA_PATH = "/home/yassine/GitRepo/Data/yolo_dataset_v1"

def get_classes_and_count(data_path = YOLO_DATA_PATH):
    data = yaml_load(data_path + "/data.yaml")

    names = data['names']
    classes_and_count = {name: 0 for name in names}

    diff_dir = ['test', 'val','train']
    for dir_name in diff_dir:
        label_dir = data[dir_name].replace('/images', '/labels')
        counts = [0] * len(names)
        for file in os.listdir(label_dir):
            open_file = open(os.path.join(label_dir, file))
            for line in open_file:
                class_id = int(line.strip().split()[0])
                counts[class_id] += 1
        i=0
        for name in names:
            classes_and_count[name] += counts[i]
            i += 1
        classes_and_count

    classes_and_count = dict(sorted(classes_and_count.items(), key=lambda item: item[1], reverse=True))
    return classes_and_count

def get_classes_images_and_labels(data_path = YOLO_DATA_PATH):
    data = yaml_load(data_path + "/data.yaml")

    names = data['names']
    classes_images_and_labels = {}
    diff_dir = [ 'val', 'test','train']
    for dir_name in diff_dir:
        classes_images_and_labels_specific_dir = {}
        label_dir = data[dir_name].replace('/images', '/labels')
        image_dir = data[dir_name]

        label_files = sorted(os.listdir(label_dir))
        img_files = sorted(os.listdir(image_dir))
        for name in names:
            class_image_path_list = []
            for label_file, img_file in zip(label_files, img_files):
                label_path = os.path.join(label_dir, label_file)
                image_path = os.path.join(image_dir, img_file)
                open_file = open(label_path)
                for line in open_file:
                    class_id = int(line.strip().split()[0])
                    if(class_id == names.index(name)):
                        class_image_path_list.append((image_path,label_path))
                        break
            classes_images_and_labels_specific_dir[name] = class_image_path_list
        classes_images_and_labels[dir_name] = classes_images_and_labels_specific_dir
    return classes_images_and_labels




def get_class_images_labels(classes_images_and_labels, class_name, percent = 100):
    if(percent > 100 or percent <=0):
            return
    images_and_labels_one_class = {}
    diff_dir = [ 'val', 'test','train']
    for dir_name in diff_dir:
        images_and_labels_one_class_specific_dir = []
        images_and_labels_specific_dir = classes_images_and_labels[dir_name][class_name]
        
        num = math.ceil((percent * len(images_and_labels_specific_dir)) / 100)
        i=0
        while(i<num):
            value = random.randint(0,len(images_and_labels_specific_dir))
            images_and_labels_one_class_specific_dir.append(images_and_labels_specific_dir[value])
            i+=1
        images_and_labels_one_class[dir_name] = images_and_labels_one_class_specific_dir
    return images_and_labels_one_class


def try_create_dir_and_push_data_for_specific_class(folder_name, image_and_label_path_dict, folder_path = DATA_PATH):
    #create dir 
    path = folder_path + '/' + folder_name
    if not os.path.exists(path):
        os.makedirs(path)

    #create images and labels dir
    images_dir_path = path + '/images/'
    labels_dir_path = path + '/labels/'
    if not os.path.exists(images_dir_path):
        os.makedirs(images_dir_path)
    if not os.path.exists(labels_dir_path):
        os.makedirs(labels_dir_path)

    #push the images and labels path to the corresponding dir
    for img_path, label_path in image_and_label_path_dict[folder_name]:
        shutil.copy(img_path, images_dir_path)
        shutil.copy(label_path, labels_dir_path)

def get_first_n_classe(n, data_path = YOLO_DATA_PATH):
    dic_classes_counts = get_classes_and_count(data_path)
    n_classes = list(dic_classes_counts.keys())[:n]
    return n_classes




def create_dataset(classes_names, percent, new_dataset_folder_path, dataset_folder_name, full_dataset_path = YOLO_DATA_PATH):
    classes_images_and_labels = get_classes_images_and_labels(full_dataset_path)
    new_dataset_folder_full_path = new_dataset_folder_path + '/' + dataset_folder_name
    os.makedirs(new_dataset_folder_full_path, exist_ok=False)
    
    diff_dir = [ 'val', 'test','train']
    for dir_name in diff_dir:
        for class_name in classes_names:
            images_and_labels_one_class = get_class_images_labels(classes_images_and_labels, class_name,percent)
            try_create_dir_and_push_data_for_specific_class(dir_name, images_and_labels_one_class, new_dataset_folder_full_path)



