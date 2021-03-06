import cv2
import numpy as np
import time

class CaptureManager(object):

    def __init__(self, capture, previewWindowManager = None, shouldMirrorPreview = False):

        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview = shouldMirrorPreview

        self._capture = capture
        self._channel = 0
        self._enteredFrame = False
        self._frame = None

        self._startTime= None
        self._framesElapsed = int(0)
        self._fpsEstimate = None

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = value
            self._frame = None

    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve()
        return self._frame

    def enterFrame(self):
        # begin to capture a frame
        assert not self._enteredFrame, 'previous enterFrame() had no matching extiFrame()'

        if self._capture is not None:
            self._enteredFrame = self._capture.grab()

    def exitFrame(self):
        # all operations for the last frame are done. release the frame
        if self.frame is None:
            self._enteredFrame = False
            return

        # udpate the FPS estimatioin
        if self._framesElapsed == 0:
            self._startTime = time.time()
        else:
            timeElapsed = time.time() - self._startTime
            self._fpsEstimate = self._framesElapsed / timeElapsed
        self._framesElapsed += 1

        # draw the frame to window
        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                mirroredFrame = np.fliplr(self._frame).copy()
                self.previewWindowManager.show(mirroredFrame)
            else:
                self.previewWindowManager.show(self._frame)

        # release the frame
        self._frame = None
        self._enteredFrame = False

    def addRect(self, rect, caption):
        if self._frame is not None:
            x, y, w, h = rect
            cv2.rectangle(self._frame, (x, y), (x+w, y+h), (0,255,0), 3)
            cv2.putText(self._frame, caption, (x+2, y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (150, 255, 0), 2)


class WindowManager(object):

    def __init__(self, windowName, keypressCallback = None):
        self.keypressCallback = keypressCallback

        self._windowName = windowName
        self._isWindowCreated = False

        self._textBuffer = []

    @property
    def isWindowCreated(self):
        return self._isWindowCreated

    def createWindow(self):
        cv2.namedWindow(self._windowName)
        self._isWindowCreated = True

    def destroyWindow(self):
        cv2.destroyAllWindows()
        self._isWindowCreated = False

    def show(self, frame):
        y = 30
        for s in self._textBuffer:
            cv2.putText(frame, s, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2)
            y += 30
        cv2.imshow(self._windowName, frame)

    def appendText(self, text):
        self._textBuffer.append(text)

    def appendChar(self, ch):
        if self._textBuffer.__len__() > 0:
            self._textBuffer[-1] = self._textBuffer[-1] + ch
        else:
            self._textBuffer.append(ch)

    def processEvents(self):
        keycode = cv2.waitKey(1)
        if self.keypressCallback is not None and keycode != -1:
            keycode &= 0xFF
            self.keypressCallback(keycode)
