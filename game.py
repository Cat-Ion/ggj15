import cv2
import numpy
import pygame
import time

screen = None
capture = None
camera_to_screen = None

def cv2_img_to_pygame(img):
    return pygame.image.frombuffer(cv2.cvtColor(img, cv2.COLOR_BGR2RGB).tostring(), img.shape[1::-1], "RGB")

def init():
    global screen
    global capture
    global matrix

    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    capture = cv2.VideoCapture(1)

def calibrate():
    global camera_to_screen

    chess = pygame.image.load("img/chess.png")
    screen.blit(chess, pygame.Rect(0,0,640,480))
    pygame.display.flip()

    time.sleep(3)

    ret, img = capture.read()
    if not ret:
        raise Exception("Camera error")

    ret, corners = cv2.findChessboardCorners(img, (7,5))

    if not ret:
        raise Exception("Detection error in the camera image")

    ret, corners2 = cv2.findChessboardCorners(cv2.imread("img/chess.png"), (7,5))
    
    if not ret:
        raise Exception("Detection error in the calibration image")

    camera_to_screen, mask = cv2.findHomography(corners, corners2)

    print(camera_to_screen)

init()
calibrate()

print(type(camera_to_screen))

for v in [cv2.CV_CAP_PROP_BRIGHTNESS, cv2.CV_CAP_PROP_CONTRAST, cv2.CV_CAP_PROP_SATURATION]:
    print(capture.get(v))

while True:
    screen.fill((0,0,0))
    pygame.display.flip()
    time.sleep(1)

    ret,img = capture.read()
    transformed = cv2.warpPerspective(img, camera_to_screen, (640, 480))
    screen.blit(cv2_img_to_pygame(transformed), pygame.Rect(0,0,640,480))
    pygame.display.flip()
    time.sleep(0.5)
