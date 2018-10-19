from win10toast import ToastNotifier
import queue
from threading import Thread

q_distance = queue.Queue()
q_view = queue.Queue()
q_angle = queue.Queue()
q_angle_ot = queue.Queue()
q_blink = queue.Queue()

class Popup:
    def __init__(self):
        self.toaster = ToastNotifier()
    def notific_20_minutes(self):
        self.toaster.show_toast("TIME RISK",
            "you watching sceen over 20 minutes",
                icon_path="logo_eyeguard.ico",
                duration=8)
    def start_notific_20_minutes(self):
        th_20second = Thread(target=self.notific_20_minutes)
        th_20second.start()
    def notific_2_hours(self):
        self.toaster.show_toast("TIME RISK",
            "you watching sceen over 2 hours",
                icon_path="logo_eyeguard.ico",
                duration=8)
    def start_notific_2_hours(self):
        th_2hours = Thread(target=self.notific_2_hours)
        th_2hours.start()
    def notific_distance(self):
        item_distance=q_distance.get()
        item_view=q_view.get()
        self.toaster.show_toast("DISTANCE RISK",
            "you view {} screen {:.0f} cm".format(
                    item_view ,item_distance),
                icon_path="logo_eyeguard.ico",
                duration=2)
    def start_notific_distance(self,distance, view):
        q_distance.put(distance)
        q_view.put(view)
        th_dis = Thread(target=self.notific_distance)
        th_dis.start()
    def notific_angle(self):
        item_angel=q_angle.get()
        item_angel_ot=q_angle_ot.get()
        self.toaster.show_toast("ANGLE RISK",
            "you view {} screen {:.0f} degree".format(
                item_angel_ot ,item_angel),
                icon_path="logo_eyeguard.ico",
                duration=2)
    def start_notific_angle(self,angle, angle_ot):
        q_angle.put(angle)
        q_angle_ot.put(angle_ot)
        th_angle = Thread(target=self.notific_angle)
        th_angle.start()
    def notific_blink(self):
        blink_item = q_blink.get()
        popup.show_toast("BLINKINK RISK",
            "{} blink/min you blinkink less".format(blink_item),
            icon_path="logo_eyeguard.ico",
            duration=2)
    def start_anotific_blink(self):
        print("start threading")
        th_blink = Thread(target=self.notific_blink)
        th_blink.start()