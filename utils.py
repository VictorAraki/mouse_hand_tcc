import cv2
import mediapipe as mp
import pyautogui

# Configurações gerais
MIN_DETECTION_CONFIDENCE = 0.8
MIN_TRACKING_CONFIDENCE = 0.8

def initialize():
    """Inicializa a câmera e o MediaPipe."""
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise Exception("Não foi possível acessar a câmera.")
        
        # Inicializando o detector de mãos do MediaPipe
        mp_hand = mp.solutions.hands.Hands(
            model_complexity=0,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        )
        mp_drawing = mp.solutions.drawing_utils
        
        # Obtendo as dimensões da tela
        screen_width, screen_height = pyautogui.size()
        
        pyautogui.FAILSAFE = False
        
        return cap, mp_hand, mp_drawing, screen_width, screen_height
    except Exception as e:
        print(f"Erro na inicialização: {e}")
        return None
