import tkinter as tk
import os
import json
import threading
from mouse_control import start_mouse_control


class MouseControlInterface:
    def __init__(self, root):
        self.is_mouse_on = False
        self.config = self.load_config()

        self.root = root
        self.root.title("Controle de Mouse Virtual")

        # Create the interface
        self.create_interface()

    def create_interface(self):
        """Create the graphical interface with the control buttons."""
        # Frame for control buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Start and Stop buttons
        btn_start = tk.Button(button_frame, text="Liga Mouse", command=lambda: threading.Thread(target=self.run_mouse_control).start())
        btn_start.pack(side="left", padx=10)

        btn_stop = tk.Button(button_frame, text="Desliga Mouse", command=self.stop_mouse_control)
        btn_stop.pack(side="left", padx=10)

        # Frame for configuration entries
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(pady=10)

        # Create labels and entry fields for each variable
        self.create_entry(entry_frame, "Ponteiro do mouse", "MousePointerPoint")
        self.create_entry(entry_frame, "Referencia para o clique:", "MouseReference")
        self.create_entry(entry_frame, "Ponto para o clique", "MouseClickRef")
        self.create_entry(entry_frame, "Sensibilidade eixo X:", "MouseSensibility_X")
        self.create_entry(entry_frame, "Sensibilidade eixo Y:", "MouseSensibility_Y")
        self.create_entry(entry_frame, "Desvio eixo X:", "ScreenOffSet_width")
        self.create_entry(entry_frame, "Desvio eixo U:", "ScreenOffSet_height")
        self.create_entry(entry_frame, "Distancia para Click:", "DistanciaClick")
        self.create_entry(entry_frame, "Duracao do movimento:", "DurationMove")

        # Update button to apply the changes
        update_button = tk.Button(self.root, text="Update", command=self.update_values)
        update_button.pack(pady=10)

        # Label to display the result
        self.result_label = tk.Label(self.root, text="", fg="green")
        self.result_label.pack(pady=10)

    def create_entry(self, parent, label_text, config_key):
        """Helper function to create a label and entry field for a config variable."""
        frame = tk.Frame(parent)
        frame.pack(fill="x", pady=5)

        label = tk.Label(frame, text=label_text, width=20, anchor="w")
        label.pack(side="left", padx=5)

        entry = tk.Entry(frame)
        entry.pack(side="left", fill="x", expand=True, padx=5)
        entry.insert(0, self.config[config_key])

        setattr(self, f"{config_key}_entry", entry)

    def update_values(self):
        try:
            # Update the configuration dictionary with the new values
            self.config["MousePointerPoint"] = int(self.MousePointerPoint_entry.get())
            self.config["MouseReference"] = int(self.MouseReference_entry.get())
            self.config["MouseClickRef"] = int(self.MouseClickRef_entry.get())
            self.config["MouseSensibility_X"] = float(self.MouseSensibility_X_entry.get())
            self.config["MouseSensibility_Y"] = float(self.MouseSensibility_Y_entry.get())
            self.config["ScreenOffSet_width"] = float(self.ScreenOffSet_width_entry.get())
            self.config["ScreenOffSet_height"] = float(self.ScreenOffSet_height_entry.get())
            self.config["DistanciaClick"] = int(self.DistanciaClick_entry.get())
            self.config["DurationMove"] = float(self.DurationMove_entry.get())
            
            try:
                with open("config.json", "w") as f:
                    json.dump(self.config, f, indent=4)
                print("Config updated successfully")
            except Exception as e:
                print(f"Error writing to config.json: {e}")
            
        except ValueError:
            self.result_label.config(text="Please enter valid numeric values")

    def mouse_on_func(self):
        return self.mouse_on

    def run_mouse_control(self):
        """Executa o controle do mouse em uma thread."""
        self.mouse_on = True
        self.update_values()
        self.set_env_vars()
        start_mouse_control(self.mouse_on_func)

    def set_env_vars(self):
        for key, value in self.config.items():
            os.environ[key] = str(value)

    def stop_mouse_control(self):
        """Para o controle do mouse."""
        self.mouse_on = False
        print("Mouse control stopped")

    def load_config(self):
        config = {}
        
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    config = json.load(f)
                    return config
            except json.JSONDecodeError:
                print("Error: config.json is not valid JSON")
            except Exception as e:
                print(f"Error reading config.json: {e}")
        
        # Default config dict
        config = {
            "MousePointerPoint": 8,
            "MouseSensibility_X": 1.4,
            "MouseSensibility_Y": 1.2,
            "ScreenOffSet_width": 0.2,
            "ScreenOffSet_height": 0.3,
            "MouseReference": 4,
            "MouseClickRef": 12,
            "DistanciaClick": 50,
            "DurationMove": 0.01
        }
        return config

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseControlInterface(root)
    root.mainloop()