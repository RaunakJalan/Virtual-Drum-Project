#import pygame


'''
pygame.init()

screen = pygame.display.set_mode((320, 480))

while True:

    
    pygame.display.update()
'''


import math
import sys
import pygame
from pygame.locals import *
import cv2
import numpy
import time
import winsound
#from playsound import playsound




class MyGame(object):

    def __init__(self):
        self.listofcolors = [[0, 0, 0], [255, 0, 255], [60, 170, 70],
                            [0, 0, 255], [255, 165, 0], [255, 255, 0],
                            [199, 97, 20]]
        pygame.mixer.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()

        self.font = pygame.font.SysFont(None, 120)
        
        self.font1 = pygame.font.SysFont(None, 80)
        self.font2 = pygame.font.SysFont(None, 60)
        
        self.background_img = pygame.image.load("D://study material//Python//prog//Projects//opencv//drum//drumbackmain.png")
        self.background_img = pygame.transform.scale(self.background_img, (600, 500))


        self.colorcam=False#True#False
        
        self.width = 1200
        self.height = 1200
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        pygame.display.set_caption("AIR DRUM")

        self.bg_color = self.listofcolors[0]

        self.text_color = [255,255,255]

        self.white = (255,255,255)
        self.black = (0,0,0)
        self.red = (255,0,0)
        self.yellow = (200,200,0)
        self.green = (34,177,76)
        self.cyan = (0,255,255)

        self.title = self.font.render("!!! AIR DRUM !!!", True, self.text_color)
        
        self.bg_text1 = self.font1.render("Press H for Instructions!!", True, self.text_color)
        self.bg_text2 = self.font1.render("Press Enter to Start..", True, self.text_color)

        
        self.bg_text3 = self.font2.render("CREATED BY: ", True, self.text_color)
        self.bg_text4 = self.font2.render("       ->RAUNAK JALAN", True, self.text_color)
        self.bg_text5 = self.font2.render("       ->JAYA KUMAR", True, self.text_color)


        self.button_text_play = self.font2.render("PLAY", True, self.black)
        self.button_text_help = self.font2.render("HELP", True, self.black)
        self.button_text_quit = self.font2.render("QUIT", True, self.black)


        self.help_title = self.font.render("!!HELP!!", True, self.text_color)
        self.help_control1 = self.font1.render("Just hit the boxes with drum sticks and",True, self.text_color)
        self.help_control2 = self.font1.render("that will produce the sound",True, self.text_color)
        

        self.FPS = 30
        self.REFRESH = pygame.USEREVENT+1
        pygame.time.set_timer(self.REFRESH, 1000//self.FPS)

        pygame.mixer.music.load("D://study material//Python//prog//Projects//opencv//drum//Drumroll.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        

    def run(self):
        timer_cap = 30     # Frequenzy to change the background color
        cur_timer = 0      # Current timer to check against the timer_cap
        current_color = 0  # Current color index
        running = True

        
         
        while running:
        
            event = pygame.event.wait()
            #print(event)
            if event.type == pygame.QUIT:
                running = False

            elif event.type == self.REFRESH:
                self.draw()

            elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_h:

                        self.help()

                    if event.key == pygame.K_RETURN:

                        self.drumbackend()

                    if event.key == pygame.K_q:
                         running = False
                        

            else:
                pass


            # Here we control the background color
            if cur_timer == timer_cap:
                cur_timer = 0
                if current_color == len(self.listofcolors)-1:
                    current_color = 0
                else:
                    current_color += 1
                self.bg_color = self.listofcolors[current_color] 
            else:
                cur_timer += 1


    def drumbackend(self):
        
        pygame.mixer.music.pause()

        lower_red = numpy.array([-10,100,100])
        upper_red = numpy.array([10,255,255])
        lower_blue = numpy.array([80,100,100])
        upper_blue = numpy.array([100,255,255])
        frequencybeep = 2500  # Set Frequency To 2500 Hertz
        durationbeep = 50  # Set Duration To 1000 ms == 1 second
        kernelOpen = numpy.ones((10,10))
        kernelClose = numpy.ones((20,20))

        cap=cv2.VideoCapture(0)
        cap.set(3,1920)
        cap.set(4,1080)
    
        retval,frame=cap.read()
                        
        runningcam=True

        while runningcam:

                        
            cv2.flip(frame,1,frame)#mirror the image

            self.screen.fill(0) 

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

                if area > 1000:

                    cv2.drawContours(frame, contour, -1, (0,255,255), 3)


            for i in range(len(contours)):

                x, y, w, h = cv2.boundingRect(contour[i])
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)
                                    #print(x,y)


                if x>450 and y>200 and x+w<550 and y+h<300:

                    cv2.rectangle(frame, (450,200),(550,300) , (0,255,255), 3)
                                    
                    #playsound("D:\\study material\\Python\\prog\\Projects\\opencv\\drum\\drumsound\\sound 4-[AudioTrimmer.com].wav")
                    winsound.PlaySound("D:\\study material\\Python\\prog\\Projects\\opencv\\drum\\drumsound\\sound 5-[AudioTrimmer.com].wav",winsound.SND_ASYNC)

                elif x>450 and y>600 and x+w<550 and y+h<700:

                    cv2.rectangle(frame, (450,600),(550,700) , (0,255,255), 3)
                                    
                    #playsound("D:\\study material\\Python\\prog\\Projects\\opencv\\drum\\drumsound\\sound 5-[AudioTrimmer.com].wav")
                    winsound.PlaySound("D:\\study material\\Python\\prog\\Projects\\opencv\\drum\\drumsound\\sound 4-[AudioTrimmer.com].wav",winsound.SND_ASYNC)

                elif x>450 and y>1000 and x+w<550 and y+h<1100:

                    cv2.rectangle(frame, (450,1000),(550,1100) , (0,255,255), 3)
                                    
                    #playsound("D:\\study material\\Python\\prog\\Projects\\opencv\\drum\\drumsound\\sound 3-[AudioTrimmer.com].wav")
                    winsound.PlaySound("D:\\study material\\Python\\prog\\Projects\\opencv\\drum\\drumsound\\sound 3-[AudioTrimmer.com].wav",winsound.SND_ASYNC)

                elif x>250 and y>400 and x+w<350 and y+h<500:

                    cv2.rectangle(frame, (250,400),(350,500) , (0,255,255), 3)
                                    
                    #playsound("D:\\study material\\Python\\prog\\Projects\\opencv\\drum\\drumsound\\sound 2-[AudioTrimmer.com].mp3")
                    winsound.PlaySound("D:\\study material\\Python\\prog\\Projects\\opencv\\drum\\drumsound\\sound 2-[AudioTrimmer.com].wav",winsound.SND_ASYNC)

                elif x>250 and y>800 and x+w<350 and y+h<900:

                    cv2.rectangle(frame, (250,800),(350,900) , (0,255,255), 3)
                                    
                    #playsound("D:\\study material\\Python\\prog\\Projects\\opencv\\drum\\drumsound\\sound 1-[AudioTrimmer.com].wav")
                    winsound.PlaySound("D:\\study material\\Python\\prog\\Projects\\opencv\\drum\\drumsound\\sound 1-[AudioTrimmer.com].wav",winsound.SND_ASYNC)


                                
            framepygame = frame

            framepygame = cv2.cvtColor(framepygame, cv2.COLOR_BGR2RGB)
                                
            framepygame=pygame.surfarray.make_surface(framepygame)
                                
            framepygame = pygame.transform.scale(framepygame, (1920, 1080))
                                

                                
                                
            self.screen.blit(framepygame,(0,0))
                                
            pygame.display.update()

            for event in pygame.event.get():
            
                if event.type == pygame.QUIT:
                    runningcam = False
                    cap.release()
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                                        
                    if event.key == pygame.K_ESCAPE:

                        pygame.mixer.music.unpause()
                        runningcam = False
                        self.draw()

                    if event.key == pygame.K_q:

                        runningcam = False
                        cap.release()
                        pygame.quit()
                        sys.exit()
                                            

                                     
    def help(self):

        pygame.mixer.music.pause()

        helprunning = True
        
        while helprunning:

            for event in pygame.event.get():
            
                if event.type == pygame.QUIT:
                    helprunning = False
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_ESCAPE:

                        pygame.mixer.music.unpause()
                        helprunning = False
                        self.draw()

                    if event.key == pygame.K_q:

                        helprunning = False
                        pygame.quit()
                        sys.exit()

                else:
                    
                    self.screen.fill(self.cyan)
                    self.screen.blit(self.help_title, [750, 150])
                    self.screen.blit(self.help_control1, [450, 800])
                    self.screen.blit(self.help_control2, [450, 870])

                    self.screen.blit(self.background_img, (600, 250))

                    self.button('PLAY', 335, 332, 130, 70, (0,255,0), self.green , "play")
                    #self.button('HELP', 340, 483, 130, 70, (105,105,105), self.white, "help")
                    self.button('QUIT', 335, 632, 130, 70, (139,0,0), self.red, "quit")

                    self.screen.blit(self.button_text_play, [350, 350])
                    #self.screen.blit(self.button_text_help, [65, 267])
                    self.screen.blit(self.button_text_quit, [350, 650])
                    

                    pygame.display.flip()    

            


    def button(self,text,x,y,width,height,active_color, inactive_color,action):

        cur = pygame.mouse.get_pos()

        click = pygame.mouse.get_pressed()

        if x+width>cur[0]>x and y+height>cur[1]>y:

            pygame.draw.rect(self.screen, active_color, (x, y, width, height))

            if click[0] == 1 and action!=None:

                if action == "quit":

                    pygame.quit()
                    sys.exit()

                elif action == "play":

                    self.drumbackend()

                elif action == "help":

                    self.help()

                else:
                    pass
            

        else:
            pygame.draw.rect(self.screen, inactive_color, (x, y, width, height))
        


    

    def draw(self):
        self.screen.fill(self.bg_color)

        self.screen.blit(self.title, [580, 150])
        self.screen.blit(self.background_img, [600, 250])

        self.screen.blit(self.bg_text1, [580, 800])
        self.screen.blit(self.bg_text2, [580, 870])

        self.screen.blit(self.bg_text3, [1250, 400])
        self.screen.blit(self.bg_text4, [1250, 450])
        self.screen.blit(self.bg_text5, [1250, 500])


        self.button('PLAY', 335, 332, 130, 70, (0,255,0), self.green , "play")
        self.button('HELP', 340, 483, 130, 70, (105,105,105), self.white, "help")
        self.button('QUIT', 335, 632, 130, 70, (139,0,0), self.red, "quit")

        self.screen.blit(self.button_text_play, [350, 350])
        self.screen.blit(self.button_text_help, [350, 500])
        self.screen.blit(self.button_text_quit, [350, 650])

        
        
        pygame.display.flip()

 
                           


MyGame().run()

pygame.quit()
sys.exit()



'''

cur =  pygame.mouse.get_pos()

        if 140>cur[0]>40 and 220>cur[1]>170:

            pygame.draw.rect(self.screen, (0,255,0), (40, 170, 100, 50))

        else:
            pygame.draw.rect(self.screen, self.green, (40, 170, 100, 50))

        if 140>cur[0]>40 and 300>cur[1]>250:

            pygame.draw.rect(self.screen, (105,105,105), (40, 250, 100, 50))

        else:

            pygame.draw.rect(self.screen, self.white, (40, 250, 100, 50))

        if 140>cur[0]>40 and 380>cur[1]>330:

            pygame.draw.rect(self.screen, (139,0,0), (40, 330, 100, 50))

        else:

            pygame.draw.rect(self.screen, self.red, (40, 330, 100, 50))



        pygame.draw.rect(self.screen, self.green, (40, 170, 100, 50))
        pygame.draw.rect(self.screen, self.white, (40, 250, 100, 50))
        pygame.draw.rect(self.screen, self.red, (40, 330, 100, 50))


'''
