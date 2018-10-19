import cv2, numpy as np
from extend_face_haar import Extend_face_haar
import time

class Time_detect:
    def __init__(self,time_reset=5):
        self.day = 0
        self.hour = 0
        self.minutes = 0
        self.second = 0
        self.hour_15 = 0
        self.minutes_15 = 0
        self.second_15 = 0
        self.day_not_face = 0
        self.hour_not_face = 0
        self.minutes_not_face = 0
        self.second_not_face = 0
        self.start = time.time()
        self.start_not_face = time.time()
        self.time_reset = time_reset
        self.m = 0
    def time_detection(self, xywh):
        if xywh!= None:
            self.second = time.time() - self.start
            if self.second >= 60:
                self.minutes += 1
                self.second = 0
                self.start = time.time()
            if self.minutes >= 60:
                self.hour += 1
                self.minutes = 0
            if self.hour >= 24:
                self.day += 1
                self.hour = 0
            self.start_not_face = time.time()

        else:
            self.second_not_face = time.time() - self.start_not_face
            if self.second_not_face >= 60:
                self.minutes_not_face += 1
                self.second_not_face = 0
                self.start_not_face = time.time()
            if self.minutes_not_face >= 60:
                self.hour_not_face += 1
                self.minutes_not_face = 0
            if self.hour_not_face >= 24:
                self.day_not_face += 1
                self.hour_not_face = 0
                # self.start = time.time()
            if self.second_not_face > self.time_reset:
                self.start = time.time()
        return self.minutes,\
               self.second, \
               self.minutes_not_face, \
               self.second_not_face, \



class Time_detect_rule:
    def __init__(self,time_reset=5):
        self.day = 0
        self.hour = 0
        self.minutes = 0
        self.second = 0
        self.hour_15 = 0
        self.minutes_15 = 0
        self.second_15 = 0
        self.day_not_face = 0
        self.hour_not_face = 0
        self.minutes_not_face = 0
        self.second_not_face = 0
        self.start = time.time()
        self.start_not_face = time.time()
        self.time_reset = time_reset
        self.second_alert = 0
        self.second_20_alert = False
        self.hour_2_alert = False

    # def stay_time(self, timeface, nottimeface):
    #     self.start = timeface
    #     self.start_not_face = nottimeface

    def time_detection(self, xywh):
        if xywh != None:
            self.hour_2_alert = False
            self.second_20_alert = False
            self.second = time.time() - self.start
            if self.second > 60:
                self.minutes += 1
                self.second_alert += 1
                if self.second_alert % 1 == 0:
                    print("alert ================= 20 minutes")
                    self.second_20_alert = True
                if self.second_alert % 121 == 0:
                    print("alert ================= 2 hours")
                    self.hour_2_alert = True
                self.second = 0
                self.start = time.time()
            self.start_not_face = time.time()

        else:
            self.second_not_face = time.time() - self.start_not_face
            if self.second_not_face > 60:
                self.minutes_not_face += 1
                self.second_not_face = 0
                self.start_not_face = time.time()
            if self.second_not_face > self.time_reset:
                self.start = time.time()

        return self.minutes, self.second ,self.second_20_alert, self.hour_2_alert

if __name__ == '__main__':
    from win10toast import ToastNotifier
    import queue
    from threading import Thread

    toaster = ToastNotifier()
    q_seconds = queue.Queue()
    q_hours = queue.Queue()
    cap = cv2.VideoCapture(0)
    ex = Extend_face_haar()
    t = Time_detect_rule()
    def notific_20_minutes():
        toaster.show_toast("TIME RISK",
            "you watching sceen over 20 minutes",
                icon_path="logo_eyeguard.ico",
                duration=8)
    def start_notific_20_minutes():
        th_20second = Thread(target=notific_20_minutes)
        th_20second.start()
    def notific_2_hours():
        toaster.show_toast("TIME RISK",
            "you watching sceen over 2 hours",
                icon_path="logo_eyeguard.ico",
                duration=8)
    def start_notific_2_hours():
        th_2hours = Thread(target=notific_20_minutes)
        th_2hours.start()
    def app_test():
        while True:
            _, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            xywh = ex.extend_face(gray)

            time_out = t.time_detection(xywh)
            seconds_timeout = time_out[2]
            hours_timeout = time_out[3]
            if seconds_timeout == True:
                start_notific_20_minutes()
            if hours_timeout == True:
                start_notific_2_hours()

            print("{:.2f} {:.2f} ".format(time_out[0],time_out[1]))
            cv2.imshow("frame", frame)
            cv2.waitKey(1)
            if cv2.getWindowProperty('frame', 1) == -1:
                break
        cap.release()
        cv2.destroyAllWindows()
    app_test()