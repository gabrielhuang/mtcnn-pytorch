from src import detect_faces
from PIL import Image
import cv2
import numpy as np
from time import time

video = cv2.VideoCapture(0)


while True:
    ret, bgr_frame = video.read()
    show_image = bgr_frame.copy()
    if not ret:
        break
    rgb_frame = cv2.cvtColor(bgr_frame,cv2.COLOR_BGR2RGB)
    pil_frame = Image.fromarray(rgb_frame)
    #pil_frame = Image.open('people.jpg')
    last = time()
    bounding_boxes, landmarks = detect_faces(pil_frame)
    dt = time() - last
    print 'Detection {:.2}s or {:.2} fps'.format(dt, 1./dt)
    print bounding_boxes

    # Draw bounding box
    for (x1, y1, x2, y2, confidence) in bounding_boxes.astype(int):
        cv2.rectangle(show_image, (x1, y1), (x2, y2), (255, 255, 255))
    # Draw landmarks
    for person in landmarks.astype(int):
        for landmark_idx in xrange(5):
            x = person[landmark_idx]
            y = person[landmark_idx + 5]
            print x,y
            cv2.circle(show_image, (x, y), 3, (255, 0, 255))

    cv2.imshow('detected_faces', show_image)
    if cv2.waitKey(100) == ord(' '):
        break

