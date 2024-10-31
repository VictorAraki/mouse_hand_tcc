import cv2
import os
import multiprocessing as mprocessing
import pyautogui


def setup():
    """Inicializa a câmera e o MediaPipe."""
    try:
        #inicializando a camera para obter os frames
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise Exception("Não foi possível acessar a câmera.")
        ret, frame = cap.read()
        cap.release()
        frame_height, frame_width, _ = frame.shape
        if not ret:
            raise Exception("Leitura do Frame com problemas")
        
        # Obtendo as dimensões da tela
        screen_width, screen_height = pyautogui.size()
        
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0
        pyautogui.MINIMUM_DURATION = 0.001
        
        setup = {
            'screen_width': screen_width,
            'screen_height': screen_height,
            'frame_width': frame_width,
            'frame_height': frame_height
        }
        return setup
    except Exception as e:
        print(f"Erro na inicialização: {e}", flush=True)
        raise e

class ProcessController:
    def __init__(self):
        self.processes = {}
        self.coords_queue = mprocessing.Queue(maxsize=1)
        self.stop_event = mprocessing.Event()

    def create_process(self, name: str, target, args=()) -> None:
        """Create a new process with a queue"""
        self.processes[name] = mprocessing.Process(
            target=target,
            args=(self.coords_queue, *args)
        )

    def start_all(self) -> None:
        """Start all registered processes"""
        self.stop_event = mprocessing.Event()
        for process in self.processes.values():
            process.start()

    def stop_all(self) -> None:
        """Stop all processes"""
        if self.stop_event:
            self.stop_event.set()
        
        for process in self.processes.values():
            if process.is_alive():
                process.join(timeout=1.0)
                if process.is_alive():
                    process.terminate()
        
        self.processes.clear()
        self.coords_queue = None
        self.stop_event = None