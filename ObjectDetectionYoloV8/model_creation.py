from ultralytics import YOLO
import os
from adaptative_path_function import adapt_path
import matplotlib.pyplot as plt

DATA_PATH = adapt_path("/home/hboua/GitRepo/Data/CandyDataset")

#Load a model
model = YOLO("yolov8s.pt")

# train model
results = model.train(data=os.path.join(DATA_PATH,  ), epochs=100, imgsz=640)


prediction = model.predict("/home/hboua/GitRepo/Data/CandyDataset/test/images/all-type-of-cup_000069_jpg.rf.bdfe0ca8227bd023cc956d59af11fbe2.jpg")
print(prediction[0])


# show image with bounding boxes
image = prediction[0].plot()
plt.imshow(image)
plt.title(class_names[label.numpy()]) # add title to image by indexing on class_names list
plt.axis(False);

print("about to show image")

