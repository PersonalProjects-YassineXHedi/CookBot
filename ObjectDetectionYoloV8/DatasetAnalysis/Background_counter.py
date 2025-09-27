import yaml
import os

def count_background_imgs(yaml_file_path):
    with open(yaml_file_path) as file:
        yaml_file = yaml.safe_load(file)
    count_dic = {
        "train":0,
        "val":0,
        "test":0
    }
    dirs = ["train", "val", "test"]
    for dir in dirs:
        dir_path = yaml_file[dir].replace('images','labels')
        try:
            files = os.listdir(dir_path)
        except:
            print("This path doesn't exist")
            continue
        for file in files:
            path = dir_path + '/' + file
            with open(path) as txt:
                lines = txt.readlines()
            if not lines:
                count_dic[dir] += 1
    return count_dic

yaml_file_path = '/home/yassine/GitRepo/Data/test2/data.yaml'
dic = count_background_imgs(yaml_file_path)
print(dic)