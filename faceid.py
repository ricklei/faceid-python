import cv2
from managers import CaptureManager, WindowManager, PeopleManager
from detector import FaceDetector

class FaceID(object):

    def __init__(self):

        self._camera = cv2.VideoCapture(0)
        self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
        self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
        self._windowManager = WindowManager('Face ID', self.onKeypress)
        self._captureManager = CaptureManager(self._camera, self._windowManager, True)
        self._faceDetector = FaceDetector()

    def run(self): # run the application
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame

            self._faceDetector.update(frame)
            faces = self._faceDetector.faces

            for face in faces:
                x, y, h, w = face.faceRect
                face_image = frame[y:y+h,x:x+w]
                cv2.imshow('face', face_image)
                break

            self._captureManager.exitFrame()
            self._windowManager.processEvents()

    def onKeypress(self, keycode):
        # handle a keypress
        if keycode == 27: # escape
            self._windowManager.destroyWindow()
            self._camera.release()


if __name__ == "__main__":
    FaceID().run()