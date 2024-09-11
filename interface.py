import tkinter as tk
import threading
from mouse_control import start_mouse_control

mouse_on = False  # Variável global de controle

def is_mouse_on():
    """Retorna o estadu atual do mouse_on"""
    global mouse_on
    return mouse_on

def run_mouse_control():
    """Executa o controle do mouse em uma thread."""
    global mouse_on
    mouse_on = True
    start_mouse_control(is_mouse_on)

def stop_mouse_control():
    """Para o controle do mouse."""
    global mouse_on
    mouse_on = False
    print("Mouse control stopped")

def create_interface():
    """Cria a interface gráfica com os botões de controle."""
    root = tk.Tk()
    root.title("Controle de Mouse Virtual")

    btn_start = tk.Button(root, text="Liga Mouse", command=lambda: threading.Thread(target=run_mouse_control).start())
    btn_start.pack(pady=10)

    btn_stop = tk.Button(root, text="Desliga Mouse", command=stop_mouse_control)
    btn_stop.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_interface()