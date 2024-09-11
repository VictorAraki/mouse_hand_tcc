import cv2
import mediapipe as mp
import pyautogui

# Definindo constantes para ajustar os parâmetros de detecção
MIN_DETECTION_CONFIDENCE = 0.8
MIN_TRACKING_CONFIDENCE = 0.8
HELP_CONSTANT = 0.015

def initialize():
    """
    Inicializa os componentes principais: câmera, MediaPipe e captura de tela.
    """
    try:
        # Inicializando captura de vídeo
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
        
        # Obtendo dimensões da tela
        screen_width, screen_height = pyautogui.size()
        
        pyautogui.FAILSAFE = False  # Desabilita o recurso de segurança do PyAutoGUI
        
        return cap, mp_hand, mp_drawing, screen_width, screen_height
    
    except Exception as e:
        print(f"Erro na inicialização: {e}")
        return None

def process_hand(results, frame_width, frame_height, screen_width, screen_height):
    """
    Processa a mão detectada e realiza as ações de controle do mouse.
    """
    not_click = True
    not_hold = False
    
    if results.multi_hand_landmarks:
        # Obtendo a primeira mão detectada
        hand = results.multi_hand_landmarks[0]
        
        # Calculando a posição da palma da mão
        palm_x_abs = int(hand.landmark[9].x * frame_width)
        palm_y_abs = int(hand.landmark[9].y * frame_height)
        
        # Ajustando as coordenadas do mouse de acordo com a tela
        x = (screen_width / (0.6 * frame_width) * palm_x_abs) - screen_width * 0.2
        y = (screen_height / (0.6 * frame_height) * palm_y_abs) - screen_height * 0.3
        pyautogui.moveTo(x, y, duration=0.1)

        # Obtendo a posição do polegar e dos dedos
        thumb_y = hand.landmark[4].y
        index_y = hand.landmark[8].y + HELP_CONSTANT
        middle_y = hand.landmark[12].y + HELP_CONSTANT
        
        # Verificando gestos para clique esquerdo e direito
        if index_y >= thumb_y:
            if not_click:
                pyautogui.click()
                not_click = False
            if middle_y >= thumb_y:  # Hold (manter pressionado)
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

def draw_landmarks(frame, hand, mp_drawing):
    """
    Desenha as landmarks da mão detectada no frame.
    """
    mp_drawing.draw_landmarks(frame, hand)

def main():
    """
    Função principal que executa o loop de detecção de mãos e controle do mouse.
    """
    # Inicializa os componentes principais
    cap, mp_hand, mp_drawing, screen_width, screen_height = initialize()
    
    if cap is None:
        print("Falha na inicialização. Saindo...")
        return
    
    try:
        while True:
            # Captura um frame da câmera
            ret, frame = cap.read()
            if not ret:
                print("Erro ao capturar frame da câmera.")
                break
            
            frame = cv2.flip(frame, 1)
            frame.flags.writeable = False
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Processa o frame usando MediaPipe
            results = mp_hand.process(frame)
            frame_height, frame_width, _ = frame.shape
            
            # Processa a mão e executa ações
            not_click, not_hold = process_hand(results, frame_width, frame_height, screen_width, screen_height)
            
            # Desenha landmarks se a mão for detectada
            if results.multi_hand_landmarks:
                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                draw_landmarks(frame, results.multi_hand_landmarks[0], mp_drawing)
            
            # Exibe o frame
            cv2.imshow('Virtual Mouse', frame)
            
            # Verifica se a tecla ESC foi pressionada para sair
            if cv2.waitKey(1) & 0xFF == 27:
                break
    except Exception as e:
        print(f"Ocorreu um erro durante a execução: {e}")
    finally:
        # Libera a câmera e fecha as janelas
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()