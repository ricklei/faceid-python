import cv2
from managers import CaptureManager, WindowManager, PeopleManager
from recognizer import Recognizer

class FaceID(object):

    def __init__(self):
        self._windowManager = WindowManager('FaceID', self.onKeypress)
        self._captureManager = CaptureManager(cv2.VideoCapture(0), self._windowManager, True)

    def run(self): # run the application
        self._windowManager.createWindow()

    def onKeypress(self, keycode):
        # handle a keypress
        if keycode == 27: # escape
            self._windowManager.destroyWindow()

if __name__ == "__main__":
    FaceID().run()