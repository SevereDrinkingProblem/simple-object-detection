import cv2 as cv
import numpy as np
import os
from time import time
import torch
from windowCapture import WindowCapture



model = torch.hub.load('ultralytics/yolov5', 'custom', path='./fish.pt', force_reload=True);

def main():
    winCap = WindowCapture('fish.mp4 - VLC media player');
    loopTime = time();

    while(True):
        screenshot = winCap.getScreenshot();

        results = model(screenshot);
        cv.putText(screenshot, 'FPS {}'.format(1 / (time() - loopTime)), (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv.LINE_AA);
        cv.imshow('Feed', np.squeeze(results.render()));

        print('FPS {}'.format(1 / (time() - loopTime)));
    
        loopTime = time();

        if cv.waitKey(1) == ord('q'):
            break;

    cv.destroyAllWindows();


if __name__ == "__main__": 
    main()