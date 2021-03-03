import turtle
import time
import math
import ERA


import tkinter
from tkinter import *


#This file was used to figure out the Inverse Kinematics
#It uses the turtle library for testing the angles are correct
#

window = tkinter.Tk()
greeting_var = tkinter.StringVar(window)

greeting = tkinter.Label(textvariable=greeting_var)
greeting_var.set("Set Position!")
greeting.pack()
window.title("Educational Robotic Arm")
window.geometry("400x400")

window.update_idletasks()
window.update()

greeting = tkinter.Label(text="X:")
greeting.pack()

slider1 = Scale(window, from_=-180, to=180, length=600,width=25, orient=HORIZONTAL)
slider1.pack()

greeting = tkinter.Label(text="Y:")
greeting.pack()

slider2 = Scale(window, from_=0, to=180, length=600,width=25, orient=HORIZONTAL)
slider2.pack()

greeting = tkinter.Label(text="Z:")
greeting.pack()

slider3 = Scale(window, from_=0, to=180, length=600,width=25, orient=HORIZONTAL)
slider3.pack()


slider1.set(0)
slider2.set(90)
slider3.set(90)

def clamp(value,minVal,maxVal):
    return max(minVal, min((value), maxVal))
def clampACos(value):
    return clamp(value,-1,1)
def getMagnitude(val):
    return math.sqrt((val[0]*val[0])+(val[1]*val[1])+(val[2]*val[2]))



def draw(targetCood):
    if(targetCood[0]==0):
        targetCood=(1,targetCood[1],targetCood[2])
    if(targetCood[1]==0):
        targetCood=(targetCood[0],1,targetCood[2])
    if(targetCood[2]==0):
        targetCood=(targetCood[0],targetCood[1],1)
    targetCoodMag = getMagnitude(targetCood)
    targetCoodMagSquared=targetCoodMag*targetCoodMag

    ArmLength = 100
    ArmLengthSquared = ArmLength*ArmLength

   
    xz=math.sqrt((targetCood[0]*targetCood[0])+(targetCood[2]*targetCood[2]))


    yRotationOffset = math.degrees(math.atan(targetCood[1]/abs(xz)))
    global myTurtle
    global window
    myTurtle.setpos(0,0)
    myTurtle.clear()
   
    
   
 
    myTurtle.color((1,1,1))
    myTurtle.setheading(yRotationOffset)
    myTurtle.forward(targetCoodMag)
    myTurtle.setpos(0,0)
    myTurtle.color((0,0,0))
    angle1 =  math.degrees(math.acos(clampACos((targetCoodMagSquared)/(2*ArmLength*targetCoodMag))))
    #print(angle1)
    
    myTurtle.setheading(yRotationOffset+angle1)
    myTurtle.forward(ArmLength)



    angle2 =  math.degrees(math.acos(clampACos((ArmLengthSquared+ArmLengthSquared-targetCoodMagSquared)/(2*ArmLengthSquared))))
    #print(angle2)
    myTurtle.right(180-angle2)
    myTurtle.forward(ArmLength)
    #time.sleep(0.5)

    myTurtle.penup()
    myTurtle.setpos(-100,-100)

    myTurtle.pendown()
    #if(targetCood[2]>0):
    myTurtle.setheading(math.degrees(math.atan(targetCood[0]/targetCood[2])))
    #else:
     #   myTurtle.setheading(180+math.degrees(math.atan(targetCood[0]/targetCood[2])))
 
    myTurtle.forward(math.sqrt((targetCood[0]*targetCood[0])+(targetCood[2]*targetCood[2])))
    
    #rawServoAngle1 = yRotationOffset+angle1
    #rawServoAngle2 = 180-angle2
    #baseServoAngle = math.degrees(math.atan(targetCood[0]/targetCood[2]))
    
    #slider1Val = round(slider1.get())
    #slider2Val = round(slider2.get())
    #slider3Val = round(slider3.get())

    #ERA.setEulerCoodinates(slider1Val,slider2Val,slider3Val)



    #print("RSA1 :"+str(round(rawServoAngle1))+"   /   RSA12:"+str(round(rawServoAngle2))+"   /   BSA :"+str(round(baseServoAngle+90)))##Final +90 is servo offset

w = turtle.Screen()
w.bgcolor("grey")
w.title("Angle Tester")

myTurtle = turtle.Turtle()
myTurtle.speed(0)


oldVal1 = slider1.get()
oldVal2 = slider2.get()
oldVal3 = slider3.get()

#if(ERA.connect(MACAddress="FC:A8:9A:00:41:82")):
#    while(True):
#        if(oldVal1!=slider1.get() or oldVal2!=slider2.get() or oldVal3!=slider3.get()):
#            draw((slider1.get(),slider2.get(),slider3.get()))
#            oldVal1 = slider1.get()
#            oldVal2 = slider2.get()
#            oldVal3 = slider3.get()
#        window.update_idletasks()
#        window.update()
#    turtle.done()


while(True):
    if(oldVal1!=slider1.get() or oldVal2!=slider2.get() or oldVal3!=slider3.get()):
        draw((slider1.get(),slider2.get(),slider3.get()))
        oldVal1 = slider1.get()
        oldVal2 = slider2.get()
        oldVal3 = slider3.get()
    window.update_idletasks()
    window.update()
turtle.done()