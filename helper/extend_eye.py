from imutils import  face_utils
import dlib
import cv2
import math
from math_eyeguarde import Math_eyeguarde
from canculator_angle import Pixel_to_Angle
import numpy as np

class Extand_eyes:
    def __init__(self):
        self.math_eye = Math_eyeguarde()
        self.angle_prediction = Pixel_to_Angle()

        # dlib function call model
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(r'..\data\shape_predictor_68_face_landmarks.dat')

        # indexes facial landmarks
        (self.left_eye_Start, self.left_eye_End) = \
            face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.right_eye_Start, self.right_eye_End) = \
            face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# extend from dlib point
    def extend(self,image_gray):
        self.detect_from_model = self.detector(image_gray, 0)

        for self.rect in self.detect_from_model:
            # detect & convert numpy
            self.shape = self.predictor(image_gray, self.rect)
            self.shape = face_utils.shape_to_np(self.shape)

            # extend for eye aspect ratio
            self.leftEye = self.shape[self.left_eye_Start: self.left_eye_End]
            self.rightEye = self.shape[self.right_eye_Start: self.right_eye_End]

            self.right_x_0, self.right_y_0 = self.rightEye[0]
            self.right_x_3, self.right_y_3 = self.rightEye[3]

            self.left_x_0, self.left_y_0 = self.leftEye[0]
            self.left_x_3, self.left_y_3 = self.leftEye[3]

            # def  x and y eye center
            self.right_x = abs(self.right_x_0 - self.right_x_3) / 2
            self.right_y = abs(self.right_y_0 - self.right_y_3) / 2

            self.left_x = (self.left_x_3 - self.left_x_0) / 2
            self.left_y = (self.left_y_3 - self.left_y_0) / 2

            # fix center eyes right and left
            self.center_right_x = self.right_x_0 + self.right_x
            self.center_right_y = self.right_y_0 + self.right_y

            self.center_left_x = self.left_x_0 + self.right_x
            self.center_left_y = self.left_y_0 + self.right_y

            self.point_center_x = (self.center_right_x + self.center_left_x) / 2
            self.point_center_y = (self.center_right_y + self.center_left_y) / 2

            return {
                    "center_right_x": self.center_right_x,
                    "center_right_y": self.center_right_y,
                    "center_left_x": self.center_left_x,
                    "center_left_y": self.center_left_y,
                    "point_center_x": self.point_center_x,
                    "point_center_y": self.point_center_y,
                    "rightEye": self.rightEye,
                    "leftEye": self.leftEye}

if __name__ == '__main__':

    extand_eyes_class = Extand_eyes()

    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        image = extand_eyes_class.extend(gray)
        # image_2 = extand_eyes_class.extend_none(image)
        # print(image_2)

        if image == None:
            pass
        else:
            point_center_x = int(image["point_center_x"])
            point_center_y = int(image["point_center_y"])
            cv2.circle(frame, (point_center_x , point_center_y), 2, (0, 255, 0), -1)

        cv2.waitKey(1)
        if cv2.getWindowProperty('frame', 1) == -1:
            break
    cap.release()
    cv2.destroyAllWindows()
