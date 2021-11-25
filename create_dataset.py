from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2

def create_dataset(name):
    detector = dlib.get_frontal_face_detector()

    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    cap = cv2.VideoCapture(0)

    dem = 0
    while True:
        ret,image = cap.read()
    
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 1)
        new_img = None
        for (i, rect) in enumerate(rects):
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            # convert dlib's rectangle to a OpenCV-style bounding box
            # [i.e., (x, y, w, h)], then draw the face bounding box
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            new_img = image[y-10:y+h+10,x-10:x+h].copy()
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # show the face number
            cv2.putText(image, "Face #{}".format(i + 1), (x - 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(image, "Dem: {}".format(dem+1), (30,30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # loop over the (x, y)-coordinates for the facial landmarks
            # and draw them on the image
            for (x, y) in shape:
                cv2.circle(image, (x, y), 1, (0, 0, 255), -1)

        cv2.imshow("Output", image)
        if cv2.waitKey(1)  == 27 or dem == 300:
            cap.release()
            cv2.destroyAllWindows()
            return dem 
        try:
            cv2.imwrite('./data/{_name}/{_dem}{_name}.jpg'.format(_name = name, _dem = dem),new_img)
            dem +=1
        except: 
            pass
