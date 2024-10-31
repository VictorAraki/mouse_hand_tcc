import cv2
import mediapipe as mpipe

class MediaPipeHelper():

    def __init__(self, setup):
        self.frame_width = setup["frame_width"]
        self.frame_height = setup["frame_height"]
        self.cap = self.start_capture()

        # Inicializando o detector de mãos do MediaPipe
        MIN_DETECTION_CONFIDENCE = 0.8
        MIN_TRACKING_CONFIDENCE = 0.8
        self.mp_hand = mpipe.solutions.hands.Hands(
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        )
        
        self.mp_drawing = mpipe.solutions.drawing_utils


    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            raise Exception("Não foi possível capturar o frame.")
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def get_coord(self, hand, point_number):
        x = int(hand.landmark[point_number].x * self.frame_width)
        y = int(hand.landmark[point_number].y * self.frame_height)
        return x,y

    def start_capture(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise Exception("Não foi possível acessar a câmera.")
        return cap

    def stop_capture(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

    def show_camera(self, frame):
        cv2.imshow('Virtual Mouse', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            raise Exception("Desligando a came")

    def draw_hand(self, hand, frame, ref, ref_click):
        """Desenha as marcas na mao"""
        self.mp_drawing.draw_landmarks(frame, hand)
        cv2.circle(img=frame, center=(ref[0],ref[1]), radius=20, color=(0, 255, 255))
        cv2.circle(img=frame, center=(ref_click[0],ref_click[1]), radius=20, color=(0, 255, 255))
    
    def main_mediapipe(self, points):
        frame = self.get_frame()
        results = self.mp_hand.process(frame)
        coords = {}
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            for point_name,point_number in points.items():
                coords[point_name] = self.get_coord(hand, point_number)
            self.draw_hand(hand, frame, ref=coords["MouseReference"], ref_click=coords["MouseClickRef"])
        self.show_camera(frame)
        return coords

if __name__ == "__main__":
    print("start")
    from utils import setup
    setup = setup()
    print("apos setup")
    config = {
            "MousePointerPoint": 8,
            "MouseReference": 4,
            "MouseClickRef": 12,
            "MouseSensibility_X": 1.4,
            "MouseSensibility_Y": 1.2,
            "ScreenOffSet_width": 0.2,
            "ScreenOffSet_height": 0.3,
            "DistanciaClick": 50,
            "DurationMove": 0.01
    }
    points = {key: config[key] for key in ['MousePointerPoint', 'MouseReference', 'MouseClickRef']}
    mph = MediaPipeHelper(setup)
    print("antes do true")
    while True:
        mph.main_mediapipe(points)