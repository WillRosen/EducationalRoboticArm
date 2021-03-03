import ERA
import time
import tkinter
from tkinter import *


#This code will allow the user to individually control each 
#servomotor on the robotic arm


#This will make a window and display "Loading!" while it
#attempts to connect to the robotic arm

window = tkinter.Tk()
greeting_var = tkinter.StringVar(window)

greeting = tkinter.Label(textvariable=greeting_var)
greeting_var.set("Attempting To Connect To ERA!")
greeting.pack()
window.title("Educational Robotic Arm")
window.geometry("400x400")
try:
    window.iconbitmap('ERA/ERAIcon.ico')
except:
    print("No Icon For Window Found")
    
window.update_idletasks()
window.update()



#As we do not know the MAC Address of the Bluetooth device when
#we first run the program, this will scan the network for any
#compatible devices, and attempt to connect with them
if(ERA.autoConnect()):
   
    #Change the text to let the user know they are connected
    greeting_var.set("Hello there!\nConnected")
    
    #Make 4 sliders,one for each servo with ranges from 0 degrees to 180 degrees
    #Also make the labels for them to say which servo is being controlled
    slider1 = Scale(window, from_=0, to=180, length=600,width=25, orient=HORIZONTAL)
    slider1.pack()
    label1 = Label(text="Gripper")
    label1.pack()

    slider2 = Scale(window, from_=0, to=180, length=600,width=25, orient=HORIZONTAL)
    slider2.pack()
    label2 = Label(text="Elbow")
    label2.pack()

    slider3 = Scale(window, from_=0, to=180, length=600,width=25, orient=HORIZONTAL)
    slider3.pack()
    label3 = Label(text="Shoulder")
    label3.pack()

    slider4 = Scale(window, from_=0, to=180, length=600,width=25, orient=HORIZONTAL)
    slider4.pack() 
    label4 = Label(text="Base")
    label4.pack()

    #Set up the sliders to have a default value of 90
    slider1.set(90)
    slider2.set(90)
    slider3.set(90)
    slider4 .set(90)

    #While the window is running, continuously update the rotation of each servo
    while(True):
        
        #The format is: setRotation(servoNumber,servoRotation)
        ERA.setRotation(1,round(slider1.get()))
        ERA.setRotation(2,round(slider2.get()))
        ERA.setRotation(3,round(slider3.get()))
        ERA.setRotation(4,round(slider4.get()))

        #Also update the window
        window.update_idletasks()
        window.update()
        

    #When the window is closed, disconnect
    ERA.disconnect()


else:
    print("Failed To Connect")

