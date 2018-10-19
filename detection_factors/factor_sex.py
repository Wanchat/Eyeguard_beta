import sys

import dlib
import cv2
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLabel


class Sex:
    def __init__(self, model=r"C:\Users\Wanch\Google Drive\Thesis\code_eyeguard\Eyeguard\main\sex_25.model"):
        self.madel_age = load_model(model)
    def estimate_sex(self, window_face):
        self.window_face = cv2.resize(window_face, (28, 28))
        self.window_face = self.window_face.astype("float") / 255.0
        self.window_face = img_to_array(self.window_face)
        self.window_face = np.expand_dims(self.window_face, axis=0)
        (self.man, self.woman) = self.madel_age.predict(self.window_face)[0]
        self.label_sex = "woman" if self.woman > self.man else "man"
        self.score_sex = self.woman if self.woman > self.man else self.man
        return self.label_sex, self.score_sex

class App(QMainWindow):
    def __init__(self):
        super(). __init__()
        self.setGeometry(100,100,200,200)
        button = QPushButton("start",self)
        button.move(100-50,50-15)
        button2 = QPushButton("detection",self)
        button2.move(100-50,100-15)
        button3 = QPushButton("close",self)
        button3.move(100-50,150-15)

        button.clicked.connect(self.play)
        button2.setCheckable(True)
        button3.clicked.connect(self.p)
        button2.clicked[bool].connect(self.d)
        button3.clicked.connect(self.p)

        self.sex = ""

        self.label = QLabel(self)
        self.label.setGeometry(0,170, 200, 30)
        self.label.setText(self.sex)

        self.start = False
        self.opendetect = False

    def d(self,e):
        if e:
            self.opendetect = True
        else:
            self.opendetect =False

    def p(self):
        self.start = True

    def play(self):
        self.start = False
        face_detect = cv2.CascadeClassifier(
            "haarcascade_frontalface_default.xml")
        cap = cv2.VideoCapture(0)
        sex_class = Sex()
        frame_number = 0
        # sex = ''
        while not (self.start):
            self.label.setText("")
            _, frame = cap.read()
            frame_number += 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face = face_detect.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in face:
                cv2.rectangle(frame,
                              (x, y),
                              (x + w, y + h),
                              (255, 255, 255),
                              2)
                face_n = frame[y:y + h, x:x + w] # Cut face
                if self.opendetect == True:
                    self.sex = sex_class.estimate_sex(face_n) # Prediction sex function
                    self.label.setText(str(self.sex))
                    print(self.sex[0])
            cv2.imshow("Frame", frame)
            cv2.waitKey(1)

        cap.release()
        cv2.destroyAllWindows()
        self.label.setText("")

if __name__ == '__main__':
    a = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(a.exec_())
