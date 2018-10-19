from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QPushButton, QFrame, \
    QGraphicsDropShadowEffect
from PyQt5.QtGui import QIcon, QPainter, QPixmap
from PyQt5.QtCore import Qt
import sys
import cv2, numpy as np
from queue import Queue
import time
from detection_factors.extend_eye import Extand_eyes
from detection_factors.extend_face_haar import Extend_face_haar
from detection_factors.popup import Popup
from detection_factors.factor_time import Time_detect_rule
from detection_factors.factor_angle import Angle
from detection_factors.factor_distance import Distance
from detection_factors.factor_blink import Blink_cnn, Blinking
from detection_factors.factor_sex import Sex
from detection_factors.factor_older import Age
from detection_factors.factor_brightness import Brightness

# My App =================================================================
class Myapp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.kill_camera = False

        # backend ========================================================
        self.frame_num = 0
        # self.xywh =None
        self.seconds_timeout =None
        self.frame = None
        self.rightEye = None
        self.leftEye = None
        self.blink = None
        self.c = True

        # ================================================================
        self.style = """
                        color: #4d4d4d;  font-family: Prompt; font-size: 14px;
                        padding: 48px;
                        """
        self.style_label_function = """
                        color: white; font-size: 11px; font-family: Arial;
                        background-color: transparent; padding: 1px;

                        """
        self.setGeometry(100, 100, 440, 500)
        self.setStyleSheet("border-color: white")
        self.setWindowTitle("Eyeguard")
        self.setWindowIcon(QIcon(r'image\icon_eyeguard.png'))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        self.label_frame = QLabel(self) # Label show frame numbers camera
        self.frame_factor = QFrame(self) # Frame factors
        self.frame_factor.setGeometry(30, 90, 380, 380)
        self.tab_top = QFrame(self) # Top tap
        self.imageGround = QFrame(self)  # Background image first page
        self.logoGround = QLabel(self.imageGround)  # Background image logo first page

        self.btn_start = QPushButton(self.tab_top)  # Button start
        self.bt_time = QPushButton(self.frame_factor)  # Button time factor
        self.bt_blink = QPushButton(self.frame_factor)  # Button blink factor
        self.bt_angle = QPushButton(self.frame_factor)  # Button angle factor
        self.bt_dis = QPushButton(self.frame_factor)  # Button distance factor
        self.bt_sex = QPushButton(self.frame_factor)  # Button sex factor
        self.bt_older = QPushButton(self.frame_factor)  # Button older factor
        self.bt_bright = QPushButton(self.frame_factor)  # Button bright factor


        self.bt_factor =[
            self.bt_time,
            self.bt_blink,
            self.bt_angle,
            self.bt_dis,
            self.bt_sex,
            self.bt_older,
            self.bt_bright]
        self.tex_time = QLabel(self.bt_time)
        self.tex_blink = QLabel(self.bt_blink)
        self.tex_angle = QLabel(self.bt_angle)
        self.tex_dis = QLabel(self.bt_dis)
        self.tex_sex = QLabel(self.bt_sex)
        self.tex_older = QLabel(self.bt_older)
        self.tex_bright = QLabel(self.bt_bright)

        y = 55
        self.tab_time(0)
        self.tab_blink(y)
        self.tab_angle(y*2)
        self.tab_dis(y*3)
        self.tab_sex(y*4)
        self.tab_older(y*5)
        self.tab_bright(y*6)

        self.stop_close_button = ''  # signal on off (show camera)
        self.close_app = False

        self.image_property()  # Image icon button
        self.shadow_property()  # Shadow button factor
        self.initGUI()
        self.call() # Call function in loop frame
        self.import_class_factors() # Import class

    def change(self,e):
        if e:
            self.c = False
        else:
            self.c =True

    def import_class_factors(self):
        self.model_path = "blink.model"
        self.extend_eye_point = Extand_eyes()
        self.extend_faceHaar = Extend_face_haar()
        self.popup_class = Popup()
        # self.time_class = Time_detect_rule()
        self.angle_class = Angle()
        self.distance_class = Distance()
        # self.blink_cnn = Blink_cnn(self.model_path)
        # self.blinking = Blinking(2)
        self.sex_class = Sex()
        self.age_class = Age()
        self.bright_class = Brightness()
        pass

    def call(self):
        self.call_time = None
        self.call_blink = None
        self.call_angle = None
        self.call_distance = None
        self.call_sex = None
        self.call_older = None
        self.call_bright = None

    # GUI =========================================================================
    def initGUI(self):
        self.tab_top.setGeometry(0, 0, 440, 60)
        self.tab_top.setStyleSheet("background-color: black;")
        self.imageGround.setGeometry(0, 60, 440, 440)
        self.imageGround.setStyleSheet("background-color: #0086FF;")
        self.logoGround.setGeometry(140, 140, 160, 160)
        self.logoGround.setPixmap(QPixmap(r'image\background_2.png'))
        # self.frame_factor.hide()
        self.image_function()
        self.btn_function()
        self.label_function()
    def btn_function(self):
        self.btn_start.setGeometry(360, 15, 59, 30)
        self.btn_start.setStyleSheet("""
                QPushButton{border-image: url('image/btOFF.png');}
                QPushButton:hover{border-image: url('image/btOFF_hover.png');}
                """)
        self.btn_start.show()
        self.btn_start.setCheckable(True)
        self.btn_start.clicked[bool].connect(self.event_start_stop)
    def image_function(self):
        self.imag_c = QLabel(self.tab_top)
        self.imag_c.setPixmap(QPixmap(r'image/logo-c.png'))
        self.imag_c.setGeometry(5, 0, 60, 60)
        self.image_name = QLabel(self.tab_top)
        self.image_name.setPixmap(QPixmap(r'image/band.png'))
        self.image_name.setGeometry(65, 8, 80, 30)
    def label_function(self):
        self.l_name = QLabel(self.tab_top)
        self.l_name.setText("Detection Risk Factors of Computer Vision Syndrome")
        self.l_name.setGeometry(65, 30, 260, 30)
        self.l_name.setStyleSheet(self.style_label_function)
    def btn(self, parent, x, y, w, h):
        new_btn = QPushButton(parent)
        new_btn.setGeometry(x, y, w, h)
        return new_btn
    def tab_time(self, y):
        self.bt_time.setGeometry(0, y, 380, 48)
        self.tex_time.setGeometry(0, 0, 332, 48)
        self.tex_time.setStyleSheet(self.style)
        # self.tex_time.setText("")
    def tab_blink(self, y):
        self.bt_blink.setGeometry(0, y, 380, 48)
        self.tex_blink.setGeometry(0, 0, 332, 48)
        self.tex_blink.setStyleSheet(self.style)
        self.tex_blink.setText("")
    def tab_angle(self, y):
        self.bt_angle.setGeometry(0, y, 380, 48)
        self.tex_angle.setGeometry(0, 0, 332, 48)
        self.tex_angle.setStyleSheet(self.style)
        self.tex_angle.setText("")
    def tab_dis(self, y):
        self.bt_dis.setGeometry(0, y, 380, 48)
        self.tex_dis.setGeometry(0, 0, 332, 48)
        self.tex_dis.setStyleSheet(self.style)
        self.tex_dis.setText("")
    def tab_sex(self, y):
        self.bt_sex.setGeometry(0, y, 380, 48)
        self.tex_sex.setGeometry(0, 0, 332, 48)
        self.tex_sex.setStyleSheet(self.style)
        self.tex_sex.setText("")
    def tab_older(self, y):
        self.bt_older.setGeometry(0, y, 380, 48)
        self.tex_older.setGeometry(0, 0, 332, 48)
        self.tex_older.setStyleSheet(self.style)
        self.tex_older.setText("")
    def tab_bright(self, y):
        self.bt_bright.setGeometry(0, y, 380, 48)
        self.tex_bright.setGeometry(0, 0, 332, 48)
        self.tex_bright.setStyleSheet(self.style)
        self.tex_bright.setText("")

    def image_value(self, icon, parent): # Image icon function
        image = QLabel(parent)
        image.setGeometry(6.5, 0, 48, 48)
        image.setPixmap(QPixmap(icon))

    def image_property(self):
        image_icon = ["time_on", # Make list icon name
                      "blink_on",
                      "angle_on",
                      "dis_on",
                      "sex_on",
                      "older_on",
                      "bright_on"]

        icon = [r'image\{}.png'.format(icon) for icon in image_icon] # Call path icon

        for i, j in enumerate(icon):
            self.image_value(j, self.bt_factor[i]) # Loop icon image in bt_factors

    def shadow_property(self): # Make function shadows to bt_factor
        for i in self.bt_factor:
            i.setGraphicsEffect(self.shadow_1(5))

    def shadow_1(self, value): # Shadow function
        self.shadow1 = QGraphicsDropShadowEffect(self)
        self.shadow1.setBlurRadius(value)
        self.shadow1.setXOffset(0)
        self.shadow1.setYOffset(0)
        return self.shadow1

    def count_frame(self, frame): # Count frame to label_frame(setText) function
        self.label_frame.setGeometry(7, 500 - 20, 400, 20)
        self.label_frame.setStyleSheet("font-size: 10px")
        self.label_frame.setText(frame)
        return frame

