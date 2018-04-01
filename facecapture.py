import cv2
import numpy as np
from managers import CaptureManager, WindowManager
import argparse
import os
from detector import Face, FaceDetector
from logger import logger
import utils
import time


class FaceCapture(object):

    def __init__(self, name):

        self._configs = utils.loadConfigFile('facecapture.cf')

        self._name = name

        self._camera = cv2.VideoCapture(int(self._configs['capture.camera']))
        self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, int(self._configs['capture.width']))
        self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, int(self._configs['capture.height']))

        self._windowManager = WindowManager('Face Capture for {0}'.format(self._name), self.onKeypress)
        self._captureManager = CaptureManager(self._camera, self._windowManager, True)
        self._faceDetector = FaceDetector()

        self._filePath = '{0}\\{1}'.format(self._configs['dataset.dir'], self._name)

        os.makedirs(self._filePath, exist_ok = True)

    def run(self):

        self._windowManager.createWindow()

        idx = 1

        while self._windowManager.isWindowCreated:

            self._captureManager.enterFrame()
            frame = self._captureManager.frame

            self._faceDetector.update(frame)
            faces = self._faceDetector.faces

            if len(faces) == 1:
                x, y, h, w = faces[0].faceRect
                face_image = frame[y:y+h, x:x+w]
                face_image = cv2.cvtColor(face_image, cv2.COLOR_RGB2GRAY)

                cv2.imshow('face', face_image)
                cv2.imwrite('{0}\\{1}-{2}.jpg'.format(self._filePath, self._name, idx), face_image)
                idx += 1

                time.sleep(0.1)

            self._captureManager.exitFrame()

            self._windowManager.processEvents()

    def onKeypress(self, keycode):

        if keycode == 27: # escape

            self._windowManager.destroyWindow()
            self._camera.release()

        elif keycode == ord('r'): # record

            if self._isRecording:
                self._isRecording = False
            else:
                self._isRecording = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('Name', help='Whose face will be recorded?')
    args = parser.parse_args()

    FaceCapture(args.Name).run()


