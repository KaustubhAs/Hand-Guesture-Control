import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
import pyautogui
import time
import os


cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volMin, volMax = volume.GetVolumeRange()[:2]
x = 0 
while True:

    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []
    if results.multi_hand_landmarks: 
        for handlandmark in results.multi_hand_landmarks:
            for id, lm in enumerate(handlandmark.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy]) 
                mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)

    if lmList != []:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2] 
        x3, y3 = lmList[12][1], lmList[12][2]
        x4, y4 = lmList[16][1], lmList[16][2]
        x5, y5 = lmList[20][1], lmList[20][2]



        cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)  
        cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED) 
        cv2.circle(img, (x3, y3), 15, (255, 0, 0), cv2.FILLED) 
        cv2.circle(img, (x4, y4), 15, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x5, y5), 15, (255, 0, 0), cv2.FILLED) 


        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
        cv2.line(img, (x2, y2), (x3, y3), (255, 0, 0), 3)
        cv2.line(img, (x3, y3), (x4, y4), (255, 0, 0), 3)
        cv2.line(img, (x4, y4), (x5, y5), (255, 0, 0), 3)

        #cv2.line(img, (x3, y3), (x1, y1), (255, 0, 0), 3)
        



        length1 = hypot(x2 - x1, y2 - y1)
        length2 = hypot(x2 - x3, y2 - y3)
        length3 = hypot(x3-x1,y3-y1)
        length4 = hypot(x4-x1,y4-y1)
        length5 = hypot(x5-x1,y5-y1)

        
        #print(length5)
        

        if((10<length3<30)and(100<length5<220)):
                if(x<=10): 
                    x = x + 1   
                    myScreenshot = pyautogui.screenshot()
                    myScreenshot.save(r'Path_of_the_folder_to_store_ss\file name{}.png'.format(x))
                    time.sleep(1)
       


        output = os.popen('wmic process get description').read()
        if (('WINWORD.EXE' in output)):

            pyautogui.FAILSAFE = False

            if((5<length1<30)and(5<length3<30)):
                pyautogui.hotkey('alt','f4')
                time.sleep(2)

            if((0<length4<30)and(0<length5<30)):
                pyautogui.hotkey('ctrl','s')

            if ((0<length2<20)and(130<length4<180)):
                pyautogui.hotkey('ctrl', 'p')



        else:
            pyautogui.FAILSAFE = True

            vol = np.interp(length1, [15, 220], [volMin, volMax])
            #print(vol, length1)
            volume.SetMasterVolumeLevel(vol, None)
            cv2.imshow('Image', img)

            if((10<length1<20)and(10<length3<20)):
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                break

            #if((10<length1<20)and(10<length3<20)):
                #os.system("shutdown /s /t 1")
                #break          
            

        pyautogui.FAILSAFE = True


    if cv2.waitKey(1) & 0xff == ord('q'): 
        break