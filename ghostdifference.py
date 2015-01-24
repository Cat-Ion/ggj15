from numpy import *
import cv2, time

cap = cv2.VideoCapture(0)

oldimg = None

def rot90(img):
    img = cv2.transpose(img)
    img = cv2.flip(img,1)
    return img

try:
    while 1:
        ret, img = cap.read()
        if not ret: raise Exception("Camera error")
        if oldimg==None: oldimg = img


        #dimg = img - oldimg
        dimg = cv2.subtract(img, oldimg)
        oldimg = img        

        dimg = rot90(dimg)
        
        cv2.imshow('frame', dimg )

        if cv2.waitKey(1) & 0xFF == ord('q'): break
        if cv2.waitKey(1) & 0xFF == ord('s'):
            print 'Save frame'
            cv2.imwrite('frame.png', gimg)

finally:
    cap.release()
    cv2.destroyAllWindows()
