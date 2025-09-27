from ultralytics import YOLO

yaml_file_path = '/home/yassine/GitRepo/Data/test1/data.yaml'

model = YOLO('yolov8n.pt')
model.train(data=yaml_file_path, epochs=50, imgsz=640)