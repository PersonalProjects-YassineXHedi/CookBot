from ultralytics.utils import yaml_load
import os 
import random

DATA_PATH = "/home/yassine/GitRepo/Data/yolo_dataset_v1"

def get_classes_and_count(data_path = DATA_PATH):
    data = yaml_load(DATA_PATH + "/data.yaml")

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
    return classes_and_count

def get_classes_images_and_labels(data_path = DATA_PATH):
    data = yaml_load(DATA_PATH + "/data.yaml")

    names = data['names']
    classes_images_and_labels = {}
    for name in names:
        image_path_list = []
        diff_dir = ['test', 'val','train']
        for dir_name in diff_dir:
            label_dir = data[dir_name].replace('/images', '/labels')
            image_dir = data[dir_name]

            label_files = sorted(os.listdir(label_dir))
            img_files = sorted(os.listdir(image_dir))

            for label_file, img_file in zip(label_files, img_files):
                label_path = os.path.join(label_dir, label_file)
                image_path = os.path.join(image_dir, img_file)
                open_file = open(label_path)
                for line in open_file:
                    class_id = int(line.strip().split()[0])
                    if(class_id == names.index(name)):
                        image_path_list.append((image_path,label_path))
                        break
        classes_images_and_labels[name] = image_path_list
    return classes_images_and_labels

def get_class_num_images(classes_images_and_labels, num, class_name):
    images_and_labels_one_class = []
    images_and_labels = classes_images_and_labels[class_name]
    if(len(images_and_labels) < num):
        return
    i=0
    while(i<num):
        value = random.randint(0,len(images_and_labels))
        images_and_labels_one_class.append(images_and_labels[value])
    return images_and_labels_one_class



    
    




