import cv2
import mediapipe as mp
import pyautogui
import time

cap = cv2.VideoCapture(0)
mp_hand = mp.solutions.hands.Hands(model_complexity=0, min_detection_confidence=0.8,
    min_tracking_confidence=0.8)
mp_drawing = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False
not_click = True
not_hold = False
help_constant = 0.015

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    frame.flags.writeable = False
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_hand.process(frame)

    frame_height, frame_width, _ = frame.shape
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        palm_x_abs = int(hand.landmark[9].x*frame_width)
        palm_y_abs = int(hand.landmark[9].y*frame_height)
        x = (screen_width / (0.6 * frame_width) * palm_x_abs) - screen_width*0.2
        y = (screen_height / (0.6 * frame_height) * palm_y_abs) - screen_height*0.3
        pyautogui.moveTo(x,y, duration=0.1)

        thumb_y= hand.landmark[4].y
        index_y = hand.landmark[8].y + help_constant
        middle_y = hand.landmark[12].y + help_constant

        if index_y >= thumb_y:
            if not_click:
                print('click')
                pyautogui.click()
                not_click = False
            if (middle_y >= thumb_y): #hold
                if not_hold:
                    pyautogui.mouseDown()
                    not_hold = False
        elif middle_y >= thumb_y:
            if not_click:
                pyautogui.click(button='right')
                not_click = False
        else:
            if not not_hold:
                pyautogui.mouseUp()
                not_hold = True
            not_click = True

        # Draw the hand annotations on the image.
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
                frame,
                hand)

    cv2.imshow('Virtual Mouse', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()