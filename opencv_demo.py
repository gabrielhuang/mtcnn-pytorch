from src import detect_faces
from PIL import Image
import cv2
import numpy as np
from time import time
import argparse

parser = argparse.ArgumentParser('Face Detector')
parser.add_argument('--video', default='webcam', help='video to analyze')
parser.add_argument('--skip', type=int, default=1, help='frames to skip (1 means no skip)')
parser.add_argument('--width', type=int, default=0, help='resize width')

args = parser.parse_args()

if args.video != 'webcam':
    video = cv2.VideoCapture(args.video)
else:
    video = cv2.VideoCapture(0) 

frame_idx = 0
while True:
    # Get frame
    ret, bgr_frame = video.read()
    if not ret:
        print 'Could not open video'
        break
    print 'Shape', bgr_frame.shape

    # Skip frames
    frame_idx += 1
    if frame_idx % args.skip != 0:
        print 'Skipping frame'
        continue

    # Resize?
    if args.width:
        height = bgr_frame.shape[0] * args.width / bgr_frame.shape[1]
        bgr_frame = cv2.resize(bgr_frame, (args.width, height))

    show_image = bgr_frame.copy()
    
    # Convert data
    rgb_frame = cv2.cvtColor(bgr_frame,cv2.COLOR_BGR2RGB)
    pil_frame = Image.fromarray(rgb_frame)

    # Actual detection
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

