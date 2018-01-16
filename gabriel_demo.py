from src import detect_faces
from PIL import Image
import cv2
import numpy as np


image = Image.open('people.jpg')
bounding_boxes, landmarks = detect_faces(image)

print bounding_boxes

show_image = np.asarray(image)

for (x1, y1, x2, y2, confidence) in bounding_boxes.astype(int):
    cv2.rectangle(show_image, (x1, y1), (x2, y2), (255, 255, 255))

cv2.imshow('detected_faces', show_image)
cv2.waitKey(0)

