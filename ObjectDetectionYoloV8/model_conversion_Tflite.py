from ultralytics import YOLO
from adaptative_path_function import adapt_path

YOLO_DATA_PATH = adapt_path("Data/SaladDataset")

model = YOLO('yolov8n.pt')
model.train(data=YOLO_DATA_PATH+'/data.yaml', epochs=50, imgsz=640)

model = YOLO("runs/detect/train3/weights/best.pt")
print(model.modules())