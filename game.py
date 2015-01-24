import cv2
import numpy
import pygame
import time
import camera

screen = None

def cv2_img_to_pygame(img):
    return pygame.image.frombuffer(cv2.cvtColor(img, cv2.COLOR_BGR2RGB).tostring(), img.shape[1::-1], "RGB")

def cv2_grayimg_to_pygame(img):
    return pygame.image.frombuffer(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB).tostring(), img.shape[1::-1], "RGB")

def init():
    global screen
    global matrix

    pygame.init()
    screen = pygame.display.set_mode((640, 480))

init()
camera.init()
camera.calibrate(screen)

screen.fill((0,0,0))
pygame.display.flip()

green_points = []
red_points = []

while True:
    rimg = None
    gimg = None
    bimg = None

    img = camera.acquire()
    screen.blit(cv2_img_to_pygame(img),      pygame.Rect(  0,   0, 640, 480))
    green_point, red_point = camera.grab_points(img)

    if green_point:
        green_points.append(green_point)
        green_points = green_points[-20:]
    if red_point:
        red_points.append(red_point)
        red_points = red_points[-20:]

    if(len(green_points) > 1): pygame.draw.lines(screen, (0,255,0), False, green_points, 3)
    if(len(red_points) > 1):   pygame.draw.lines(screen, (255,0,0), False, red_points, 3)

    pygame.display.flip()
