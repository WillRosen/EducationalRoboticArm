import ERA
import tkinter
from tkinter import *

#This code will allow the user to use the Inverse Kinematic controls 


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
    
    #Make 4 sliders, for XYZ positions and gripper rotation with labels above them
   
    slider1 = Scale(window, from_=-250, to=250, length=600,width=25, orient=HORIZONTAL)
    slider1.pack()
    label1 = Label(text="X Position")
    label1.pack()

    
    slider2 = Scale(window, from_=0, to=250, length=600,width=25, orient=HORIZONTAL)
    slider2.pack()
    label2 = Label(text="Y Position")
    label2.pack()

  
    slider3 = Scale(window, from_=0, to=250, length=600,width=25, orient=HORIZONTAL)
    slider3.pack()
    label3 = Label(text="Z Position")
    label3.pack()
    
    slider4 = Scale(window, from_=0, to=180, length=600,width=25, orient=HORIZONTAL)
    slider4.pack()
    label4 = Label(text="Gripper")
    label4.pack()
    #Set up the sliders with default IK Positions
    slider1.set(0)
    slider2.set(100)
    slider3.set(100)
    slider4.set(100)

    #While the window is running, continuously update the rotation of each servo
    while(True):
        
        #Read the values of each IK Slider
        slider1Val = round(slider1.get())
        slider2Val = round(slider2.get())
        slider3Val = round(slider3.get())

        #Set the coodinates of the robotic arm using these slider values
        ERA.setEulerCoodinates(slider1Val,slider2Val,slider3Val)

        #The last slider is the gripper, so this is set individually
        ERA.setRotation(1,round(slider4.get()))

        #Also update the window
        window.update_idletasks()
        window.update()
        

    #When the window is closed, disconnect
    ERA.disconnect()


else:
    print("Failed To Connect")


