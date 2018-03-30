import cv2
import numpy as np
import utils


class Face(object):

    def __init__(self):
        self.faceRect = None
        self.leftEyeRect = None
        self.rightEyeRect = None
        self.noseRect = None
        self.mouthRect = None


class FaceDetector(object):

    def __init__(self, scaleFactor = 1.2, minNeighbors = 2, flags = cv2.CASCADE_SCALE_IMAGE):

        self.scaleFactor = scaleFactor
        self.minNeighbors = minNeighbors
        self.flags = flags

        self._faces = []

        self._faceClassifier = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt.xml')
        self._eyeClassifier = cv2.CascadeClassifier('cascades/haarcascade_eye.xml')
        self._noseClassifier = cv2.CascadeClassifier('cascades/haarcascade_mcs_nose.xml')
        self._mouthClassifier = cv2.CascadeClassifier('cascades/haarcascade_mcs_mounth.xml')

    @property
    def faces(self):
        return self._faces

    def update(self, image):

        self._faces = []

        if not utils.isGray(image):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.equalizeHist(image)

        minFaceSize = utils.sizeDividedBy(image, 8)

        faceRects = self._faceClassifier.detectMultiScale(
            image, self.scaleFactor, self.minNeighbors, self.flags,
            minFaceSize)

        if faceRects is not None:
            for faceRect in faceRects:

                face = Face()
                face.faceRect = faceRect

                self._faces.append(face)
