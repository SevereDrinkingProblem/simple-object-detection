import numpy as np
import win32gui
import win32ui
import win32con



class WindowCapture:
    width = 0;
    height = 0;
    hwnd = None;
    croppedX = 0;
    croppedy = 0;
    
    def __init__(self, windowName):
        self.hwnd = win32gui.FindWindow(None, windowName); 
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(windowName));
        windowRect = win32gui.GetWindowRect(self.hwnd);
        self.width = windowRect[2] - windowRect[0];
        self.height = windowRect[3] - windowRect[1];
    
        borderPixels = 10;
        titlebarPixels = 10;
        self.width = self.width - (borderPixels * 2);
        self.height = self.height - titlebarPixels - borderPixels;
        self.croppedX = borderPixels;
        self.croppedY = titlebarPixels;

    def getScreenshot(self):
        wDC = win32gui.GetWindowDC(self.hwnd);
        dcObj=win32ui.CreateDCFromHandle(wDC);
        cDC=dcObj.CreateCompatibleDC();
        dataBitMap = win32ui.CreateBitmap();
        dataBitMap.CreateCompatibleBitmap(dcObj, self.width, self.height);
        cDC.SelectObject(dataBitMap);
        cDC.BitBlt((0,0),(self.width, self.height) , dcObj, (self.croppedX,self.croppedY), win32con.SRCCOPY);
        signedIntsArray = dataBitMap.GetBitmapBits(True);
        img = np.fromstring(signedIntsArray, dtype='uint8');
        img.shape = (self.height, self.width, 4);

        dcObj.DeleteDC();
        cDC.DeleteDC();
        win32gui.ReleaseDC(self.hwnd, wDC);
        win32gui.DeleteObject(dataBitMap.GetHandle());

        img = img[...,:3];
        img = np.ascontiguousarray(img);

        return img;