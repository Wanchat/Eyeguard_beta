import math
from math_eyeguarde import Math_eyeguarde
from canculator_angle import Pixel_to_Angle
from extend_eye import Extand_eyes
import cv2

class Angle:
    def __init__(self):
        self.angle_prediction = Pixel_to_Angle()
    def estimate_angle(self, point_center_y): # cale angle camera
        self.point = self.angle_prediction.px_plus(point_center_y)
        self.estimate_angle_new = self.angle_prediction.px_to_degree(self.point)
        return self.estimate_angle_new
    def down_top(self, point):
        self.o_or_t = self.angle_prediction.d_or_e(point)
        return self.o_or_t
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
                                  abs(point_center_y - 240)) * 180 / math.pi
        # cale line Ad cm
        self.line_AD = self.math_eye.tanRounded(abs(90 - self.angle_B)) * est
        # cale distance
        self.estimate_distance_new = self.math_eye.tanRounded(
            abs(90 - estimate_angle)) * self.line_AD

        return self.estimate_distance_new
    def alert_distance(self, distance):
        if 50 < distance <= 80:
            return True
        else:
            return False


if __name__ == '__main__':

    import time
    from win10toast import ToastNotifier
    import queue
    from threading import Thread

    q_angle = queue.Queue()
    q_angle_ot = queue.Queue()
    toaster = ToastNotifier()
    extand_eyes_class = Extand_eyes()
    angle_class = Angle()
    distance_class = Distance()
    cap = cv2.VideoCapture(0)

    def notific():
        item_angel=q_angle.get()
        item_angel_ot=q_angle_ot.get()
        toaster.show_toast("ANGLE RISK",
            "you view {} screen {:.0f} degree".format(
                item_angel_ot ,item_angel),
                icon_path="logo_eyeguard.ico",
                duration=2)
    def start_notific(angle, angle_ot):
        q_angle.put(angle)
        q_angle_ot.put(angle_ot)
        th = Thread(target=notific)
        th.start()
    def app_test():
        start_time = time.time()
        status_face = ''
        angle_on_top = ''
        angle = 0
        while True:
            success, frame = cap.read()
            second_3 = time.time() - start_time
            if second_3 > 3: # Check 3 second
                print("3 second =====================")
                if status_face == "face": # Check face
                    print("face =========================")
                    if angle>9 and angle_on_top=="TOP": # Check rule of angle
                        pass
                    else:
                        print("alert ========================") # If not rule of angle
                        start_notific(angle, angle_on_top)
                second_3 = 0 # Reset time 3 second
                start_time = time.time()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            image = extand_eyes_class.extend(gray)
            try:
                point_center_x = image["point_center_x"]
                point_center_y = image["point_center_y"]
                center_right_x = image["center_right_x"]
                angle = angle_class.estimate_angle(point_center_y)
                angle_on_top = angle_class.down_top(point_center_y)
                status_face = "face"
            except:
                status_face = "not face"
                angle_on_top = ''
                angle = ''
            print("{} {} {}".format(status_face, angle_on_top, angle))
            cv2.imshow("Frame", frame)
            cv2.waitKey(1)
            if cv2.getWindowProperty('Frame', 1) == -1:
                break
        cap.release()
        cv2.destroyAllWindows()
    app_test()

