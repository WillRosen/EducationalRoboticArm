import pygame
import ERA

#This code will allow the user to use the Inverse Kinematic controls, 
#but using the computer's keyboard

#These values will store the values we want to send to the robotic arm
xVal=0
yVal=100
zVal=100
gripVal=90

#These values are used to change the values above
xChanger=0
yChanger=0
zChanger=0
gripChanger=0

#This is how fast the values we want to send will change
sensitivity=10

#As we do not know the MAC Address of the Bluetooth device when
#we first run the program, this will scan the network for any
#compatible devices, and attempt to connect with them
if(ERA.autoConnect()):

    #If we connect to the robotic arm, we can set up the window more
    #Here I am initialising the font and pyGame
    pygame.font.init()
    pygame.init()
    pygame.display.set_caption('Educational Robotic Arm')
    screen = pygame.display.set_mode((300, 125))
    screen.fill((100,100,100))
    try:
        programIcon = pygame.image.load('ERA/ERAIcon.ico')
        pygame.display.set_icon(programIcon)
    except:
        print("No Icon For Window Found")
    myfont = pygame.font.SysFont('Times New Roman', 20)

    #Now the font is set up, I can display the controls to the user
    #These values store the control text
    s0="Controls"
    s1="Change X - A/D"
    s2 = "Change Z - W/S"
    s3="Change Y - Left Shift/Left Control"
    s4 = "Close Gripper - E"
    s5 = "Open Gripper - Q"

    #This displays the text on screen for the user
    textsurface = myfont.render(s0, False, (255, 255, 255))
    screen.blit(textsurface,(0,0))

    textsurface = myfont.render(s1, False, (255, 255, 255))
    screen.blit(textsurface,(0,20))

    textsurface = myfont.render(s2, False, (255, 255, 255))
    screen.blit(textsurface,(0,40))

    textsurface = myfont.render(s3, False, (255, 255, 255))
    screen.blit(textsurface,(0,60))

    textsurface = myfont.render(s4, False, (255, 255, 255))
    screen.blit(textsurface,(0,80))

    textsurface = myfont.render(s5, False, (255, 255, 255))
    screen.blit(textsurface,(0,100))

    pygame.display.flip()

    #While we are in the 'game' or window
    while 1:

        #Get the keyboard information
        pygame.event.pump() 
        
        #Key presses are handles as events
        for event in pygame.event.get():
            #On the event we quit the game, stop the code
            if (event.type == pygame.QUIT):
                pygame.quit()
                exit()

            #On the event we press a key which controls
            #The Robotic Arm
            #Then set the changer value to nonzero
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_a):
                    xChanger=sensitivity
                if event.key == pygame.K_d:
                    xChanger=-sensitivity
                if (event.key == pygame.K_w):
                    zChanger=sensitivity
                if event.key == pygame.K_s:
                    zChanger=-sensitivity
                if (event.key == pygame.K_LSHIFT):
                    yChanger=sensitivity
                if event.key == pygame.K_LCTRL:
                    yChanger=-sensitivity
                if (event.key == pygame.K_e):
                    gripChanger=sensitivity
                if event.key == pygame.K_q:
                    gripChanger=-sensitivity

            #On the event we release a key which controls
            #The Robotic Arm
            #Then set the changer value to zero      
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    xChanger=0
                if event.key == pygame.K_d:
                   xChanger=0
                if (event.key == pygame.K_w):
                    zChanger=0
                if event.key == pygame.K_s:
                    zChanger=-0
                if (event.key == pygame.K_LSHIFT):
                    yChanger=0
                if event.key == pygame.K_LCTRL:
                    yChanger=-0
                if (event.key == pygame.K_q):
                    gripChanger=0
                if event.key == pygame.K_e:
                    gripChanger=-0
        
        #Now we apply the changes to the values 
        #That we want to send
        xVal+=xChanger
        zVal+=zChanger
        yVal+=yChanger
        gripVal+=gripChanger
    
        #Adding an upper and lower limits for better control
        gripVal=min(180,max(gripVal,0))
        xVal=min(200,max(xVal,-200))
        yVal=min(200,max(yVal,-200))
        zVal=min(200,max(zVal,-200))

        #Now we have all of the values, we can send it 
        #To the robotic arm
        ERA.setEulerCoodinates(xVal,yVal,zVal)
        ERA.setRotation(1,gripVal)



       


        