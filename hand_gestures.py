import mediapipe as mp
import cv2
import numpy as np
import os
import uuid
import pyautogui as pg
cam=cv2.VideoCapture(0)
mp_hands=mp.solutions.hands
screen_w,screen_h=pg.size()
with mp_hands.Hands(min_detection_confidence=0.8,min_tracking_confidence=0.8) as hands:
    while cam.isOpened():
        ret,frame=cam.read()
        frame=cv2.flip(frame,1)
        if cv2.waitKey(10)&0xFF==ord('q'):
            break
        #bgr to rgb
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable=False
        #detection
        results=hands.process(rgb_frame)
        rgb_frame.flags.writeable=True
        rgb_frame=cv2.cvtColor(rgb_frame,cv2.COLOR_RGB2BGR)
        landmark_points=results.multi_hand_landmarks
        frame_h,frame_w,_=frame.shape
        if landmark_points:
            landmarks=landmark_points[0].landmark
            for id,landmark in enumerate(landmarks[0:20]):
                x=int(landmark.x*frame_w)
                y=int(landmark.y*frame_h)
                cv2.circle(frame,(x,y),3,(0,255,0))
                if id==1:
                    screen_x=screen_w/frame_w*x
                    screen_y=screen_h/frame_h*y
                    pg.moveTo(screen_x,screen_y)
            click=[landmarks[8],landmarks[5]]
            if (click[1].y-click[0].y)<0.1:
                pg.click()
                pg.sleep(1)

        cv2.imshow('Hand controlled mouse',frame)


cam.release()
cv2.destroyAllWindows()

