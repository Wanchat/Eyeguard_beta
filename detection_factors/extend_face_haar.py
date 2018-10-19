import cv2

class Extend_face_haar:
    def __init__(self):
        self.face_detect = cv2.CascadeClassifier(
            r"C:\Users\Wanch\Google Drive\Thesis"
            r"\code_eyeguard\Eyeguard\data"
            r"\haarcascade_frontalface_default.xml")

    def extend_face(self,image_gray):

        self.face = self.face_detect.detectMultiScale(image_gray, 1.3,5)
        for (self.x,self.y,self.w,self.h) in self.face:
            return self.x,self.y,self.w,self.h

    def window_face(self,extend_face, origin_image):

        self.face_window = origin_image[extend_face[1]:extend_face[1] + extend_face[3],
                           extend_face[0]:extend_face[0] + extend_face[2]]
        return self.face_window

if __name__ == '__main__':

    Extend_face_haar_class = Extend_face_haar()

    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        try:
            xywh = Extend_face_haar_class.extend_face(gray)
            face_window = Extend_face_haar_class.window_face(xywh, frame)
            cv2.rectangle(frame,(xywh[0],xywh[1]),(xywh[0]+xywh[2],xywh[1]+xywh[3]),(0,255,0),2)
        except:
            print("not face")
            pass

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()