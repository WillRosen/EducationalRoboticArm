import bluetooth
import sys
import time
import math

#The socket is what we use to send data to the robotic arm
#It is a global variable so we can access it anywhere in the program
mySocket = None

#This array stores the known rotations of the servos from 0-180 degrees
#Index: 0 - Gripper | 1 - Elbow | 2 - Shoulder | 3 - Base
#They start with rotations -1 degrees as we do not currently know their state 
servoRotations =[-1,-1,-1,-1]


#This will do a bluetooth scan to find nearby devices, and will display
#the name and MAC Addres of them (MAC Address is like a device's ID)
#The MAC address is needed to use the connect(MACAddress) function
def displayBluetoothDevices():
    try:
        #Will retrive a list of nearby bluetooth devices
        nearby_devices = bluetooth.discover_devices(lookup_names=True)

        #Displays this information to the user
        print("Found {} devices.".format(len(nearby_devices)))
        print("    MAC Address \t Name")
        for addr, name in nearby_devices:
            print("  {} - {}".format(addr, name))

    except OSError:
        #In the event of an operating system error (e.g. bluetooth is turned off)
        #we remind the user to check the bluetooth is on
        print("Error: Please make sure your device's Bluetooth is turned on.")




#Attempts to auto-connect to a compatilbe device, which is to say it looks for a
#device with the name "HC-05" then calls the connect(MACAddress) function once found
#This is much slower compared the the connect(MACAddress) function as it has to scan
#the network before attemping to connect
#This returns True if a connection was successful and False if not
def autoConnect():
    print("Attempting Auto Connect...")
    try:
        #Will retrive a list of nearby bluetooth devices
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        
        #Displays this information to the user
        print("Found {} devices.".format(len(nearby_devices)))
        print("    MAC Address \t Name")
        for addr, name in nearby_devices:

            print("  {} - {}".format(addr, name))
            if("HC-05" in name):
                #If we detect a device with the name "HC-05"
                #Attempt to connect using its MACAddress
                print("Found Bluetooth ERA")
                return connect(addr)

                #We return the result of the connection attempt
                #No more code from the autoConnect function is executed
               
        
        #If we have looked at all nearby devices and none of them cause us 
        #to try and connect to them, let the user know we didn't find anything
        print("No Compatible  Devices Found")

    except OSError:
        #In the event of an operating system error (e.g. bluetooth is turned off)
        #we remind the user to check the bluetooth is on
        print("Error: Please make sure your device's Bluetooth is turned on.")

    #Lastly we return false as no connection was made if this line is executed
    return False




#Much faster than the autoConnect as the MACAddress is already known
#This returns True if a connection was successful and False if not 
def connect(MACAddress):
    print("Attempting Connection With {}".format(MACAddress))
    
    #We need to tell python that we are using a global variable called mySocket
    #otherwise when we assign this value it will be a local variable and can not
    #be used outside of this function
    global mySocket
    try:

        #We make a Universally unique identifier or UUID set to the following
        #dont worry about this, its just needed to make a connection
        myUUIDHex = "00001101-0000-1000-8000-00805F9B34FB"
        
        #We find all the results which have the same MACAddress 
        #(Should only be one as MACAddresses are ideally unique) 
        service_matches = bluetooth.find_service(uuid=myUUIDHex, address=MACAddress)

        
        if len(service_matches) == 0:
            #If there are no matches then we have failed to connect, return False
            print("Couldn't find the SampleServer service.")
            return False

        else:
            #If there is more than one match, then connect to the first one (index 0)
            first_match = service_matches[0]

            #Retrieve the port to communicate ont and the host we are communicating with
            port = first_match["port"]
            host = first_match["host"]
            
            #Then set up the socket with the port and host values
            mySocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            mySocket.connect((host, port))

            print("Connection With {} Was Successful".format(MACAddress))
            return True
    except:
        #If there were any unexpected errors along the way
        #Then the connection has failed and we return False
        print("Connection With {} Was Unsuccessful".format(MACAddress))
        return False

#This will send data to the robotic arm, considering the socket has been set up
def sendData(data):
    global mySocket
    if(mySocket!=None):
        #If the socket has been set up then send the data and wait 0.04ms
        #This wait ensures that the robotic arm has had enough time to process 
        #the data before another sendData is called
        print("Sending Data: \t{}".format(data))
        mySocket.send(data)
        time.sleep(0.04)
    else:
        print("No Bluetooth Connection")

#Used for Inverse Kinematics, clamps a value between a min and max value
def clamp(value,minVal,maxVal):
    return max(minVal, min((value), maxVal))

#Used for Inverse Kinematics, gets the magnitude of a 1x3 vector
def getMagnitude(val):
    return math.sqrt((val[0]*val[0])+(val[1]*val[1])+(val[2]*val[2]))

