import cv2 as cv
import numpy as np

'''
Video proccessing
Colorspaces 
Morphological operations (opening, closing)
Srodek ciezkości piłki (suma współrzedcnych lub contours featuers)
ramka
'''

def main():
    video()
    #rgb_to_hsv()




def video():
    
    cap = cv.VideoCapture('movingball.mp4')

    while cap.isOpened():

        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        

      

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        lower_red = np.array([0,125,50])
        upper_red = np.array([15, 220,255])

        lower_rose = np.array([330, 100,100])
        upper_rose = np.array([350,255,255])
        
        
        lower_rose_2 = np.array([165,100,200])
        upper_rose_2 = np.array([185, 255,255])
        
        lower_rose_3 = np.array([165,80,170])
        upper_rose_3= np.array([185, 255,255])
        
        lower_orange = np.array([35,150,150])
        upper_orange = np.array([40, 255,255])
        
        lower_brown = np.array([16,200,200])
        upper_brown = np.array([25,250,250])

        mask_red = cv.inRange(hsv,lower_red,upper_red)
        mask_rose = cv.inRange(hsv,lower_rose,upper_rose)
        mask_rose_2 = cv.inRange(hsv,lower_rose_2,upper_rose_2)
        mask_rose_3 = cv.inRange(hsv,lower_rose_3,upper_rose_3)
        mask_orange = cv.inRange(hsv,lower_orange,upper_orange)

        mask_brown = cv.inRange(hsv,lower_brown,upper_brown)


        mask = mask_red | mask_rose | mask_rose_2 |  mask_rose_3 | mask_orange
        
        kernel_closing = np.ones((2,2), np.uint8)
        closing = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel_closing)
        #mask = np.subtract(mask_brown, mask)
        res = cv.bitwise_and(frame,frame,mask=closing)

        h, s, v1 = cv.split(res)

        ret,thresh = cv.threshold(v1,127,255,0)
        contours,hierarchy = cv.findContours(thresh, cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

        cnt = contours[0]
        M = cv.moments(cnt)
        print( M )

        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            # set values as what you need in the situation
            cx, cy = 0, 0

        (x,y),radius = cv.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        cv.circle(res,center,radius,(0,255,0),2)
        cv.circle(res,center, 1, (0,255,0),2)
        cv.imshow('frame', frame)
        cv.imshow('mask', closing)
        cv.imshow('res', res)


        if cv.waitKey(1) == ord('q'):
            break
    
    cap.release()
    cv.destroyAllWindows()

def rgb_to_hsv():
    green = np.uint8([[[86,118,145 ]]])
    hsv_green = cv.cvtColor(green,cv.COLOR_BGR2HSV)
    print( hsv_green )
if __name__ == '__main__':
    main()