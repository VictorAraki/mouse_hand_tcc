import tkinter as tk
from tkinter import simpledialog, Toplevel, Label, Scale, HORIZONTAL
import threading
from mouse_control import start_mouse_control

mouse_on = False  # Variável global de controle

# Função para verificar o estado do mouse
def is_mouse_on():
    """Retorna o estadu atual do mouse_on"""
    global mouse_on
    return mouse_on

# Função que roda o controle do mouse em uma nova thread
def run_mouse_control():
    """Executa o controle do mouse em uma thread."""
    global mouse_on
    mouse_on = True
    start_mouse_control(is_mouse_on)

# Função para parar o controle do mouse
def stop_mouse_control():
    """Para o controle do mouse."""
    global mouse_on
    mouse_on = False
    print("Mouse control stopped")

# Função para ajustar parâmetros de detecção
def adjust_mouse_settings():
    """Abre uma nova janela para ajustar as configurações do mouse."""
    def apply_settings():
        global detection_confidence
        detection_confidence = conf_scale.get() / 100  # Ajustando de 0 a 1
        print(f"Confiança ajustada para: {detection_confidence}")

    settings_window = Toplevel()
    settings_window.title("Ajustar Mouse")
    
    # Label e controle deslizante para ajuste da confiança
    Label(settings_window, text="Ajuste o nível de confiança:").pack(pady=10)
    conf_scale = Scale(settings_window, from_=10, to=100, orient=HORIZONTAL)
    conf_scale.set(80)  # Valor padrão
    conf_scale.pack(pady=10)
    
    # Botão para aplicar as configurações
    tk.Button(settings_window, text="Aplicar", command=apply_settings).pack(pady=10)

# Função que cria a interface
def create_interface():
    """Cria a interface gráfica com os botões de controle."""
    root = tk.Tk()
    root.title("Controle de Mouse Virtual")

    # Configurando o layout
    root.geometry("300x200")  # Tamanho fixo da janela

    # Botão para ligar o mouse
    btn_start = tk.Button(root, text="Liga Mouse", command=lambda: threading.Thread(target=run_mouse_control).start())
    btn_start.pack(pady=10, padx=20)
    # Botão para desligar o mouse
    btn_stop = tk.Button(root, text="Desliga Mouse", command=stop_mouse_control)
    btn_stop.pack(pady=10, padx=20)

    # Botão para ajustar o mouse
    btn_adjust = tk.Button(root, text="Regula Mouse", command=adjust_mouse_settings)
    btn_adjust.pack(pady=10, padx=20)

    # Iniciando o loop da interface
    root.mainloop()

if __name__ == "__main__":
    create_interface()