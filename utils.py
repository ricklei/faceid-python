import cv2
import numpy as np
import scipy.interpolate
from logger import logger

def isGray(image):
    return image.ndim < 3

def sizeDividedBy(image, divisor):
    h, w = image.shape[:2]
    return ((int)(w/divisor), (int)(h/divisor))

def loadConfigFile(filePath):
    configs = {}
    logger().info('Loading config file: {0}'.format(filePath))

    cf = open(filePath, 'r')

    for line in cf:
        if len(line) <= 0 or line.startswith('#') or not '=' in line:
            continue
        words = line.split('=')
        configs[words[0].strip()] = words[1].strip()

    cf.close()

    return configs
