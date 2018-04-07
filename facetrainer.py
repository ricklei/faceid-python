import cv2
import numpy as np
import logger
import utils
from PIL import Image
import os

class FaceTrainer(object):

    def __init__(self):
        self._configs = utils.loadConfigFile('facecapture.cf')
        self._users = utils.loadConfigFile('names.cf')
        self._path = self._configs['dataset.dir']

    def run(self):
        ids, faces = self.getImagesWithId()
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(faces, ids)
        recognizer.save('trainingData.yml')

    def getImagesWithId(self):
        faces = []
        ids = []

        for image in os.listdir(self._path):
            faceImg = Image.open('{0}\\{1}'.format(self._path, image))
            faceNp = np.array(faceImg, 'uint8')
            id = int(image.split('-')[0])
            faces.append(faceNp)
            ids.append(id)
            cv2.imshow('training', faceNp)

        return np.array(ids), faces

if __name__ == '__main__':
    FaceTrainer().run()
