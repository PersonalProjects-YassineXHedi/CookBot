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
        try:
            files = os.listdir(path)
        except:
            print("This path doesn't exist")
            continue
        new_names = new_data['names']
        old_names = old_data['names']
        for file in files:
                file_path = path + '/' + file
                change_label_index(file_path, new_names, old_names)
        
            
        

# ---------------- Private Helper Function ---------------- #

def change_label_index(txt_label_file, new_names, old_names):
    """
    Remap class IDs in a YOLO label file from the old class order to the new one.

    For each line: take the old class ID → get its name from old_names → find its
    index in new_names → write that as the new class ID. Box coordinates are unchanged.

    Args:
        txt_label_file (str): Path to the .txt label file.
        new_names (list[str]): New class name list (target order).
        old_names (list[str]): Old class name list (source order).
    """
    with open(txt_label_file, 'r') as file:
        lines = file.readlines()
    
    new_lines= []
    for line in lines:
        line = line.split()
        class_name = old_names[int(line[0])]
        new_index = new_names.index(class_name)
        line[0] = str(new_index)
        new_line = ' '.join(line)+ '\n'
        new_lines.append(new_line)

    with open(txt_label_file, 'w') as file:
        file.writelines(new_lines)



    