
# coding: utf-8

# In[2]:

import cv2,dlib
import sys
import math
from renderFace import renderFace
from playsound import playsound

PREDICTOR_PATH = "./data/shape_predictor_68_face_landmarks.dat"
RESIZE_HEIGHT = 480
SKIP_FRAMES = 2


# In[ ]:


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
    frame_count = 0
    initial_eye_dist = 0
    
    # Grab and process frames until the main window is closed by the user.
    while(True):
        if count==0:
            t = cv2.getTickCount()
        # Grab a frame  
        ret, im = cap.read()
        
        im = cv2.flip(im, 1)
        
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
            shape = predictor(imSmall, newRect)
            
            # Draw facial landmarks
            lefteye_x, lefteye_y = shape.part(39).x, shape.part(39).y
            righteye_x, righteye_y = shape.part(42).x, shape.part(42).y
            uppernose_x, uppernose_y = shape.part(27).x, shape.part(27).y
            lowernose_x, lowernose_y = shape.part(30).x, shape.part(30).y
            
            cv2.circle(imSmall, (lefteye_x, lefteye_y),  5, (0,0,255), -1)
            cv2.circle(imSmall, (righteye_x, righteye_y),  5, (0,0,255), -1)
            cv2.circle(imSmall, (uppernose_x, uppernose_y), 5, (255, 0, 0), -1)
            cv2.circle(imSmall, (lowernose_x, lowernose_y), 5, (255, 0, 0), -1)
            
            epsilon = 0.00000000000000000000000001 
            
        # get the inital eye distance
        if frame_count < 10 :
            initial_eye_dist += math.sqrt( (lefteye_x - righteye_x)**2 + (lefteye_y - righteye_y)**2 ) / 10                
            
        # get eye & nose slope
        eye_slope = abs((lefteye_y - righteye_y) / (lefteye_x - righteye_x + epsilon))
        nose_slope = abs((uppernose_y - lowernose_y) / (uppernose_x - lowernose_x + epsilon))
        eye_dist = math.sqrt( (lefteye_x - righteye_x)**2 + (lefteye_y - righteye_y)**2 )
            
        if frame_count > 10 and frame_count % 50 == 0:
            print("Frame count", frame_count)
            print("Eye slope : {:.5f}".format(eye_slope))
            print("Nose slope : {:.5f}".format(nose_slope))
            print("Initial Eye dist : {:.5f}".format(initial_eye_dist))    
            print("Eye dist : {:.5f}".format(eye_dist))           

            if initial_eye_dist * 1.3 < eye_dist :
                playsound("./data/warning.mp3")

            if eye_slope > 0.1 :
                playsound("./data/warning.mp3")

        # renderFace(imSmall, shape)
        frame_count += 1

        # Put fps at which we are processinf camera feed on frame
        cv2.putText(imSmall, "{0:.2f}-fps".format(fps), (50, size[0]-50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 255), 3)
        # Display it all on the screen
        cv2.imshow(winName, imSmall)
        # Wait for keypress
        key = cv2.waitKey(1) & 0xFF

        # Stop the program.
        if key==27:  # ESC
            # If ESC is pressed, exit.
            break
            # sys.exit()

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

