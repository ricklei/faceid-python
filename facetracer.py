import cv2
import numpy as np
import os
import utils
from managers import WindowManager, CaptureManager
from facecapture import FaceDetector
import time


class FaceTracer(object):

    def __init__(self):
        self._configs = utils.loadConfigFile('facecapture.cf')
        self._users = utils.loadConfigFile('names.cf')

        self._camera = cv2.VideoCapture(int(self._configs['capture.camera']))
        self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, int(self._configs['capture.width']))
        self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, int(self._configs['capture.height']))

        self._windowManager = WindowManager('Face Tracing', self.onKeypress)
        self._captureManager = CaptureManager(self._camera, self._windowManager)
        self._faceDetector = FaceDetector()

        self._recognizer = cv2.face.LBPHFaceRecognizer_create()
        self._recognizer.read('trainingData.yml')

    def onKeypress(self, keycode):
        if keycode == 27: # escape

            self._windowManager.destroyWindow()
            self._camera.release()

    def run(self):
        trainData = 'trainingData.yml'

        self._windowManager.createWindow()

        while self._windowManager.isWindowCreated:

            self._captureManager.enterFrame()
            frame = self._captureManager.frame

            self._faceDetector.update(frame)
            faces = self._faceDetector.faces

            for face in faces:
                x, y, h, w = face.faceRect
                face_image = frame[y:y+h, x:x+w]
                face_image = cv2.cvtColor(face_image, cv2.COLOR_RGB2GRAY)
                ids, conf = self._recognizer.predict(face_image)
                if conf < 50:
                    for name, id in self._users.items():
                        if int(id) == ids:
                            self._captureManager.addRect(face.faceRect, '{0}({1:.0f})'.format(name, conf))
                else:
                    self._captureManager.addRect(face.faceRect, 'Unknown')

            self._captureManager.exitFrame()

            self._windowManager.processEvents()

            time.sleep(0.1)

if __name__ == '__main__':
    FaceTracer().run()
