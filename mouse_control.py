import cv2
import os
import pyautogui
import math

from utils import initialize


class MouseControl():
    def __init__(self) -> None:
        self.pointer = int(os.getenv('MousePointerPoint'))
        self.sensibility_x = float(os.getenv('MouseSensibility_X'))
        self.sensibility_y = float(os.getenv('MouseSensibility_Y'))
        self.screen_offset_height = float(os.getenv('ScreenOffSet_width'))
        self.screen_offset_width = float(os.getenv('ScreenOffSet_height'))
        
        self.reference = int(os.getenv('MouseReference'))
        self.click_ref = int(os.getenv('MouseClickRef'))
        self.dist_click = int(os.getenv('DistanciaClick'))

        self.is_hold = False

    def move_mouse(self, screen_width, screen_height, frame_width, frame_height, hand):
        """
        Move mouse pointer
        """
        # Get pointer coord
        x_pointer = int(hand.landmark[self.pointer].x * frame_width)
        y_pointer = int(hand.landmark[self.pointer].y * frame_height)

        # Calculate how to move mouse
        scale_x = screen_width / frame_width
        scale_y = screen_height / frame_height
        off_set_x = screen_width * self.screen_offset_width
        off_set_y = screen_height * self.screen_offset_height
        x = x_pointer * scale_x * self.sensibility_x - off_set_x
        y = y_pointer * scale_y * self.sensibility_y - off_set_y

        pyautogui.moveTo(x, y, duration=0.1, tween=pyautogui.easeInOutQuad)

    def _distancia_entre_pontos(self, x_ref, y_ref, x_ref_click, y_ref_click):
        # Calculando a distância euclidiana entre os dois pontos
        distancia = math.sqrt((x_ref_click - x_ref)**2 + (y_ref_click - y_ref)**2)
        return distancia

    def click_mouse(self, frame_width, frame_height, hand):
        x_ref = int(hand.landmark[self.reference].x * frame_width)
        y_ref = int(hand.landmark[self.reference].y * frame_height)

        x_ref_click = int(hand.landmark[self.click_ref].x * frame_width)
        y_ref_click = int(hand.landmark[self.click_ref].y * frame_height)

        dist = self._distancia_entre_pontos(x_ref, y_ref, x_ref_click, y_ref_click)

        if dist < self.dist_click:
            if not self.is_hold:
                pyautogui.mouseDown()
                self.is_hold = True
        elif self.is_hold:
            pyautogui.mouseUp()
            self.is_hold = False


    def process_hand(self, results, frame_width, frame_height, screen_width, screen_height):
        """Processa a mão detectada e realiza as ações de controle do mouse."""
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
        
            self.move_mouse(screen_width, screen_height, frame_width, frame_height, hand)
            self.click_mouse(frame_width, frame_height, hand)

def start_mouse_control(mouse_on_func):
    """Inicia o controle do mouse."""
    cap, mp_hand, mp_drawing, screen_width, screen_height = initialize()
    mouse_control = MouseControl()
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
            mouse_control.process_hand(results, frame_width, frame_height, screen_width, screen_height)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.imshow('Virtual Mouse', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()