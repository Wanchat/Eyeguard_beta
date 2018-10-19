from math_eyeguarde import Math_eyeguarde
from canculator_angle import Pixel_to_Angle
from extend_eye import Extand_eyes
import math
import cv2
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from threading import Thread
from queue import Queue
from win10toast import ToastNotifier

class Angle:
    def __init__(self):
        self.angle_prediction = Pixel_to_Angle()
    # cale angle camera
    def estimate_angle(self, point_center_y):
        self.point = self.angle_prediction.px_plus(point_center_y)
        self.estimate_angle_new = self.angle_prediction.px_to_degree(self.point)
        return self.estimate_angle_new
class Distance():
    def __init__(self):
        self.math_eye = Math_eyeguarde()
    # estimate_distance
    def estimate_distance(self, estimate_angle,
                            point_center_x,
                            point_center_y,
                            center_right_x,
                            est=2.6):
        # calc angle B
        self.angle_B = math.atan2(abs(point_center_x - center_right_x),
                                  abs(point_center_y - 240))*180/math.pi
        # cale line Ad cm
        self.line_AD = self.math_eye.tanRounded(abs(90 - self.angle_B))*est
        # cale distance
        self.estimate_distance_new = self.math_eye.tanRounded(
                                        abs(90 - estimate_angle))*self.line_AD
        return self.estimate_distance_new


if __name__ == '__main__':

    import time
    from win10toast import ToastNotifier
    import queue
    from threading import Thread

    q_distance = queue.Queue()
    q_view= queue.Queue()

    toaster = ToastNotifier()
    extand_eyes_class = Extand_eyes()
    angle_class = Angle()
    distance_class = Distance()
    cap = cv2.VideoCapture(0)

    def notific_distance():
        item_distance=q_distance.get()
        item_view=q_view.get()
        toaster.show_toast("DISTANCE RISK",
            "you view {} screen {:.0f} cm".format(
                    item_view ,item_distance),
                icon_path="logo_eyeguard.ico",
                duration=2)
    def start_notific_distance(distance, view):
        q_distance.put(distance)
        q_view.put(view)
        th = Thread(target=notific_distance)
        th.start()
    def app_test():
        start_time = time.time()
        status_face = ''
        distance = 0
        view_pos = ''
        while True:
            success, frame = cap.read()
            second_3 = time.time() - start_time
            if second_3 > 3:
                print("3 second =====================")
                if status_face == 'face':
                    print("face =========================")
                    if 50 <= distance <= 70:
                        pass
                    else:
                        print("alert ========================")
                        start_notific_distance(distance, view_pos)
                second_3 = 0
                start_time = time.time()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            image = extand_eyes_class.extend(gray)
            try:
                status_face = "face"
                point_center_x = image["point_center_x"]
                point_center_y = image["point_center_y"]
                center_right_x = image["center_right_x"]
                angle = angle_class.estimate_angle(point_center_y)
                distance = distance_class.estimate_distance(
                                            angle,point_center_x,
                                            point_center_y,center_right_x)
                if distance < 50:
                    view_pos = "near"
                elif 50 <= distance < 70:
                    view_pos = "good"
                else:
                    view_pos = "long"
            except:
                distance = ''
                view_pos = ''
                status_face = "not face"
            print('{} {} {}'.format(status_face, distance, view_pos))
            cv2.imshow("Frame", frame)
            cv2.waitKey(1)
            if cv2.getWindowProperty('Frame', 1) == -1:
                break
        cap.release()
        cv2.destroyAllWindows()
    app_test()