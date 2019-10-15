import cv2
import numpy as np
import winsound



def main():

    cap = cv2.VideoCapture(0)
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])

    if cap.isOpened():

        ret, frame = cap.read()


    else:   

        ret = False


    while ret:

        ret, frame = cap.read()

        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second

        frame = numpy.array(frame)

        cv2.rectangle(frame, (20,320),(150,440) , (0,255,0), 3)
    
        
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        

        mask1 =  cv2.inRange(frameHSV, lower_red, upper_red)

        #res = cv2.bitwise_and(frame,frame, mask= mask1)


        kernelOpen = np.ones((10,10))
        kernelClose = np.ones((20,20))
        
        maskOpen = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernelOpen)
        maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)

        maskFinal = maskClose

        img, contours, h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        

        for contour in contours:

            area = cv2.contourArea(contour)

            if area > 500:

                cv2.drawContours(frame, contour, -1, (0,255,255), 3)


        for i in range(len(contours)):

            x, y, w, h = cv2.boundingRect(contour[i])
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)
            #print(x,y)


            if x>20 and y>320 and x+w<150 and y+h<440:

                cv2.rectangle(frame, (20,320),(150,440) , (0,255,255), 3)
        
                winsound.Beep(frequency, duration)

        


        cv2.imshow("Frame", frame)
        
        #cv2.imshow("FrameHSV", frameHSV)
        #cv2.imshow("MASK", mask1)
        #cv2.imshow("MASKq", maskClose)
        


        if cv2.waitKey(1) == 13:

            break

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":

    main()

