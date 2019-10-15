import cv2
import numpy as np
import winsound

f = 500  
d = 500
kernelOpen = np.ones((10,10))
kernelClose = np.ones((20,20))
lb=np.array([80,100,100])
ub=np.array([100,255,255])

cap=cv2.VideoCapture(0)

while(True):

    ret,frame=cap.read()
    #cv2.rectangle(frame, (100,320),(340,440) , (0,0,255), 3)

    cv2.rectangle(frame,(430,10),  (560,128),(0,255,0),3)#top right
    cv2.rectangle(frame,(50,10),  (180,128),(0,255,0),3)#top left
    cv2.rectangle(frame, (50,320),(180,440) , (0,255,0), 3)#bottom left
    cv2.rectangle(frame, (240,320),(370,440) , (0,255,0), 3)#bottom middle
    cv2.rectangle(frame, (430,320),(560,440) , (0,255,0), 3)#bottom right

    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv=cv2.cvtColor( blurred_frame,cv2.COLOR_BGR2HSV)
    
    
    mask = cv2.inRange(hsv,lb,ub)

    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)

    maskFinal = maskClose

    a , contour, b = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)
    for contours in contour:
        area = cv2.contourArea(contours)
        if area > 1000:
            cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)
           # print(area)
    #for i in range(len(contour)):
     #   x, y, w, h = cv2.boundingRect(contour[i])
      #  cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)
#top left
    for i in range(len(contour)):
            x1, y1, w1, h1 = cv2.boundingRect(contour[i])
            if x1>50 and y1>10 and x1+w1<180 and y1+h1<128:
                cv2.rectangle(frame, (x1,y1), (x1+w1,y1+h1), (0,0,0), 3)
                winsound.Beep(f,d)
    #top right
            a, b, c, d = cv2.boundingRect(contour[i])
            if a>430 and b>10 and a+c<560 and b+d<128:
                 cv2.rectangle(frame, (a,b), (a+c,b+d), (0,0,0), 3)
                 winsound.Beep(f,d)
    #bottom left
            x3, y3, w3, h3 = cv2.boundingRect(contour[i])
            if x3>50 and y3>320 and x3+w3<180 and y3+h3<440:
                 cv2.rectangle(frame, (x3,y3), (x3+w3,y3+h3), (0,0,0), 3)
                 winsound.Beep(f,d)
    #bottom middle
        
            x4, y4, w4, h4 = cv2.boundingRect(contour[i])
            if x4>240 and y4>320 and x4+w4<370 and y4+h4<440:
                 cv2.rectangle(frame, (x4,y4), (x4+w4,y4+h4), (0,0,0), 3)
                 winsound.Beep(f,d)
    #bottom right
            x5, y5, w5, h5 = cv2.boundingRect(contour[i])
            if x5>430 and y5>320 and x5+w5<560 and y5+h5<440:
                 cv2.rectangle(frame, (x5,y5), (x5+w5,y5+h5), (0,0,0), 3)
                 winsound.Beep(f,d)

        
                #print(x,y)
   # for c in contour:
    #    x, y, w, h = cv2.boundingRect(c)
    #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    cv2.imshow("Frame", frame)
    cv2.imshow("contors", mask)
    if cv2.waitKey(1) & 0xff==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
