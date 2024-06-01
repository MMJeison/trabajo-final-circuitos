import cv2
from threading import Thread

class VideoStreamN:
    def __init__(self, src=0):
        self.src = src
        self.cap = None
        self.grabbed = False
        self.frame = None
        self.stopped = True

    def start(self):
        if self.stopped:
            self.cap = cv2.VideoCapture(self.src)
            self.grabbed, self.frame = self.cap.read()
            self.stopped = False
            Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            self.grabbed, self.frame = self.cap.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        if self.cap:
            self.cap.release()
