import cv2
import numpy
import pygame


capture = None
camera_to_screen = None
min_vals = [0,0]

def init():
    global capture
    capture = cv2.VideoCapture(0)

def calibrate(screen):
    global camera_to_screen
    global min_vals

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
            print("Retrying")
            continue
        break

    camera_to_screen, mask = cv2.findHomography(corners, corners2)

    if camera_to_screen[0][0] < 0:
        camera_to_screen = numpy.dot(numpy.matrix(((-1, 0, 640), (0, -1, 480), (0,0,1))), camera_to_screen)

    screen.fill((255,0,0))
    pygame.display.flip()
    for i in range(10): acquire()
    img = cv2.cvtColor(acquire(), cv2.COLOR_BGR2HSV)
    green = filter_green(img)
    red = filter_red(img)
    red_val = filter_combined(img, green, red)[1][1]

    screen.fill((0,255,0))
    pygame.display.flip()
    for i in range(10): acquire()
    img = cv2.cvtColor(acquire(), cv2.COLOR_BGR2HSV)
    green = filter_green(img)
    red = filter_red(img)
    green_val = filter_combined(img, green, red)[1][0]

    min_vals = [green_val, red_val]
    print(min_vals)

    screen.fill((0,0,0))
    pygame.display.flip()
    for i in range(10): acquire()
    
def acquire():
    ret, img = capture.read()
    if not ret:
        raise Exception("Reading camera failed")
        
    img = cv2.warpPerspective(img, camera_to_screen, (640, 480))
    return img

def grab_points(img):
    return grab_points_hsv(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))

def grab_points_hsv(hsvimg):
    green_tmp = filter_green(hsvimg)
    red_tmp   = filter_red(hsvimg)
    return filter_combined(hsvimg, green_tmp, red_tmp)[0]

def filter_green(img):
    h,s,v = cv2.split(img)
    h = 255-cv2.absdiff(h, 60)
    h = cv2.dilate(h, numpy.ones((5,5), numpy.uint8))
    h = cv2.erode(h, numpy.ones((5,5), numpy.uint8))
    s = cv2.dilate(s, numpy.ones((5,5), numpy.uint8))
    return numpy.uint8(255. * cv2.multiply(cv2.multiply(cv2.multiply(h/255., h/255.), s/255.), v/255.))

def filter_red(img):
    h,s,v = cv2.split(img)
    h = 2*(254-cv2.absdiff(h, 0))
    h = cv2.dilate(h, numpy.ones((5,5), numpy.uint8))
    h = cv2.erode(h, numpy.ones((5,5), numpy.uint8))
    s = cv2.dilate(s, numpy.ones((5,5), numpy.uint8))
    return numpy.uint8(255. * cv2.multiply(cv2.multiply(cv2.multiply(h/255., h/255.), s/255.), v/255.))

def filter_combined(img, green_tmp, red_tmp):
    green_img = cv2.subtract(green_tmp, red_tmp)
    red_img = cv2.subtract(red_tmp, green_tmp)

    green_val = cv2.minMaxLoc(green_img)
    red_val = cv2.minMaxLoc(red_img)

    green_point = green_val[-1]
    red_point = red_val[-1]

    green_found, red_found = True, True
    if green_point == (0,0) or green_val[1] < min_vals[0]:
        green_found = False
    if red_point == (0,0) or red_val[1] < min_vals[1]:
        red_found = False
    if cv2.norm(green_point, red_point) < min_vals[0]:
        if green_img[green_point[1], green_point[0]] > red_img[red_point[1], red_point[0]]:
            red_found = False
        else:
            green_found = False

    return ((green_point if green_found else None,
             red_point   if red_found   else None),
            (green_val[1], red_val[1]))


def get_line(player, callback):
    empty_frames = 0
    points = []
    while True:
        point = grab_points(acquire())[player]
        if point:
            break

    while empty_frames < 5 or len(points) < 2:
        point = grab_points(acquire())[player]
        if point == None:
            empty_frames += 1
            continue
        empty_frames = 0
        if len(points) > 0 and cv2.norm(point, points[-1]) < 10:
            points[-1] = (
                0.5 * point[0] + 0.5 * points[-1][0],
                0.5 * point[1] + 0.5 * points[-1][1])
        else:
            points.append(point)
        points = points[-20:]
        if callback != None and len(points) > 1:
            callback(points)
    return points
        
