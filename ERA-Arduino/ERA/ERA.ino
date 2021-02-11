//#include <AltSoftSerial.h>
#include <Servo.h>



Servo servo1;

Servo servo2;

Servo servo3;

Servo servo4;

String Command;


HardwareSerial  bluetooth(PA10, PA9); // RX | TX



void setup()
{
  servo1.attach(D12);
  servo2.attach(D11);
  servo3.attach(D10);
  servo4.attach(D9);
  //  servo.attach(PB4);
  Serial.begin(9600);

  bluetooth.begin(9600);
  bluetooth.println("Hello World");

  Serial.println("The bluetooth gates are open.\n Connect to HC-05 from any other bluetooth device with 1234 as pairing key!.");

}


void loop() {
  char c;

  if (Serial.available()) {
    c = Serial.read();
    bluetooth.print(c);
  }

  while (bluetooth.available())
  {
    // get new byte
    char inChar = (char)bluetooth.read();
    if (inChar == ',') {
      char ID = Command.charAt(0);
      Command.remove(0, 1);
     if(ID=='1'){
      servo1.write(Command.toInt());
     }else if(ID=='2'){
      servo2.write(Command.toInt());
      }else if(ID=='3'){
      servo3.write(Command.toInt());
      }else if(ID=='4'){
      servo4.write(Command.toInt());
      }
      Command = "";
    } else {
      Command += inChar;
      delay(4);
    }

  }

}
