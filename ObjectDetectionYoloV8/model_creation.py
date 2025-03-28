from ultralytics import YOLO
import os
from adaptative_path_function import adapt_path




path = adapt_path("/home/hboua/GitRepo/Data/CandyDataset/data.yaml")
print(path)

model = YOLO("yolov8s.pt")

results = model.train(data=path, epochs=100, imgsz=640)

prediction = model.predict("/home/hboua/GitRepo/Data/CandyDataset/test/images/all-type-of-cup_000069_jpg.rf.bdfe0ca8227bd023cc956d59af11fbe2.jpg")
print(prediction[0])