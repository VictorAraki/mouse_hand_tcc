import cv2
import os
import pyautogui
import math

from utils import initialize


class MouseControl():
    def __init__(self, mp_drawing, screen_width, screen_height) -> None:
        self.mp_drawing = mp_drawing
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.pointer = int(os.getenv('MousePointerPoint'))
        self.sensibility_x = float(os.getenv('MouseSensibility_X'))
        self.sensibility_y = float(os.getenv('MouseSensibility_Y'))
        self.screen_offset_height = float(os.getenv('ScreenOffSet_width'))
        self.screen_offset_width = float(os.getenv('ScreenOffSet_height'))
        
        self.reference = int(os.getenv('MouseReference'))
        self.click_ref = int(os.getenv('MouseClickRef'))
        self.dist_click = int(os.getenv('DistanciaClick'))
        self.duration = float(os.getenv('DurationMove'))

        self.is_click = False

    def move_mouse(self, frame_width, frame_height, hand):
        """
        Move mouse pointer
        """
        # Get pointer coord
        x_pointer = int(hand.landmark[self.pointer].x * frame_width)
        y_pointer = int(hand.landmark[self.pointer].y * frame_height)

        # Calculate how to move mouse
        scale_x = self.screen_width / frame_width
        scale_y = self.screen_height / frame_height
        off_set_x = self.screen_width * self.screen_offset_width
        off_set_y = self.screen_height * self.screen_offset_height
        x = x_pointer * scale_x * self.sensibility_x - off_set_x
        y = y_pointer * scale_y * self.sensibility_y - off_set_y

        pyautogui.moveTo(x, y, duration=self.duration)

    def _distancia_entre_pontos(self, x_ref, y_ref, x_ref_click, y_ref_click):
        # Calculando a distância euclidiana entre os dois pontos
        distancia = math.sqrt((x_ref_click - x_ref)**2 + (y_ref_click - y_ref)**2)
        return distancia

    def click_mouse(self, frame_width, frame_height, hand):
        self.x_ref = int(hand.landmark[self.reference].x * frame_width)
        self.y_ref = int(hand.landmark[self.reference].y * frame_height)

        self.x_ref_click = int(hand.landmark[self.click_ref].x * frame_width)
        self.y_ref_click = int(hand.landmark[self.click_ref].y * frame_height)

        dist = self._distancia_entre_pontos(self.x_ref, self.y_ref, self.x_ref_click, self.y_ref_click)

        if dist < self.dist_click:
            if not self.is_click:
                pyautogui.click()
                self.is_click = True
        else:
            self.is_click = False

    def process_hand(self, hand, frame_width, frame_height):
        """Processa a mão detectada e realiza as ações de controle do mouse."""
        self.move_mouse(frame_width, frame_height, hand)
        self.click_mouse(frame_width, frame_height, hand)

    def draw_hand(self, hand, frame):
        """Desenha as marcas na mao"""
        self.mp_drawing.draw_landmarks(frame, hand)
        cv2.circle(img=frame, center=(self.x_ref,self.y_ref), radius=20, color=(0, 255, 255))
        cv2.circle(img=frame, center=(self.x_ref_click,self.y_ref_click), radius=20, color=(0, 255, 255))

def start_mouse_control(mouse_on_func):
    """Inicia o controle do mouse."""
    cap, mp_hand, mp_drawing, screen_width, screen_height = initialize()
    mouse_control = MouseControl(mp_drawing, screen_width, screen_height)
    if not cap:
        print("Falha na inicializacao da camera.")
        return

    try:
        while mouse_on_func():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frame.flags.writeable = False
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = mp_hand.process(frame)
            frame_height, frame_width, _ = frame.shape
            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                mouse_control.process_hand(hand, frame_width, frame_height)
                mouse_control.draw_hand(hand, frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.imshow('Virtual Mouse', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()