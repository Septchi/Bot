import numpy as np
import cv2
from cv2 import cuda
import pyautogui
from time import time
import win32gui
from ImageProcessing import ImageProcessing

window = "SuperNova - https://chat.kongregate.com/gamez/0024/9627/live/game.swf?kongregate_game_version=1564415602"
hwnd = win32gui.FindWindow(None, window)
imgProc = ImageProcessing(hwnd)


def draw_circle(event, x, y, flags, param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        #cv2.circle(img, (x, y), 100, (255, 0, 0), -1)
        mouseX, mouseY = x, y
        #print(mouseX, mouseY)

def test(hay):
    needle = cv2.imread("apple.jpeg", 0)
    #hay = cv2.imread("screen.jpeg", cv2.IMREAD_UNCHANGED)
    result = cv2.matchTemplate(hay, needle, cv2.TM_CCOEFF_NORMED)

    needleW = needle.shape[1]
    needleH = needle.shape[0]

    threshold = 0.52


    locations = np.where(result>=threshold)
    locations = list(zip(*locations[::-1]))
    #print("location: ", locations)
    min, max, minPos, maxPos = cv2.minMaxLoc(result)

    res = min
    resPos = minPos

    #print("best location: %s" % str(maxPos))
    #print(max)

    rects = []

    if locations:
        #print("match found")
        for l in locations:
            rect = [int(l[0]), int(l[1]), needleW, needleH]
            rects.append(rect)
        #print(rects)
        rects, weights = cv2.groupRectangles(rects, groupThreshold=1, eps=0.5)
        #print(rects)
        if len(rects):
            #print("rects found")
            for (x, y, w, h) in rects:
                topLeft = (x, y)
                botRight = (x + w, y + h)
                cv2.rectangle(hay, topLeft, botRight, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_4)
    return hay
    #cv2.imwrite("result.jpeg", hay)

def main():
    #print("started")

    global img

    timeStart = time()
    frames=0
    while True:
        if(time()-timeStart<1):
            frames+=1
        else:
            timeStart=time()
            print("frames: ", frames)
            frames=0


        img = test(cv2.cvtColor(imgProc.screenshot(),cv2.COLOR_RGB2GRAY))
        cv2.imshow("Test", img)

        if(cv2.waitKey(1) & 0xFF) == ord('s'):
            cv2.imwrite("screen.jpeg", img)
            #print("saved")
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break

# Start of the main program here
if __name__ == "__main__":
    #test()
    main()
