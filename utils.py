import cv2
import numpy as np
import scipy.interpolate

def isGray(image):
    return image.ndim < 3

def sizeDividedBy(image, divisor):
    h, w = image.shape[:2]
    return ((int)(w/divisor), (int)(h/divisor))