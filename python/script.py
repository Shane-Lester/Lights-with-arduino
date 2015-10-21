import webiopi
#import datetime
import random
from time import localtime, strftime
import ephem
from datetime import datetime,timedelta
from webiopi.devices.serial import Serial
#from sunset2 import *

SEC30 =timedelta (seconds=30)

home=ephem.Observer()
home.lat='54.520'
home.long='-1.5503'
home.elevation=40

sun=ephem.Sun()


def suntime():
    
    sun.compute(home)

    nextrise = home.next_rising(sun)
    nextset = home.next_setting(sun)

    nextriseutc= nextrise.datetime() + SEC30
    nextsetutc= nextset.datetime() + SEC30


    hour= int((nextsetutc.strftime("%H")))
    minute =int((nextsetutc.strftime("%M")))


    risehour= int((nextriseutc.strftime("%H")))
    riseminute =int((nextriseutc.strftime("%M")))

    return (hour,minute,risehour,riseminute)

#HOUR_ON,MIN_ON=17,30#Turn Light ON at 17:15 (so can't be negative
HOUR_OFF,MIN_OFF = 23,45# Turn Light OFF at 23:00
HOUR_ON,MIN_ON,MORN_OFF,MORNMIN_OFF=suntime()#use sunset times
BASE_ON=MIN_ON
BASE_OFF=MIN_OFF
MORN_ON,MORNMIN_ON=6,30
MORN_OFF,MORNMIN_OFF=7,0
AUTOMAN = "AUTO"
hall,lounge,upstairs=0,0,0
rand=1
morning=0
serial=Serial("/dev/ttyACM0",9600)
active =0
webiopi.sleep(2)

if (rand):

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
numberLights=3 #how many lights are plugged in
# setup function is automatically called at WebIOPi startup
def setup():
    global active, numberLights,morning, rand, MIN_ON,MIN_OFF, BASE_ON,BASE_OFF
    global MORN_ON, MORNMIN_OFF, AUTOMAN
    
   
    # retrieve current datetime
    now = datetime.now()
   

    # test if we are between ON time and tun the light ON
    switch_on=compare_time(now,HOUR_ON,MIN_ON,HOUR_OFF,MIN_OFF)
    if (switch_on):
            webiopi.debug("going on at setup")
            active=1# unique situation- only 1 if should be active at setup
            #serial.writeString("A")
            #serial.writeString("B")
            #serial.writeString("C")
    else:
        webiopi.debug("off at setup")

       
# loop function is repeatedly called by WebIOPi 
def loop():
    global active, numberLights,morning, rand, MIN_ON,MIN_OFF, BASE_ON,BASE_OFF
    global MORN_ON, MORNMIN_OFF, AUTOMAN
    
    # retrieve current datetime
    now = datetime.now()

  
    if (serial.available()>0):
        data=serial.readString()
        webiopi.debug("I've just read %s"%(data))
        lines=data.split("\r\n")
        webiopi.debug("lines is %s"%(lines))
        count=len(lines)
        lines=lines[0:count-1]#last line will be empty so remove it
        for info in lines:
            webiopi.debug("data is %s"%(info))
            room(info)
            
        
    
    if (active==1):
        webiopi.sleep(0.5)
        allOn(numberLights)#if active at time of initiation light em up
        webiopi.debug("setup says on!")
        #light(1,3)
        active=2 #stop it repeating
    elif (active==0):
        webiopi.sleep(0.5)
        allOff(numberLights)
        webiopi.debug("setup says off!")
        lightoff(1,3)
        active=2#stop repeating
    
    if ((morning) and (now.hour==MORN_ON) and (now.minute==MORNMIN_ON) and (now.second==0)):
            webiopi.debug("morning")
            allOn(numberLights)

    if ((now.hour==MORN_OFF) and (now.minute==MORNMIN_OFF) and (now.second<3)):
            #always switch off in the morning
            allOff(numberLights)
            #lightoff(1,3)


      #at 1 am randomise the time if rand button ticked- check time first
    if ((now.hour==1) and (now.minute==0) and (now.second==0)):
        if (rand):
            newhour,BASE_ON,newrisehour,BASEOFF=suntime()

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

        else:
            HOUR_ON,MIN_ON,MORN_OFF,MORNMIN_OFF=suntime()            
            
        
        
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
        
    webiopi.debug("lounge %d hall %d upstairs %d"%(lounge,hall,upstairs))
    # gives CPU some time before looping again
    webiopi.sleep(1.0)
    

# destroy function is called at WebIOPi shutdown
def destroy():
    #GPIO.digitalWrite(LIGHT, GPIO.LOW)
    return



def room(incoming):
    global hall,lounge,upstairs
    webiopi.debug("Room ")
    webiopi.debug(incoming)
    if (incoming=='a'):
        lounge=0
        return
    elif (incoming=='b'):
        hall=0
        return
    elif (incoming=='c'):
        upstairs=0
        return
    elif(incoming=='A'):
        lounge=1
        return
    elif(incoming=='B'):
        hall=1
        return
    elif(incoming=='C'):
        upstairs=1
        return
    

def compare_time(now,start_hour,start_min,stop_hour,stop_min):
    on=datetime.now().replace(hour=start_hour,minute=start_min).time()
    off=datetime.now().replace(hour=stop_hour,minute=stop_min).time()
    if (on<=now.time()<off):
        return True
    else:
        return False

@webiopi.macro
def sendLounge():
    global lounge
    webiopi.debug("lounge %s"%(str(lounge)))
    return lounge

@webiopi.macro
def sendHall():
    global hall
    webiopi.debug("hall %s"%(str(hall)))
    return hall

@webiopi.macro
def sendUpstairs():
    global upstairs
    webiopi.debug("upstairs %d"%(upstairs))
    return upstairs

@webiopi.macro
def update():
    global morning,rand,AUTOMAN,hall,lounge

    webiopi.debug( "%d:%d:%s:%s:%s"%(morning,rand,AUTOMAN,hall,lounge))
    return "%d:%d:%s:%s:%s"%(morning,rand,AUTOMAN,hall,lounge)

@webiopi.macro
def light(num1,num2):
    global lounge
    global hall
    global upstairs
    if (int(num1)==1):
        if (int(num2)==1):
            serial.writeString("A")
            lounge=1
            webiopi.debug("lounge is now on and %d"%(lounge))
            webiopi.sleep(0.1)
        if (int(num2)==2):
            serial.writeString("B")
            hall=1
            webiopi.sleep(0.1)
        if (int(num2)==3):
            serial.writeString("C")
            upstairs=1
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
    global lounge
    global hall
    global upstairs
    if (int(num1)==1):
        if (int(num2)==1):
            serial.writeString("a")
            lounge=0
            webiopi.sleep(0.1)
        if (int(num2)==2):
            serial.writeString("b")
            hall=0
            webiopi.sleep(0.1)
        if (int(num2)==3):
            serial.writeString("c")
            upstairs=0
            webiopi.sleep(0.1)
    return

@webiopi.macro
def toggleRandom():
    global rand
    if (rand):
        rand=0
    else:
        rand=1
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
    webiopi.debug("AUTOMAN")
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
    #global AUTOMAN
    seq= int(number)
    for f in range(seq):
        light(1,f+1)
        webiopi.sleep(0.1)
        #light(1,f+1)
    return

@webiopi.macro
def allOff(number):
    seq= int(number)
    for f in range(seq):           
        lightoff(1,f+1)
        webiopi.sleep(0.1)
        #lightoff(1,f+1)
        
    return
