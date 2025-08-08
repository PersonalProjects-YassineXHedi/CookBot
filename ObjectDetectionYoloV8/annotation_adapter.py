import yaml
import os

old_yaml_file = '/home/yassine/GitRepo/Data/test/old_data.yaml'
new_yaml_file = '/home/yassine/GitRepo/Data/test/new_data.yaml'

def change_class_number(old_yaml_file, new_yaml_file):
    """
    Updates YOLO label files to match a new class order from a new YAML file.
    This works by mapping the class indices from the old YAML to the new YAML.
    
    Args:
        old_yaml_file (str): Path to the original dataset YAML file (old classes).
        new_yaml_file (str): Path to the new dataset YAML file (new classes).
    """
    with open(new_yaml_file, 'r') as new_file:
        new_data = yaml.safe_load(new_file)

    with open(old_yaml_file, 'r') as old_file:
        old_data = yaml.safe_load(old_file)

    dirs = ['val' ,'test', 'train']
    for dir in dirs:
        path = new_data[dir].replace('images','labels')
        new_index = 0
        try:
            files = os.listdir(path)
        except:
            print("This path doesn't exist")
            continue
        for name in new_data['names']:
            old_index = old_data['names'].index(name)
            for file in files:
                file_path = path + '/' + file
                change_label_index(file_path , old_index, new_index)
            new_index += 1
            
        

# ---------------- Private Helper Function ---------------- #

def change_label_index(txt_label_file, old_index, new_index):
    """
    Changes a specific class index in a YOLO label file to a new index.
    
    Args:
        txt_label_file (str): Path to the YOLO label file (.txt).
        old_index (int): The original class index to replace.
        new_index (int): The new class index to set.
    """
    with open(txt_label_file, 'r') as file:
        lines = file.readlines()
    
    new_lines= []
    for line in lines:
        line = line.split()
        if(int(line[0]) == old_index):
            line[0] = str(new_index)
        new_line = ' '.join(line)+ '\n'
        new_lines.append(new_line)

    with open(txt_label_file, 'w') as file:
        file.writelines(new_lines)

    