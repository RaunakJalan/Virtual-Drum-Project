import pygame
from pygame.locals import *
import cv2
import numpy
import sys
import winsound




cap=cv2.VideoCapture(0)


cap.set(3,1920)
cap.set(4,1080)


lower_red = numpy.array([-10,100,100])
upper_red = numpy.array([10,255,255])
lower_blue = numpy.array([80,100,100])
upper_blue = numpy.array([100,255,255])
frequencybeep = 2500  # Set Frequency To 2500 Hertz
durationbeep = 50  # Set Duration To 1000 ms == 1 second
kernelOpen = numpy.ones((10,10))
kernelClose = numpy.ones((20,20))



retval,frame=cap.read()

cv2.flip(frame,1,frame)#mirror the image

screen_width, screen_height = 800, 600
screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

screen.fill(0) 
    
running=True
while running:



    retval,frame=cap.read()


    frame=numpy.rot90(frame)

    

    frame = numpy.ascontiguousarray(frame, dtype=numpy.uint8)

    

    cv2.rectangle(frame, (450,200),(550,300) , (0,255,0), 2)
    cv2.rectangle(frame, (450,600),(550,700) , (0,255,0), 2)
    cv2.rectangle(frame, (450,1000),(550,1100) , (0,255,0), 2)
    cv2.rectangle(frame, (250,400),(350,500) , (0,255,0), 2)
    cv2.rectangle(frame, (250,800),(350,900) , (0,255,0), 2)

    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask1 =  cv2.inRange(frameHSV, lower_red, upper_red)
    mask2 = cv2.inRange(frameHSV, lower_blue, upper_blue)


    #res = cv2.bitwise_and(frame,frame, mask= mask1)

        
    maskOpen1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernelOpen)
    maskClose1 = cv2.morphologyEx(maskOpen1, cv2.MORPH_CLOSE, kernelClose)

    
    maskOpen2 = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, kernelOpen)
    maskClose2 = cv2.morphologyEx(maskOpen2, cv2.MORPH_CLOSE, kernelClose)

    maskClose = maskClose1 + maskClose2

    maskFinal = maskClose

    img, contours, h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        

    for contour in contours:

        area = cv2.contourArea(contour)

        if area > 100:

            cv2.drawContours(frame, contour, -1, (0,255,255), 3)

    

    for i in range(len(contours)):

        x, y, w, h = cv2.boundingRect(contour[i])
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)
        #print(x,y)


        if x>450 and y>200 and x+w<550 and y+h<300:

            cv2.rectangle(frame, (450,200),(550,300) , (0,255,255), 3)
        
            winsound.Beep(frequencybeep, durationbeep)

        elif x>450 and y>600 and x+w<550 and y+h<700:

            cv2.rectangle(frame, (450,600),(550,700) , (0,255,255), 3)
        
            winsound.Beep(frequencybeep, durationbeep)

        elif x>450 and y>1000 and x+w<550 and y+h<1100:

            cv2.rectangle(frame, (450,1000),(550,1100) , (0,255,255), 3)
        
            winsound.Beep(frequencybeep, durationbeep)

        elif x>250 and y>400 and x+w<350 and y+h<500:

            cv2.rectangle(frame, (250,400),(350,500) , (0,255,255), 3)
        
            winsound.Beep(frequencybeep, durationbeep)

        elif x>250 and y>800 and x+w<350 and y+h<900:

            cv2.rectangle(frame, (250,800),(350,900) , (0,255,255), 3)
        
            winsound.Beep(frequencybeep, durationbeep)

    
    framepygame = frame

    framepygame = cv2.cvtColor(framepygame, cv2.COLOR_BGR2RGB)
    
    framepygame=pygame.surfarray.make_surface(framepygame)
    
    framepygame = pygame.transform.scale(framepygame, (1920, 1080))
    

    
    
    screen.blit(framepygame,(0,0))
    
    pygame.display.update()
    
    for event in pygame.event.get(): #process events since last loop cycle

        if event.type == pygame.QUIT:
            running = False
                    
        
        if event.type == KEYDOWN:
            running=False


cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()
