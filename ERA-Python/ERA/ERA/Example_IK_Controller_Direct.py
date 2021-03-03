import pygame
import ERA

#This code will allow the user to use the Inverse Kinematic controls, 
#but using a GamePad/Controller which is connected by USB to the computer

#These values will store the values we want to send to the robotic arm
xVal=0
yVal=100
zVal=100
gripVal=90

#The sensitivity of the gamepad's controls, higher means faster movement
sensitivity=15



#As we do not know the MAC Address of the Bluetooth device when
#we first run the program, this will scan the network for any
#compatible devices, and attempt to connect with them
if(ERA.autoConnect()):

    #If we connect to the robotic arm, we can set up the window more
    #Here I am initialising the font, gamepad(joystick) and pyGame
    pygame.font.init()
    pygame.joystick.init()
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
    s1="X - Right Stick Horizontal"
    s2 = "Z - Right Stick Vertical"
    s3="Y - Left Stick Vertical"
    s4 = "Gripper - Right Trigger"

    

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

    pygame.display.flip()

    joystick = None
    try:
        joystick = pygame.joystick.Joystick(0)
    except:
        print("\n\n>>>No Joystick Detected!<<<\n\n")
        quit()
    joystick.init()

    #While we are in the 'game' or window
    while 1:

        #Get joystick information
        pygame.event.pump() 
  

       

        #Read the joystick values and cllamp them between 
        #their respective ranges
        gripVal=min(180,max((joystick.get_axis(5)+1)*180,0))
        xVal=min(200,max(-joystick.get_axis(2)*150,-200))
        yVal=min(200,max(-joystick.get_axis(1)*100+100,-200))
        zVal=min(200,max(-joystick.get_axis(3)*100+100,-200))

        #Now we have all of the values, we can send it 
        #To the robotic arm
        ERA.setEulerCoodinates(xVal,yVal,zVal)
        ERA.setRotation(1,gripVal)

        #In the event we close the window, stop the code
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                exit()


        