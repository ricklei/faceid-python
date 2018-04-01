import cv2
import numpy as np
import logger
import utils

class FaceTrainer(object):

    def __init__(self):
        self._configs = utils.loadConfigFile('facecapture.cf')
        self._path = self._configs['dataset.dir']

    def run(self):




if __name__ == '__main__':
    FaceTrainer().run()