#Importing Dependables 

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

#Define GPIO and set up their modes
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT) #GPIO 11 is connected to the green LED
GPIO.setup(11, GPIO.OUT) #GPIO 12 is connected to the red LED
GPIO.setup(9, GPIO.OUT) #GPIO 13 is connected to the servo motor
GPIO.setup(7, GPIO.OUT) #GPIO 15 is connected to button 1 (the button to turn on the green LED)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("identificacion") #"x/y/z" replace this with your topic name of your choice in the given order.
    
#You can define as many GPIO as you wish to control your switches.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if "green_on" in msg.payload:
        GPIO.output(11, True)
    elif "green_off" in msg.payload:
          GPIO.output(11, False)

#Fucntion calls
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

client.loop_forever() # handles reconnecting.