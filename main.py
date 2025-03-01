import cv2
from cvzone.HandTrackingModule import HandDetector
import math
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands = 2)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["Space", "Backspace"]]

finalText = ""
keyboard = Controller()


#def drawAll(img, buttonList):
   # for button in buttonList:
      #  x, y = button.pos
        #w, h = button.size
       # cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 234), cv2.FILLED)
        #cv2.putText(img, button.text, (x + 20, y + 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
    #return img

def drawAll(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1],button.size[0],button.size[1]),20,rt=0)

        cv2.rectangle(img, button.pos, (x + w, y + h), (169,170,168), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

    out = img.copy()
    alpha = 0.75
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    return out

def calculateDistance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

class Button:
    def __init__(self, pos, text, size=None):
        if size is None:
            size = [85,85]
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i, row in enumerate(keys):
    for j, key in enumerate(row):
        if key == "Space":
            buttonList.append(Button([j * 100 + 100, i * 100 + 50], key, size=[300, 85]))
        elif key == "Backspace":
            buttonList.append(Button([j * 100 + 500, i * 100 + 50], key, size=[350, 85]))
        else:
            buttonList.append(Button([j * 100 + 50, i * 100 + 50], key))

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    #hands = detector.findHands(img, draw = False)

    img = drawAll(img, buttonList)

    if hands:
        hand1 = hands[0]
        lmList = hand1['lmList']
        bbox1 = hand1['bbox']
        # centerPoint1= hand1['center']
        # handType1 = hand1['type']
        # print(len(lmList1),lmList1)
        # print(bbox1)
        # print(centerPoint1)
        # print(handType1)


        if lmList:
            for button in buttonList:
              x, y = button.pos
              w, h = button.size

              if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

                l = calculateDistance(lmList[8], lmList[12])

                if l < 35:
                    #keyboard.press(button.text)

                    if button.text == "Space":
                        finalText += " "
                    elif button.text == "Backspace":
                        finalText = finalText[:-1]
                    else:
                        finalText += button.text

                    cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 60), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

                    sleep(0.10)

        cv2.rectangle(img, (50, 550), (1230, 650), (175, 0, 175), cv2.FILLED)
        cv2.putText(img, finalText, (60, 630), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255),3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
