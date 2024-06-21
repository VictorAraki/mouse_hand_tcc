import cv2
import mediapipe as mp
import pyautogui
import time
from google.protobuf.json_format import MessageToDict

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    if output.multi_handedness:
        hands_landmarks = output.multi_hand_landmarks
        for idx, hand_handedness in enumerate(output.multi_handedness[:2]):
            handedness_dict = MessageToDict(hand_handedness)
            handedness = handedness_dict['classification'][0]['label']
            if handedness == 'Right':
                index_x = int(hands_landmarks[idx].landmark[8].x*frame_width)
                index_y = int(hands_landmarks[idx].landmark[8].y*frame_height)
                x = (screen_width / (0.9 * frame_width)) * index_x
                y = (screen_height / (0.9 * frame_height)) * index_y
                pyautogui.moveTo(x,y)
            if handedness == 'Left':
                index_y_1 = hands_landmarks[idx].landmark[8].y
                index_y_2 = hands_landmarks[idx].landmark[6].y
                if index_y_1 > index_y_2:
                    pyautogui.click()
                    print("click")
                    time.sleep(0.5)

    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)