# Def factor =============================================================
            #=============================================================
    def time_def(self):
        time_out = None
        time_out = self.time_class.time_detection(self.xywh)
        minutes_timeout = time_out[2]
        hours_timeout = time_out[3]
        if minutes_timeout == True:
            self.popup_class.start_notific_20_minutes()
        if hours_timeout == True:
            self.popup_class.start_notific_2_hours()
        try:
            timeset = 'You watching screen {}:{:.2f}'.format(time_out[0],
                                                             time_out[1])
            self.tex_time.setText(timeset)
        except:
            pass
        print(timeset)


    def blink_def(self):
        if self.status_face == "face":
            if self.blink_seconds == 0:
                self.blinking.alert_eye_blinking(self.blink)
        self.blink_extend = self.blink_cnn.extend_eyes(self.frame,
                                                       self.rightEye,
                                                       self.leftEye)
        self.blink_pre = self.blink_cnn.pre_process(self.blink_extend)
        self.blink_classify = self.blink_cnn.classify_blink(self.blink_pre)
        self.blink_count = self.blinking.predict_eye_blinking(
                                        self.blink_classify)
        self.blink_seconds = self.blink_count[0]
        self.blink = self.blink_count[2]

        blinkset = "You blinking less {}/min".format(self.blink)
        print(self.blink_seconds,blinkset)
        return

        # self.tex_blink.setText(blinkset)

    def angle_def(self):
        print("Angle active")
        if self.alertSent_4_sec == True:
            if self.status_face == "face":
                if self.angle > 9 and self.angle_on_top=="TOP":
                   pass
                else:
                    self.popup_class.start_notific_angle(
                            self.angle, self.angle_on_top)
        self.angle = self.angle_class.estimate_angle(self.point_center_y)
        self.angle_on_top = self.angle_class.down_top(self.point_center_y)
        angleset = 'You have view {} {} degree'.format(
                self.angle_on_top, self.angle)
        self.tex_angle.setText(angleset)

    def distance_def(self):
        print("Distance active")
        if self.alertSent_3_sec == True:
            if self.status_face == "face":
                if 50 <= self.distance <= 70:
                    pass
                else:
                    self.popup_class.start_notific_distance(
                            self.distance, self.pos_view)
        self.angle = self.angle_class.estimate_angle(self.point_center_y)
        self.distance = self.distance_class.estimate_distance(
                            self.angle, self.point_center_x,
                            self.point_center_y, self.center_right_x)
        if self.distance < 50:
            self.pos_view = "near"
        elif 50 <= self.distance < 70:
            self.pos_view = "good"
        else:
            self.pos_view = "long"
        distanceset = "You have view {} {} cm".format(self.pos_view,
                                                    self.distance)
        self.tex_dis.setText(distanceset)

    def sex_def(self):
        print("Sex active")
        sex = self.sex_class.estimate_sex(self.face_window)
        sexsent = "You is {} ".format(sex)
        print(sexsent)
        self.tex_sex.setText(sex)

    def older_def(self):
        print("Older active")
        older = self.age_class.estimate_age(self.face_window)
        oldersent = "You is {} ".format(older)
        print(oldersent)
        self.tex_older.setText(oldersent)

    def bright_def(self):
        print("Bright active")
        self.array = self.bright.array_gray(self.gray)  # Avg black white
        self.bright_if = self.bright.brightness(self.array)  # bright screen vs light avg
        self.bright.change_screen(self.bright_if)  # Change screen display
        brightsent = "bright: {} screen: {}".format(self.bright_if, self.array)
        print(brightsent)
        self.tex_bright.setText(brightsent)

    # Any Event ============================================================
    def event_start_stop(self, event):  # Event start camera and system
        if event:
            print("start")
            self.btn_start.setStyleSheet("""
                            QPushButton{border-image: url('image/btON.png');}
                            """)
            self.imageGround.hide()
            self.frame_factor.show()
            self.kill_camera = False #  camera
            for setTure in self.bt_factor: # Loop set button True
                setTure.setCheckable(True)
            self.list_active = [
                self.active_time,
                self.active_blink,
                self.active_angle,
                self.active_dis,
                self.active_sex,
                self.active_older,
                self.active_bright]  # Build list active for loop
            for bt in range(len(self.list_active)): # Looop click button
                self.bt_factor[bt].clicked[bool].connect(self.list_active[bt])
            self.tex_factor = [
                self.tex_time,
                self.tex_blink,
                self.tex_angle,
                self.tex_dis,
                self.tex_sex,
                self.tex_older,
                self.tex_bright] # Build text_factors list
            for setText in self.tex_factor: # Loop setText tab = ''
                setText.setText("")
            self.camera_open() # Start camera when click button start
        else:
            print("stop")
            self.btn_start.setStyleSheet("""
                            QPushButton{border-image: url('image/btOFF.png');}
                            QPushButton:hover{border-image: url('image/btOFF_hover.png');}
                            """)
            self.imageGround.show()
            self.frame_factor.hide()
            self.kill_camera = True
            self.call_time = False
            self.call_blink = False
            self.call_angle = False
            self.call_distance = False
            self.call_sex = False
            self.call_older = False
            self.call_bright = False

            self.blink = 0

            for setFalse in self.bt_factor: # Loop set button False
                setFalse.setCheckable(False)
    def active_time(self, event):
        if event:
            self.call_time = True
        else:
            self.call_time = False
            self.tex_time.setText("")
    def active_blink(self, event):
        if event:
            self.call_blink = True
        else:
            self.blink = 0
            self.call_blink = False
            self.tex_blink.setText("")
    def active_angle(self, event):
        if event:
            self.call_angle = True
            self.tex_angle.setText("angle_on")
        else:
            self.call_angle = False
            self.tex_angle.setText("")
    def active_dis(self, event):
        if event:
            self.call_distance = True
            self.tex_dis.setText("distance_on")
        else:
            self.call_distance = False
            self.tex_dis.setText("")
    def active_sex(self, event):
        if event:
            self.call_sex = True
            self.tex_sex.setText("sex_on")
        else:
            self.call_sex = False
            self.tex_sex.setText("")
    def active_older(self, event):
        if event:
            self.call_older = True
            self.tex_older.setText("older_on")
        else:
            self.call_older = False
            self.tex_older.setText("")
    def active_bright(self, event):
        if event:
            self.call_bright = True
            self.tex_bright.setText("bright_on")
        else:
            self.call_bright = False
            self.tex_bright.setText("")

    # Camera <===================================================================
    # ===========================================================================

    def camera_open(self):

        cap = cv2.VideoCapture(0)

        self.blink_cnn = Blink_cnn(self.model_path)
        self.blinking = Blinking(2)
        self.time_class = Time_detect_rule()
        self.time_start_60 = time.time()
        self.time_start_3 = time.time()
        self.time_start_4 = time.time()
        self.minutes = 0
        self.second_60 = 0
        self.second_3 = 0
        self.second_4 = 0
        self.every_3_seconds = 0
        self.every_4_seconds = 0
        self.status_face = ''
        self.checkminutes = 0
        self.alertSent_3_sec = False
        self.alertSent_4_sec = False
        self.alertSent_1_min = False

        self.reset_blink = False

        while (not self.kill_camera):
            self.blink_seconds =None

            self.xywh = None
            self.alertSent_3_sec = False
            self.alertSent_4_sec = False
            self.alertSent_1_min = False  # Reset alert time 1 min

            self.count_frame('{}:{:.2f}'.format(self.minutes,self.second_60))  # Status
            _, self.frame = cap.read()
            self.frame_num += 1  # Frame _number
            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)  # Image gray

            self.eye_point = self.extend_eye_point.extend(self.gray)  # <== Extend_eye
            try:
                self.center_right_x = self.eye_point["center_right_x"]
                self.center_right_y = self.eye_point["center_right_y"]
                self.center_left_x = self.eye_point["center_left_x"]
                self.center_left_y = self.eye_point["center_left_y"]
                self.point_center_x = self.eye_point["point_center_x"]
                self.point_center_y = self.eye_point["point_center_y"]
                self.rightEye = self.eye_point["rightEye"]
                self.leftEye = self.eye_point["leftEye"]
                self.xywh = self.extend_faceHaar.extend_face(self.gray)
                self.face_window = self.extend_faceHaar.window_face(
                                                        self.xywh, self.frame) # <== Extend face window
                self.status_face = "face"  # <== Check status face
                print("face ===========================")
            except:
                self.status_face = "no face"  # Check status no face
                print("no face ===========================")


            self.second_3 = time.time() - self.time_start_3  # Check time make 3 second
            self.second_4 = time.time() - self.time_start_4  # Check time make 4 second
            self.second_60 = time.time() - self.time_start_60  # Check time make 60 second

            if self.second_3 > 3:  # Make alert 3 self.second_60 *****
                self.every_3_seconds += 1
                if self.every_3_seconds % 1 == 0:
                    self.alertSent_3_sec = True

                self.time_start_3 = time.time()

            if self.second_4 > 4:  # Make alert 3 self.second_60 *****
                self.every_4_seconds += 1
                if self.every_4_seconds % 1 == 0:
                    self.alertSent_4_sec = True

                self.time_start_4 = time.time()

            if self.second_60 > 60:  # Make self.minutes reset self.second_60 set alert time *****
                self.minutes += 1
                if self.minutes % 1 == 0:
                    self.alertSent_1_min = True

                # self.second_60 = 0
                self.time_start_60 = time.time()

            if self.call_time == True:
                self.time_def()
            if self.call_blink == True:
                self.blink_def()
            if self.call_angle == True:
                self.angle_def()
            if self.call_distance == True:
                self.distance_def()
            if self.call_sex == True:
                self.sex_def()
            if self.call_older == True:
                self.older_def()
            if self.call_bright == True:
                self.bright_def()
            cv2.imshow('CAMERA', self.frame)
            if cv2.waitKey(1) == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    def ex(self):
        QApplication.exit()
        self.kill_camera = True
        print("application ====================== exit ")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Myapp()
    main.show()
    app.exec_()
    main.ex()
