import cv2
import pyautogui
from utils import initialize

def process_hand(results, frame_width, frame_height, screen_width, screen_height):
    """Processa a mão detectada e realiza as ações de controle do mouse."""
    not_click = True
    not_hold = False
    
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        
        # Coordenadas da palma
        palm_x_abs = int(hand.landmark[9].x * frame_width)
        palm_y_abs = int(hand.landmark[9].y * frame_height)
        
        # Coordenadas ajustadas para o movimento do mouse
        x = (screen_width / (0.6 * frame_width) * palm_x_abs) - screen_width * 0.2
        y = (screen_height / (0.6 * frame_height) * palm_y_abs) - screen_height * 0.3
        pyautogui.moveTo(x, y, duration=0.1)

        # Detectar gestos e cliques
        thumb_y = hand.landmark[4].y
        index_y = hand.landmark[8].y
        middle_y = hand.landmark[12].y
        
        if index_y >= thumb_y:
            if not_click:
                pyautogui.click()
                not_click = False
            if middle_y >= thumb_y:
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
    
    return not_click, not_hold

def start_mouse_control(mouse_on_func):
    """Inicia o controle do mouse."""
    cap, mp_hand, mp_drawing, screen_width, screen_height = initialize()
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
            process_hand(results, frame_width, frame_height, screen_width, screen_height)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.imshow('Virtual Mouse', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()