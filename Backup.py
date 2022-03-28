import imutils   # sudo pip3 install imutils
from imutils.video import VideoStream
import cv2

try:
    _height = 368
    _width = 400
    _resolution = (_height,_width)
    cf = VideoStream( usePiCamera=True , resolution=_resolution , framerate=30 )
    cf.start()

    while True:
        frame = cf.read()
        cv2.imshow("Output", frame)
except Exception as e:
    print(e)