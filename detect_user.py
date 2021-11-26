import os, cv2 ,dlib
from numpy.core.numeric import True_
from db import *
from imutils import face_utils
from tkinter import messagebox
import threading
import time



class CountdownTask:
      
    def __init__(self):
        self._running = True
      
    def terminate(self):
        self._running = False
      
    def run(self, n):
        n = n * 60*10
        while self._running and n > 0:
            n -= 1
            time.sleep(0.1)
        global state
        state = False
        # cap.release()
        # cv2.destroyAllWindows()

class DetectUser():
    def __init__(self) -> None:
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    
    def run(self) -> str:
        list_user_db = show_user_id()

        data_classfiers = []
        list_user = []

        for i in list_user_db:
            data_classfier = cv2.face.LBPHFaceRecognizer_create()
            try:
                data_classfier.read(f'./classifiers/{i[0]}_classifier.xml')
                data_classfiers.append(data_classfier)
                list_user.append(i[0])
            except Exception as e:
                pass
        

        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        c = CountdownTask()
        t1 = threading.Thread(target=c.run,args=(2,))
        t1.setDaemon(True)
        t1.start()
        global state
        state = True
        text = None
        while state:
            ret, image = cap.read()

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            rects = self.detector(gray, 1)

            for (i, rect) in enumerate(rects):

                shape = self.predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                (x, y, w, h) = face_utils.rect_to_bb(rect)
                roi_gray =  gray[y:y+h,x:x+w].copy()
                list_confidence = []
                for i in range(len(list_user)):
                    id , confidence = data_classfiers[i].predict(roi_gray)
                    list_confidence.append(confidence)
                value_confidence_min = min(list_confidence)
                index = list_confidence.index(value_confidence_min)
                if value_confidence_min >= 65:
                    text = list_user[index]
                    font = cv2.FONT_HERSHEY_PLAIN
                    image = cv2.putText(image, text, (x, y-4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    messagebox.showinfo("Thông báo","{} chấm công thành công".format(text))
                    cap.release()
                    cv2.destroyAllWindows()
                    c.terminate()
                    return text
                else:
                    pred = -1
                    text = "UnknownFace"
                    font = cv2.FONT_HERSHEY_PLAIN
                    image = cv2.putText(image, text, (x, y-4), font, 1, (0, 0,255), 1, cv2.LINE_AA)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
            cv2.imshow('Chấm công',image)
            if cv2.waitKey(1) == 27:
                pass
        cap.release()
        cv2.destroyAllWindows()
        c.terminate()
        return text

