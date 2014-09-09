import webiopi
import datetime
import random
import time
from webiopi.devices.serial import Serial
serial=Serial("/dev/ttyACM0",9600)



HOUR_ON,MIN_ON=19,15#Turn Light ON at 17:15 (so can't be negative
HOUR_OFF,MIN_OFF = 23,30# Turn Light OFF at 23:00
BASE_ON=MIN_ON
BASE_OFF=MIN_OFF
MORN_ON,MORNMIN_ON=6,30
MORN_OFF,MORNMIN_OFF=7,0
AUTOMAN = "AUTO"
rand=True
morning=1
serial=Serial("/dev/ttyACM0",9600)
time.sleep(20)
if (rand==True):

    MIN_ON=BASE_ON+random.randint(-15,15)
    if (MIN_ON<0):
            MIN_ON=0
    if (MIN_ON>59):
            MIN_ON=59
    MIN_OFF=BASE_OFF+random.randint(-15,15)
    if (MIN_OFF<0):
            MIN_OFF=0
    if (MIN_OFF>59):
            MIN_OFF=59

active = 0
numberLights=2 #how many lights are plugged in
# setup function is automatically called at WebIOPi startup
def setup():
    global active
    serial=Serial("/dev/ttyACM0",9600)
   
    # retrieve current datetime
    now = datetime.datetime.now()
   

    # test if we are between ON time and tun the light ON
    if ((now.hour >= HOUR_ON) and (now.hour <= HOUR_OFF)):
        if ((now.minute >= MIN_ON)):
            active=1# unique situation- only 1 if should be active at setup
            serial.writeString("A")
            serial.writeString("B")
            serial.writeString("C")
             

       
# loop function is repeatedly called by WebIOPi 
def loop():
    global active
    global numberLights
    global AUTOMAN
    global MIN_ON
    global MIN_OFF
    global morning
    global rand
    
    # retrieve current datetime
    now = datetime.datetime.now()
    
    if (active==1):
        webiopi.sleep(0.5)
        allOn(numberLights)#if active at time of initiation light em up
        webiopi.debug("setup says on!")
        light(1,3)
        active=2 #stop it repeating
    elif (active==0):
        webiopi.sleep(0.5)
        allOff(numberLights)
        webiopi.debug("setup says off!")
        lightoff(1,3)
        active=2#stop repeating
    
    if ((morning) and (now.hour==MORN_ON) and (now.minute==MORNMIN_ON) and (now.second==0)):
            webiopi.debug(morning)
            allOn(numberLights)

    if ((now.hour==MORN_OFF) and (now.minute==MORNMIN_OFF) and (now.second==0)):
            #always switch off in the morning
            allOff(numberLights)
            lightoff(1,3)


      #at 1 am randomise the time if rand button ticked
    if ((rand==True)and (now.hour==1) and (now.minute==0) and (now.second==0)):
        MIN_ON=BASE_ON + random.randint(-15,15)
        if (MIN_ON<0):
            MIN_ON=0
        if (MIN_ON>59):
            MIN_ON=59
        
        MIN_OFF=BASE_OFF + random.randint(-15,15)
        if (MIN_OFF<0):
            MIN_OFF=0
        if (MIN_OFF>59):
            MIN_OFF=59
        
        
    # toggle light ON all days at the correct time
    if ((now.hour == HOUR_ON) and (now.minute == MIN_ON) and (now.second <=10)) and (AUTOMAN=="AUTO"):
        webiopi.debug("Time to go on")
        allOn(numberLights)
        light(1,3)
        
        
    # toggle light OFF
    if ((now.hour == HOUR_OFF) and (now.minute == MIN_OFF) and (now.second <=10))and (AUTOMAN=="AUTO"):
        webiopi.debug("Time to go off")
        allOff(numberLights)
        lightoff(1,3)
   
    # gives CPU some time before looping again
    webiopi.sleep(1.0)
    

# destroy function is called at WebIOPi shutdown
def destroy():
    #GPIO.digitalWrite(LIGHT, GPIO.LOW)
    return

@webiopi.macro
def update():
    global morning
    global rand
    if (rand==True):
        random=1
    else:
        random=0
    return "%d:%d"%(morning,random)

@webiopi.macro
def light(num1,num2):
    if (int(num1)==1):
        if (int(num2)==1):
            serial.writeString("A")
            webiopi.sleep(0.1)
        if (int(num2)==2):
            serial.writeString("B")
            webiopi.sleep(0.1)
        if (int(num2)==3):
            serial.writeString("C")
            webiopi.sleep(0.1)
    return

@webiopi.macro
def morningLights(ison):
    global morning
    if (ison=="true"):
        morning=1
        return 
    elif (ison=="false"):
        morning=0
        return 


@webiopi.macro
def lightoff(num1,num2):
    if (int(num1)==1):
        if (int(num2)==1):
            serial.writeString("a")
            webiopi.sleep(0.1)
        if (int(num2)==2):
            serial.writeString("b")
            webiopi.sleep(0.1)
        if (int(num2)==3):
            serial.writeString("c")
            webiopi.sleep(0.1)
    return

@webiopi.macro
def toggleRandom():
    global rand
    if (rand):
        rand=False
    else:
        rand=True
    return

@webiopi.macro
def getLightHours():
    global HOUR_ON,MIN_ON,HOUR_OFF,MIN_OFF
    return "%d:%d:%d:%d" % (HOUR_ON,MIN_ON,HOUR_OFF,MIN_OFF)


@webiopi.macro
def setLightHours(hour,minute,hourOff,minuteOff):
    global AUTOMAN
    global HOUR_ON,MIN_ON, HOUR_OFF,MIN_OFF
    
    HOUR_ON=int(hour)
    MIN_ON=int(minute)
    if (MIN_ON>59):
        MIN_ON=59
    if (MIN_ON<0):
        MIN_ON=0
    HOUR_OFF=int(hourOff)
    MIN_OFF=int(minuteOff)
    if (MIN_OFF>59):
        MIN_OFF=59
    if (MIN_OFF<0):
        MIN_OFF=0
    AUTOMAN="AUTO"
    return getLightHours()


@webiopi.macro
def autoManual():
    global AUTOMAN
    if (AUTOMAN=="AUTO"):
        return "AUTO"
    elif(AUTOMAN=="MANUAL"):
        return "MANUAL"
    else:
        webiopi.debug("Error")
        return "AUTO"


@webiopi.macro
def toggleAuto():#data is the js sent mode= auto or manual
    global AUTOMAN
    if (AUTOMAN=="AUTO"):
        AUTOMAN="MANUAL"
        return "MANUAL"
     
    else:
        AUTOMAN="AUTO"
        return "AUTO"

@webiopi.macro
def allOn(number):
    global AUTOMAN
    seq= int(number)
    for f in range(seq):
        light(1,f+1)
        webiopi.sleep(0.1)
        light(1,f+1)
    return

@webiopi.macro
def allOff(number):
    seq= int(number)
    for f in range(seq):           
        lightoff(1,f+1)
        webiopi.sleep(0.1)
        lightoff(1,f+1)
        
    return
