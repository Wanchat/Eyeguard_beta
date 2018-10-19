import dlib
import cv2
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import os
import sys
import pyautogui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel,\
    QBoxLayout,QHBoxLayout,QGridLayout
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from style import Style

class Age:
    def __init__(self,model="age_50.model"):
        self.madel_age = load_model(model)
        self.alert = False
        self.frame = 0
    def gui_alert_age(self):
        pass
    def estimate_age(self, window_face):
        self.window_face = cv2.resize(window_face, (28, 28))
        self.window_face = self.window_face.astype("float") / 255.0
        self.window_face = img_to_array(self.window_face)
        self.window_face = np.expand_dims(self.window_face, axis=0)
        (self.under, self.older) = self.madel_age.predict(self.window_face)[0]
        self.label_age = "older40" if self.older > self.under else "under40"
        self.score_age = self.older if self.older > self.under else self.under
        return  self.label_age, self.score_age
    def chage_screen(self, age):
        if age != None:
            self.frame += 1
        else:
            if self.frame == 10:

                if age == "older40" :
                    pass
                else:
                    pass
        if self.alert == True :
            os.system("start ms-settings:display")
        else:
            pass


class Pip_alert_age(QWidget):

    def __init__(self, x):
        super().__init__()
        self.x = "You is age {} !".format(x)
        self.stylegui = Style()
        self.style = self.stylegui.initgui()
        self.setStyleSheet(self.style)
        self.title = 'CHANGE SCREEN'
        self.screen_wide, self.screen_high = pyautogui.size()
        self.screen_wide_c = self.screen_wide/2
        self.screen_high_c = self.screen_high /2
        self.width = 480
        self.height = 200
        self.left = self.screen_wide_c - (self.width/2)
        self.top = self.screen_high_c - (self.height/2)
        self.bt_width = 100
        self.bt_hight = 30
        self.bt_width_c = self.bt_width / 2
        self.pop_center_w = self.width / 2
        self.lb_1_width = 460
        self.lb_1_hight = 40
        self.lb_1_top = 80
        self.lb_1_left = 10
        self.lb_2_top = 40
        self.lb_2_left = 10
        self.text = "Do you want to active the screen?"
        self.initUI()
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(
            r'D:\code_python\Eyeguard\data\icon_eyeguard.png'))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setGeometry(self.left, self.top, self.width, self.height)
        label_1 = QLabel(self.text,self)
        label_1.setStyleSheet("font-size: 20px;")
        label_1.setAlignment(Qt.AlignCenter)
        label_1.resize(self.lb_1_width, self.lb_1_hight)
        label_1.move(self.lb_1_left, self.lb_1_top)
        label_2 = QLabel(self.x, self)
        label_2.resize(self.lb_1_width, self.lb_1_hight)
        label_2.move(self.lb_2_left, self.lb_2_top)
        label_2.setAlignment(Qt.AlignCenter)
        label_2.setStyleSheet("font-size: 30px;")
        bt_ok = QPushButton('OK',self)
        bt_cancel = QPushButton('CANCEL',self)
        bt_ok.resize(self.bt_width,self.bt_hight)
        bt_cancel.resize(self.bt_width,self.bt_hight)
        bt_ok.move(130, 140)
        bt_cancel.move(250, 140)
        bt_ok.clicked.connect(self.open_display)
        bt_cancel.clicked.connect(self.exit_popup)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.show()
    @pyqtSlot()
    def open_display(self):
        os.system("start ms-settings:display")
        sys.exit()
    def exit_popup(self):
        sys.exit()

if __name__ == '__main__':

    def chage_screen(age):
        if age == "older40" :
            app = QApplication(sys.argv)
            alert = Pip_alert_age(age)
            sys.exit(app.exec_())
        else:
            pass

    face_detect = cv2.CascadeClassifier(
            "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)
    age_class = Age()
    frame_number = 0
    Older = ''
    while True:
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
            face_n = frame[y:y + h, x:x + w]  # Cut face
            try:
                if frame_number == 1:  # Use first frame for age
                    Older = age_class.estimate_age(face_n)  # Prediction age function
            except:
                pass
        older = Older[0] # Extract older from older class
        print(Older)
        chage_screen(older) # Function change screen
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
