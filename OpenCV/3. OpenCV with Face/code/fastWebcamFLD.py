#!/usr/bin/python
# Copyright 2017 BIG VISION LLC ALL RIGHTS RESERVED
#
# This code is made available to the students of
# the online course titled "Computer Vision for Faces"
# by Satya Mallick for personal non-commercial use.
#
# Sharing this code is strictly prohibited without written
# permission from Big Vision LLC.
#
# For licensing and other inquiries, please email
# spmallick@bigvisionllc.com
#

import cv2,dlib
import sys
from renderFace import renderFace


PREDICTOR_PATH = "../../common/shape_predictor_68_face_landmarks.dat"
RESIZE_HEIGHT = 480
SKIP_FRAMES = 2

try:
  # Create an imshow window
  winName = "Fast Facial Landmark Detector"

  # Create a VideoCapture object
  cap = cv2.VideoCapture(0)

  # Check if OpenCV is able to read feed from camera
  if (cap.isOpened() is False):
    print("Unable to connect to camera")
    sys.exit()

  # Just a place holder. Actual value calculated after 100 frames.
  fps = 30.0

  # Get first frame
  ret, im = cap.read()

  # We will use a fixed height image as input to face detector
  if ret == True:
    height = im.shape[0]
    # calculate resize scale
    RESIZE_SCALE = float(height)/RESIZE_HEIGHT
    size = im.shape[0:2]
  else:
    print("Unable to read frame")
    sys.exit()
  
  # Load face detection and pose estimation models
  detector = dlib.get_frontal_face_detector()
  predictor = dlib.shape_predictor(PREDICTOR_PATH)
  # initiate the tickCounter
  t = cv2.getTickCount()
  count = 0

  # Grab and process frames until the main window is closed by the user.
  while(True):
    if count==0:
      t = cv2.getTickCount()
    # Grab a frame  
    ret, im = cap.read()
    # create imSmall by resizing image by resize scale
    imSmall= cv2.resize(im, None, fx = 1.0/RESIZE_SCALE, fy = 1.0/RESIZE_SCALE, interpolation = cv2.INTER_LINEAR)

    # Process frames at an interval of SKIP_FRAMES.
    # This value should be set depending on your system hardware
    # and camera fps.
    # To reduce computations, this value should be increased
    if (count % SKIP_FRAMES == 0):
      # Detect faces
      faces = detector(imSmall,0)

    # Iterate over faces
    for face in faces:
      # Since we ran face detection on a resized image,
      # we will scale up coordinates of face rectangle
      newRect = dlib.rectangle(int(face.left() * RESIZE_SCALE),
                               int(face.top() * RESIZE_SCALE),
                               int(face.right() * RESIZE_SCALE),
                               int(face.bottom() * RESIZE_SCALE))
      
      # Find face landmarks by providing reactangle for each face
      shape = predictor(im, newRect)
      # Draw facial landmarks
      renderFace(im, shape)

    # Put fps at which we are processinf camera feed on frame
    cv2.putText(im, "{0:.2f}-fps".format(fps), (50, size[0]-50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 255), 3)
    # Display it all on the screen
    cv2.imshow(winName, im)
    # Wait for keypress
    key = cv2.waitKey(1) & 0xFF

    # Stop the program.
    if key==27:  # ESC
      # If ESC is pressed, exit.
      sys.exit()

    # increment frame counter
    count = count + 1
    # calculate fps at an interval of 100 frames
    if (count == 100):
      t = (cv2.getTickCount() - t)/cv2.getTickFrequency()
      fps = 100.0/t
      count = 0
  cv2.destroyAllWindows()
  cap.release()

except Exception as e:
  print(e)
