import cv2
from helper.extend_eye import Extand_eyes
import numpy as np
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import time
from queue import Queue
from win10toast import ToastNotifier
import imutils
import sys
import os
from threading import Thread

q_risk = Queue()
q_blilnk = Queue()
popup = ToastNotifier()
q_blink = Queue()

class Blink_cnn:

    def __init__(self, model_blink):
        self.model_blink = load_model(model_blink)
        self.window_right = None
        self.window_left = None
        self.closedeyes_right = None
        self.openeyes_right = None
        self.closedeyes_left = None
        self.openeyes_left = None
        self.label = None
        self.label_2 = None
        self.eye_predict = None
    def extend_eyes(self, image, rightEye, leftEye):
        self.image = image
        self.rightEye = rightEye
        self.leftEye = leftEye
        self.right_0_x, self.right_0_y = self.rightEye[0]
        self.right_1_x, self.right_1_y = self.rightEye[1]
        self.right_3_x, self.right_3_y = self.rightEye[3]
        self.right_4_x, self.right_4_y = self.rightEye[4]
        self.left_0_x, self.left_0_y = self.leftEye[0]
        self.left_1_x, self.left_1_y = self.leftEye[1]
        self.left_3_x, self.left_3_y = self.leftEye[3]
        self.left_4_x, self.left_4_y = self.leftEye[4]
        self.window_right = self.image[
                       self.right_1_y - 5: self.right_4_y + 5,
                       self.right_0_x - 5: self.right_3_x + 5]
        self.window_left = self.image[
                      self.left_1_y - 5: self.left_4_y + 5,
                      self.left_0_x - 5: self.left_3_x + 5]
        return  self.window_right, self.window_left
    def pre_process(self, window_eye):
        self.window_right_pre = cv2.resize(window_eye[0], (28, 28))
        self.window_right_pre = self.window_right_pre.astype("float") / 255.0
        self.window_right_pre = img_to_array(self.window_right_pre)
        self.window_right_pre = np.expand_dims(self.window_right_pre, axis=0)
        self.window_left_pre = cv2.resize(window_eye[1], (28, 28))
        self.window_left_pre = self.window_left_pre.astype("float") / 255.0
        self.window_left_pre = img_to_array(self.window_left_pre)
        self.window_left_pre = np.expand_dims(self.window_left_pre, axis=0)
        return self.window_right_pre, self.window_left_pre

    def classify_blink(self, window_pre):
        (self.closedeyes_right,self.openeyes_right) = \
            self.model_blink.predict(window_pre[0])[0]
        (self.closedeyes_left,self.openeyes_left) = \
            self.model_blink.predict(window_pre[1])[0]
        if self.openeyes_right > self.closedeyes_right:
            self.label = "openeyes_right"
            self.score = self.openeyes_right
        else:
            self.label = "closedeyes_right"
            self.score = self.closedeyes_right
        if self.openeyes_left > self.closedeyes_left:
            self.label_2 = "openeyes_left"
            self.score_2 = self.openeyes_left
        else:
            self.label_2 = "closedeyes_left"
            self.score_2 = self.closedeyes_left
        if self.label == "openeyes_right" and self.label_2 == "openeyes_left":
                self.eye_predict = "openeyes"
        else:
            self.eye_predict = "closedeyes"
        return self.eye_predict

class Blinking:
    def __init__(self, blink_frame = 3):
        self.blink_frame = blink_frame
        self.blink_counter_frame = 0
        self.blink_total = 0
        self.blink_total_reset = 0
        self.blink_alert = False
        self.alert_count = 0
        self.blink_min = ''
        self.start_time_blink = time.time()
        self.minutes_blink = 0
        self.seconds_blink = 0

    def predict_eye_blinking(self, eye_predict):
        self.eye=eye_predict
        if self.eye == "closedeyes": # Check blink from close eyes
            self.blink_counter_frame += 1
        else:
            if self.blink_counter_frame >= self.blink_frame: # Check frame blink
                self.blink_total += 1
                self.blink_total_reset += 1
            self.blink_counter_frame = 0
        self.seconds_blink = time.time() - self.start_time_blink
        if self.seconds_blink > 60 : # Second time 60 minutes
            self.blink_total_reset = 0
            self.seconds_blink = 0
            self.start_time_blink = time.time()
        return self.seconds_blink, self.blink_total, self.blink_total_reset

    def alert_eye_blinking(self, blink_per_minutes, sex="man"):
        self.blink_per_minutes=blink_per_minutes # Blink per second
        self.sex = sex
        self.alert_risk_blink = False # Set default alert
        if self.sex == "man": # Check man or woman
            self.blink_min = 20
        else:
            self.blink_min = 30
        if self.blink_per_minutes < self.blink_min : #Check risk and alert
            print('time alert')
            print("blinking RISK!")
            self.alert_risk_blink = True
            q_blink.put(self.blink_per_minutes) # Start popup
            self.start_notific_blink()
        else:
            pass
        return

    def notific_blink(self): # Popup function
        blink_item = q_blink.get()
        popup.show_toast("BLINKINK RISK",
            "{} blink/min you blinkink less".format(blink_item),
            icon_path= r"..\data\logo_eyeguard.ico",
            duration=2)

    def start_notific_blink(self): # Start threading popup
        print("start threading")
        play_test = Thread(target=self.notific_blink)
        play_test.start()


if __name__ == '__main__':
    from threading import Thread
    from queue import Queue
    from win10toast import ToastNotifier

    q_risk = Queue()
    q_blilnk = Queue()
    popup = ToastNotifier()

    model_path= r"..\data\blink.model"
    extend_eye_point = Extand_eyes()
    blink_cnn = Blink_cnn(model_path)
    blinking = Blinking()
    cap = cv2.VideoCapture(0)

    def play_frame():
        frame_num = 0
        second = 0
        minutes = False
        start_time = time.time()
        blink_count = None
        blink_classify = None
        face_status = None

        while True:
            minutes = False
            _, frame = cap.read()
            second = time.time() - start_time
            if second > 60:
                print(" 1 ==================== minutes ")
                minutes = True
                start_time = time.time()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            eye_point = extend_eye_point.extend(gray)
            if minutes == True and face_status == 'face':
                blinking.alert_eye_blinking(blink_count[1])
            try:
                rightEye = eye_point["rightEye"]
                leftEye = eye_point["leftEye"]
                blink_extend = blink_cnn.extend_eyes(frame, rightEye, leftEye)
                blink_pre = blink_cnn.pre_process(blink_extend)
                blink_classify = blink_cnn.classify_blink(blink_pre)
                face_status = 'face'
            except:
                face_status = 'no face'
            blink_count = blinking.predict_eye_blinking(blink_classify)
            print('{} >> {}'.format(face_status, blink_count))
            if cv2.getWindowProperty('frame', 1) == -1:
                break
        cap.release()
        cv2.destroyAllWindows()
    play_frame()