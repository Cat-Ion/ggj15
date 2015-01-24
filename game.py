import cv2
import numpy
import pygame
import time

screen = None
capture = None
camera_to_screen = None
means = None

def cv2_img_to_pygame(img):
    return pygame.image.frombuffer(cv2.cvtColor(img, cv2.COLOR_BGR2RGB).tostring(), img.shape[1::-1], "RGB")

def cv2_grayimg_to_pygame(img):
    return pygame.image.frombuffer(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB).tostring(), img.shape[1::-1], "RGB")

def init():
    global screen
    global capture
    global matrix

    pygame.init()
    screen = pygame.display.set_mode((640, 720))

    capture = cv2.VideoCapture(1)

def calibrate():
    global camera_to_screen
    global means

    chess = pygame.image.load("img/chess.png")
    screen.blit(chess, pygame.Rect(0,0,640,480))
    pygame.display.flip()

    ret, corners2 = cv2.findChessboardCorners(cv2.imread("img/chess.png"), (7,5))
    if not ret:
        raise Exception("Detection error in the calibration image")

    print("Position image and hit enter.")
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN and event.key == ord('\r'):
            break

    while True:
        ret, img = capture.read()
        if not ret:
            raise Exception("Camera error")

        ret, corners = cv2.findChessboardCorners(img, (7,5))
        if not ret:
            continue
            raise Exception("Detection error in the camera image")

        camera_to_screen, mask = cv2.findHomography(corners, corners2)

        if camera_to_screen[0][0] > 0:
            break
        else:
            camera_to_screen = numpy.dot(numpy.matrix(((-1, 0, 640), (0, -1, 480), (0,0,1))), camera_to_screen)
    print(camera_to_screen)
    
    screen.fill((255,255,255))
    pygame.display.flip()
    for i in range(5): capture.read()
    ret, img = capture.read()
    img = cv2.warpPerspective(img, camera_to_screen, (640, 480))
    img = cv2.resize(img, (320,240))
    bimg, gimg, rimg = cv2.split(img)

    means = [bimg.mean(), gimg.mean(), rimg.mean()]
    print(means)

def filter_green(img):
    h,s,v = cv2.split(img)
    h = 255-cv2.absdiff(h, 60)
    h = cv2.dilate(h, numpy.ones((5,5), numpy.uint8))
    h = cv2.erode(h, numpy.ones((9,9), numpy.uint8))
    screen.blit(cv2_grayimg_to_pygame(h),  pygame.Rect(320, 480, 320,  0))
    s = cv2.dilate(s, numpy.ones((5,5), numpy.uint8))
    return cv2.threshold(numpy.uint8(255. * cv2.multiply(cv2.multiply(cv2.multiply(h/255., h/255.), s/255.), v/255.)), 30, 255, cv2.THRESH_TOZERO)[1]

def filter_red(img):
    global screen
    h,s,v = cv2.split(img)
    h = 2*(254-cv2.absdiff(h, 0))
    h = cv2.dilate(h, numpy.ones((5,5), numpy.uint8))
    h = cv2.erode(h, numpy.ones((9,9), numpy.uint8))
    screen.blit(cv2_grayimg_to_pygame(h),  pygame.Rect(  0, 480, 320,240))
    s = cv2.dilate(s, numpy.ones((5,5), numpy.uint8))
    return cv2.threshold(numpy.uint8(255. * cv2.multiply(cv2.multiply(cv2.multiply(h/255., h/255.), s/255.), v/255.)), 30, 255, cv2.THRESH_TOZERO)[1]

init()
calibrate()

print(type(camera_to_screen))

screen.fill((0,0,0))
pygame.display.flip()
time.sleep(1)
for i in range(5): capture.read()

green_points = []
red_points = []

while True:
    rimg = None
    gimg = None
    bimg = None

    ret,img = capture.read()

    img = cv2.warpPerspective(img, camera_to_screen, (640, 480))
    img = cv2.resize(img, (320,240))
    hsvimg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    green_tmp = filter_green(hsvimg)
    red_tmp   = filter_red(hsvimg)

    green_img = cv2.subtract(green_tmp, red_tmp)
    red_img = cv2.subtract(red_tmp, green_tmp)

    green_point = cv2.minMaxLoc(green_img)[-1]
    red_point = cv2.minMaxLoc(red_img)[-1]

    screen.blit(cv2_img_to_pygame(img),      pygame.Rect(  0,   0, 320,240))
    
    screen.blit(cv2_grayimg_to_pygame(red_img),  pygame.Rect(  0, 240, 320,240))
    screen.blit(cv2_grayimg_to_pygame(green_img),pygame.Rect(320, 240, 320,240))

    green_found, red_found = True, True
    if cv2.norm(green_point, red_point) < 20:
        if green_img[green_point[1], green_point[0]] > red_img[red_point[1], red_point[0]]:
            red_found = False
        else:
            green_found = False

    if green_found:
        green_points.append(green_point)
        green_points = green_points[-20:]
    if red_found:
        red_points.append(red_point)
        red_points = red_points[-20:]

    if(len(green_points) > 1): pygame.draw.lines(screen, (0,255,0), False, green_points, 3)
    if(len(red_points) > 1):   pygame.draw.lines(screen, (255,0,0), False, red_points, 3)

    #screen.blit(cv2_grayimg_to_pygame(rimg), pygame.Rect(320,   0, 320,240))
    #screen.blit(cv2_grayimg_to_pygame(gimg), pygame.Rect(  0, 240, 320,240))
    #screen.blit(cv2_grayimg_to_pygame(bimg), pygame.Rect(320, 240, 320,240))
    pygame.display.flip()
