from ultralytics import YOLO
import os
from adaptative_path_function import adapt_path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

DATA_PATH = adapt_path("/home/hboua/GitRepo/Data/CandyDataset")
cat_dog_image = adapt_path("cat_dog.jpg")
#Load a model
model = YOLO("yolov8s.pt")

# train model
#results = model.train(data=os.path.join(DATA_PATH), epochs=100, imgsz=640)


img = mpimg.imread(cat_dog_image)
plt.imshow(img)

prediction = model.predict(cat_dog_image)
prediction[0]
len(prediction[0].boxes)
print(prediction[0])


# show image with bounding boxes


print("about to show image")