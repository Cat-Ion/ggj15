import cv2
import numpy
import pygame
import time
import camera
import gamemaths
import graphics

def cv2_img_to_pygame(img):
    return pygame.image.frombuffer(cv2.cvtColor(img, cv2.COLOR_BGR2RGB).tostring(), img.shape[1::-1], "RGB")

def cv2_grayimg_to_pygame(img):
    return pygame.image.frombuffer(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB).tostring(), img.shape[1::-1], "RGB")

graphics.init()
camera.init()
camera.calibrate(graphics.screen)

while True:
    line = gamemaths.fit_line(camera.get_line(0,
                                              graphics.draw_lines),
                              100)
    print(line)
    pygame.display.flip()
