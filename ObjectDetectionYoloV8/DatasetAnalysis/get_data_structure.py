import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def plot_bbox_with_orientation(image_path, label_path):
    # Load image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 

    height, width, _ = image.shape

    # Load labels
    with open(label_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        # Parse label
        class_id, x_center, y_center, w, h, *orientation = map(float, line.split())
        
        # Convert normalized coordinates to pixel values
        x_center *= width
        y_center *= height
        w *= width
        h *= height

        # Calculate bounding box corners
        x1 = int(x_center - w / 2)
        y1 = int(y_center - h / 2)
        x2 = int(x_center + w / 2)
        y2 = int(y_center + h / 2)

        # Draw bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # Draw orientation (if available)
        if orientation:
            angle = orientation[0]  # Assuming orientation is the first additional parameter
            # Calculate orientation line endpoints
            length = min(w, h) / 2
            dx = length * np.cos(np.radians(angle))
            dy = length * np.sin(np.radians(angle))
            x_end = int(x_center + dx)
            y_end = int(y_center + dy)
            # Draw orientation line
            cv2.line(image, (int(x_center), int(y_center)), (x_end, y_end), (0, 255, 0), 2)

    # Display image
    plt.imshow(image)
    plt.axis('off')
    plt.show()



image_path = "/home/hboua/GitRepo/Data/test/images/DSC_5941_JPG_jpg.rf.b475b612117860a9a8fe6ec637b22a40.jpg"
label_path = "/home/hboua/GitRepo/Data/test/labels/DSC_5941_JPG_jpg.rf.b475b612117860a9a8fe6ec637b22a40.txt"

plot_bbox_with_orientation(image_path, label_path)








