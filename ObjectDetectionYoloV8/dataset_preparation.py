from ultralytics.utils import yaml_load
import os 
import random
import shutil

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
    for name in names:
        image_path_list = []
        diff_dir = [ 'val', 'test','train']
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

def get_class_images_labels(classes_images_and_labels, class_name, percent = 100):
    images_and_labels_one_class = []
    images_and_labels = classes_images_and_labels[class_name]
    if(percent > 100 or percent <=0):
        return
    num = (percent*len(images_and_labels))/100
    i=0
    while(i<num):
        value = random.randint(0,len(images_and_labels))
        images_and_labels_one_class.append(images_and_labels[value])
        i+=1
    return images_and_labels_one_class


def create_dir_with_specific_images(folder_name, image_and_label_path_list, folder_path = DATA_PATH):
    #create dir 
    path = folder_path + '/' + folder_name
    os.makedirs(path, exist_ok=True)

    #create images and labels dir
    images_dir_path = path + '/images/'
    labels_dir_path = path + '/labels/'
    os.makedirs(images_dir_path, exist_ok=True)
    os.makedirs(labels_dir_path, exist_ok=True)

    #push the images and labels path to the corresponding dir
    for img_path, label_path in image_and_label_path_list:
        shutil.copy(img_path, images_dir_path)
        shutil.copy(label_path, labels_dir_path)

def get_first_n_classe(n, data_path = YOLO_DATA_PATH):
    dic_classes_counts = get_classes_and_count(data_path)
    n_classes = list(dic_classes_counts.keys())[:n]
    return n_classes




def create_dataset(classes_names, percent, new_dataset_folder_path, dataset_folder_name, full_dataset_path = YOLO_DATA_PATH):
    classes_images_and_labels = get_classes_images_and_labels(full_dataset_path)
    dataset_folder_full_path = new_dataset_folder_path + '/' + dataset_folder_name
    os.makedirs(dataset_folder_full_path, exist_ok=False)
    for class_name in classes_names:
        images_and_labels_one_class = get_class_images_labels(classes_images_and_labels, class_name,percent)
        diff_dir = [ 'val', 'test','train']
        for dir_name in diff_dir:
            create_dir_with_specific_images(dir_name, images_and_labels_one_class, dataset_folder_full_path)

create_dataset(['ground beef', 'onion'], 1, DATA_PATH,'test_v1_1_percent')

