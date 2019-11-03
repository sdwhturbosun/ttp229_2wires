from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

SCL = 19
SDO = 13
touch = 0 # variable for storing pressed pad number
edge_detect = None # variable for detecting press

# GPIO pin modes
GPIO.setup(SCL, GPIO.OUT)
GPIO.setup(SDO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(SCL, GPIO.HIGH) # Has to be HIGH 

def interrupt():
  global touch
  touch = 0

  sleep(0.000005) # 5us

  for i in range(16):
    GPIO.output(SCL, GPIO.LOW)

    readout = GPIO.input(SDO)
    if not readout: # when you press the pad, readout will be 0
      touch = i+1
      print("{}".format(touch))

    sleep(0.00001) # 10us
    GPIO.output(SCL, GPIO.HIGH)
    sleep(0.00001) # 10us

print("[press ctrl+Z to end the script]")  
try: # Main program loop
  while True:
    edge_detect = GPIO.wait_for_edge(SDO, GPIO.FALLING)
    sleep(0.01) # for stability
    
    if edge_detect is not None:
      interrupt()
      edge_detect = None

# Scavenging work after the end of the program
except KeyboardInterrupt:
  print("Script End!")
  GPIO.cleanup()