#This is the Inverse Kinematics function which takes in a 3D point in space (X,Y,Z)
#and sets the robotic arm's gripper to be at this position relative to the arm.
def setEulerCoodinates(x,y,z):

    #the targetCood vector stores the XYZ values
    #First make sure none of them are zero as we later divide by them
    #and a division by zero is a big mistake in mathematics
    targetCood=(x,max(0,y),max(0,z))
    if(targetCood[0]==0):
        targetCood=(1,targetCood[1],targetCood[2])
    if(targetCood[1]==0):
        targetCood=(targetCood[0],1,targetCood[2])
    if(targetCood[2]==0):
        targetCood=(targetCood[0],targetCood[1],1)
   
    #Two more values we need are the magnitude of this vector
    #and the squared value of the magnitude of this vector
    targetCoodMag = getMagnitude(targetCood)
    targetCoodMagSquared=targetCoodMag*targetCoodMag

    #The robotic arm's arm length is approximately 100mm,
    #We need this value and the sqaured length of the arm
    ArmLength = 100
    ArmLengthSquared = ArmLength*ArmLength

    #Then using mathematics we calculate the angles
    xz=math.sqrt((targetCood[0]*targetCood[0])+(targetCood[2]*targetCood[2]))
    yRotationOffset = math.degrees(math.atan(targetCood[1]/abs(xz)))
    angle1 =  math.degrees(math.acos(clamp((targetCoodMagSquared)/(2*ArmLength*targetCoodMag),-1,1)))
    rawServoAngle1 = 180-(yRotationOffset+angle1)
    angle2 =  math.degrees(math.acos(clamp((ArmLengthSquared+ArmLengthSquared-targetCoodMagSquared)/(2*ArmLengthSquared),-1,1)))
    rawServoAngle2 = angle2
    baseServoAngle = 90+math.degrees(math.atan(targetCood[0]/targetCood[2]))

    #Lastly we send these values to the robotic arm
    setRotation(4,baseServoAngle)
    setRotation(3,rawServoAngle1)
    setRotation(2,rawServoAngle2)

#This will return the angle the servomotor is currently at
#as long as the servo requested is valid
def getRotation(servo):
     if(servo>0 and servo<5):
         return servoRotations[servo-1]

#The parameter servo is a number and determines which servo to move
#Servo ID: 1 - Gripper | 2 - Elbow | 3 - Shoulder | 4 - Base
#The rotation is between 0 and 180 degrees
#The robotic arm recieves commands in the form of XYYY,
#Where X is the servo number and YYY is between 0 and 180 degrees
def setRotation(servo, rotation):
    #We round it to the nearest whole number as the format XYYY, requires
    #and ensure it is above zero
    rotation = round(rotation)
    rotation=max(0,rotation)

    #We ensure the servo number is valid before we access the array
    #of servo values, this avoids an array index error
    if(servo>0 and servo<5):

        #One optimisation is not to send data if the servo is already
        #in the rotation we have requested
        if(servoRotations[servo-1]==rotation):
            return

        #If all is well, store the new rotation and send the data
        #in the format XYYY,
        servoRotations[servo-1]=rotation
        sendData(str(servo)+str(rotation)+",")

#Closes the gripper 
def closeGripper():
    setRotation(1,180)

#Opens the gripper
def openGripper():
    setRotation(1,0)

#This does the same as setRotation, but also waits until the servo
#has finished moving before the python code continues
#The time which we wait is calculated by the difference in 
#known rotation and requested rotation
def setRotationAndWait(servo,rotation):
    
    timeToWait =0 
    if(servo>0 and servo<5):
        #If we do not the know rotation of the servo, then wait for 
        #the longest time of 0 to 180
        if(servoRotations[servo-1]==-1):
            servoRotations[servo-1]=rotation+180
        
        #the time to wait is calculated by the difference in known rotation
        #and requested rotation, scaled by a value.
        differenceInRotation=abs(servoRotations[servo-1]-rotation)
        timeToWait=differenceInRotation/600

        #Set the rotation of the servo then wait, taking into account the
        #0.04 additional wait time caused by sendData
        setRotation(servo,rotation)
        time.sleep(max(timeToWait-0.04,0))

#This function adds a rotation to a servo, provided the servo is valid
def addRotationToServo(servo,rotation):
    if(servo>0 and servo<5):
        setRotation(servo,max(0, min((servoRotations[servo-1]+rotation), 180)))

#This function adds a rotation to a servo, provided the servo is valid
#but also waits for the servomotor to reach the given rotation before continuing
def addRotationToServoAndWait(servo,rotation):
    if(servo>0 and servo<5):
        setRotationAndWait(servo,max(0, min((servoRotations[servo-1]+rotation), 180)))

#This function closes the connection with the robotic arm, and makes sure the socket is now invalid
def disconnect():
    global mySocket
    mySocket.close()
    mySocket=None
    print("Closed connection")


