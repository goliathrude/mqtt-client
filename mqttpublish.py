#!/usr/bin/python

### BEGIN INIT INFO
# Provides:          mqttpublish.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

# -*- coding: utf-8 -*-
# Import package
import paho.mqtt.client as mqtt
#add for output
import RPi.GPIO as GPIO


# Define Variables

MQTT_BROKER = "000.000.000.000"       # IP address of your broker
MQTT_PORT = 1883                    # Port of your broker 
MQTT_KEEPALIVE_INTERVAL = 45        # Interval to keep alive
MQTT_TOPIC = "busylight/POWER"      # Topic to use
#

LED1 = 17                           # LED number to trigger on the Raspberry Pi
GPIO.setmode(GPIO.BCM)              # Set the GPIO mode
GPIO.setup(LED1, GPIO.OUT)          # Set 

try:

  # Define on connect event function
  # We shall subscribe to our Topic in this function

  def on_connect(self,mosq, obj, rc):
     mqttc.subscribe(MQTT_TOPIC, 0)
     print("Connect on "+ MQTT_HOST)

  # Define on_message event function. 
  # This function will be invoked every time,
  # a new message arrives for the subscribed topic 

  def on_message(mosq, obj, msg):
     if (msg.payload =='ON'):
           GPIO.output(LED1,True)
           print 'light on'
           print "Topic: " + str(msg.topic)
           print "QoS: " + str(msg.qos)
     if (msg.payload =='OFF'):
           GPIO.output(LED1,False)
           print 'light off'
           print "Topic: " + str(msg.topic)
           print "QoS: " + str(msg.qos)

  def on_subscribe(mosq, obj, mid, granted_qos):
          print("Subscribed to Topic: " + 
          MQTT_TOPIC + " with QoS: " + str(granted_qos))

  # Initiate MQTT Client

  mqttc = mqtt.Client()

    # Assign event callbacks
  mqttc.on_message = on_message
  mqttc.on_connect = on_connect
  mqttc.on_subscribe = on_subscribe

    # Connect with MQTT Broker
  mqttc.username_pw_set("USER",password="PASSWORD")
  mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

    # Continue monitoring the incoming messages for subscribed topic
  mqttc.loop_forever()

except KeyboardInterrupt:  
    # here you put any code you want to run before the program   
    # exits when you press CTRL+C
    GPIO.cleanup()  
#finally:  
    #GPIO.cleanup() # this ensures a clean exit  
