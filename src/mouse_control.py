import cv2
import os
import pyautogui
import math


class PyAutoGuiHelper():
    def __init__(self, setup, config):
        self.screen_width = setup["screen_width"]
        self.screen_height = setup["screen_height"]
        self.frame_width = setup["frame_width"]
        self.frame_height = setup["frame_height"]
        self.sensibility_x = config['MouseSensibility_X']
        self.sensibility_y = config['MouseSensibility_Y']
        self.screen_offset_width = config['ScreenOffSet_width']
        self.screen_offset_height = config['ScreenOffSet_height']
        self.dist_click = config['DistanciaClick']
        self.duration = config['DurationMove']
        self.is_click = False
        self.is_hold = False

    def get_x_y(self, coords, point_key):
        x,y = coords[point_key]
        return x,y

    def move_mouse(self, x, y):
        """
        Move mouse pointer
        """
        # Calculate how to move mouse
        scale_x = self.screen_width / self.frame_width
        scale_y = self.screen_height / self.frame_height
        off_set_x = self.screen_width * self.screen_offset_width
        off_set_y = self.screen_height * self.screen_offset_height
        x_move = x * scale_x * self.sensibility_x - off_set_x
        y_move = y * scale_y * self.sensibility_y - off_set_y

        pyautogui.moveTo(x_move, y_move, duration=self.duration, tween=pyautogui.easeOutQuad)

    def _distancia_entre_pontos(self, x_ref, y_ref, x_ref_click, y_ref_click):
        # Calculando a distância euclidiana entre os dois pontos
        distancia = math.sqrt((x_ref_click - x_ref)**2 + (y_ref_click - y_ref)**2)
        return distancia

    def click_mouse(self,x_ref, y_ref, x_ref_click, y_ref_click):
        dist = self._distancia_entre_pontos(x_ref, y_ref, x_ref_click, y_ref_click)

        if dist < self.dist_click:
            if not self.is_click:
                pyautogui.click()
                self.is_click = True
            elif not self.is_hold:
                pyautogui.mouseDown()
                self.is_hold = True
        else:
            pyautogui.mouseUp()
            self.is_click = False
            self.is_hold = False

    def main_mouse(self, coords):
        x_move, y_move = self.get_x_y(coords, "MousePointerPoint")
        self.move_mouse(x_move, y_move)

        x_ref, y_ref = self.get_x_y(coords, "MouseReference")
        x_ref_click, y_ref_click = self.get_x_y(coords, "MouseClickRef")
        self.click_mouse(x_ref, y_ref, x_ref_click, y_ref_click)
        
