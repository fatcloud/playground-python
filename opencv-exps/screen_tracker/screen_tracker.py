import cv2
import numpy as np
from motion_detect import MotionDetector
from cam import MyCam

# cam = MyCam()

if __name__ == '__main__':
    img = np.full((600,800,3), 0, np.uint8)

    m_255 = np.full((600,800), 255, np.uint8)
    m_0 = np.full((600,800), 0, np.uint8)

    img[:,:,0] = m_255[:,:]
    index = 0
    
    cam = MyCam()
    md = MotionDetector(N=2, shape=cam.read().shape)
    
    while True:
        
        # turn off the previous bias
        img[:, :, index] = m_0
        
        # now turn on the next
        index = (index + 1) % 3
        img[:, :, index] = m_255
        
        cam_img = cam.read()
        md.feed_image(cam_img)
        gray_diff = cv2.cvtColor(md.diff, cv2.COLOR_BGR2GRAY)
        blured = cv2.blur(gray_diff, (5,5))
        
        # edges = cv2.Canny(gray_diff, 100, 200)
        _, th = cv2.threshold(blured, 20, 255, cv2.THRESH_BINARY)
        
        contours, hry = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # screens = []
        # for ctr in contours:
            # epsilon = 0.2*cv2.arcLength(ctr,True)
            # tmp = cv2.approxPolyDP(ctr,epsilon,True)
            # print len(tmp), cv2.contourArea(tmp)
            # if len(tmp) == 4 and cv2.contourArea(tmp) > 1000:
                # screens.append(tmp)
        
        # for tmp in screens:
        cv2.drawContours(th, contours, 0, (0, 0, 255))
        print contours
        cv2.imshow('motion', th)
        cv2.imshow('BGR', img)
        k = cv2.waitKey(500)
        if k == 27:
            break