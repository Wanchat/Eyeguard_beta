import wmi
import cv2
import numpy as np

class Brightness:
    def array_gray(self, image): # Avg black white
        self.avg_gray = np.average(image)
        self.avg_gray = round(self.avg_gray)
        return self.avg_gray

    def brightness(self, image_gray): # Bright screen vs light avg
        self.var_brightness = 100 # max light is 255
        if 200 > self.avg_gray >= 140:
            self.var_brightness = 90
        elif 140 > self.avg_gray >= 100:
            self.var_brightness = 80
        elif 100 > self.avg_gray >= 60:
            self.var_brightness = 70
        elif 60 > self.avg_gray >= 50:
            self.var_brightness = 60
        elif 50 > self.avg_gray >= 40:
            self.var_brightness = 50
        elif 40 > self.avg_gray >= 30:
            self.var_brightness = 40
        elif 30 > self.avg_gray >= 0:
            self.var_brightness = 30
        else:
            self.var_brightness = 100
        return self.var_brightness

    def change_screen(self,v_brightness): # Change screen display
        wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(v_brightness, 1)

if __name__ == '__main__':
    bright = Brightness()
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        array = bright.array_gray(gray) # Avg black white
        bright_if = bright.brightness(array) # Bright screen vs light avg
        bright.change_screen(bright_if) #Change screen display
        print("bright: {} screen: {}".format(bright_if, array))
        cv2.imshow("Frame", frame)
        cv2.waitKey(1)
        if cv2.getWindowProperty("Frame", 1) == -1:
            break
    cap.release()
    cv2.destroyAllWindows()