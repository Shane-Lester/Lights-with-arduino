/* YourDuino.com Example Software Sketch
 IR Remote Kit Test
 Uses YourDuino.com IR Infrared Remote Control Kit 2
 http://arduino-direct.com/sunshop/index.php?l=product_detail&p=153
 based on code by Ken Shirriff - http://arcfn.com
 Get Library at: https://github.com/shirriff/Arduino-IRremote
 Unzip folder into Libraries. RENAME folder IRremote
 terry@yourduino.com
 Editted 5/2/14 by Shane Lester for Sainsmart remote
 
 Receiver pin 11
 RCSwitch included with transmitter pin 10
 */

/*-----( Import needed libraries )-----*/

#include "IRremote.h"
#include <RCSwitch.h>

RCSwitch mySwitch = RCSwitch();

/*-----( Declare Constants )-----*/
int receiver = 11; // pin 1 of IR receiver to Arduino digital pin 11

/*-----( Declare objects )-----*/
IRrecv irrecv(receiver);           // create instance of 'irrecv'
decode_results results;            // create instance of 'decode_results'
/*-----( Declare Variables )-----*/


void setup()   /*----( SETUP: RUNS ONCE )----*/
{
  Serial.begin(9600);
  //Serial.println("IR Receiver Raw Data + Button Decode Test");
  irrecv.enableIRIn(); // Start the receiver
  mySwitch.enableTransmit(10);//RC switch setup

}/*--(end setup )---*/


void loop()   /*----( LOOP: RUNS CONSTANTLY )----*/
         {
  
  int which=0;// nothing to do
  if (irrecv.decode(&results)) // have we received an IR signal?
       {
    //Serial.println(results.value, HEX);  //UN Comment to see raw values
    which=translateIR(); 
    irrecv.resume(); // receive the next value
  }  
  
  if (Serial.available()){
     char c=Serial.read();
     //Serial.println(c);
     if (islower(c)){
      which=0; 
      switch (c){
        case'a':
         which=1;
         break;
         
        case'b':
         which=2;
         break;
        
        case'c':
         which=4;
         break;
         
        case'o':
         which=7;
         break;
         
        
      }
      
     }
     else if (isupper(c)){
      which=8;
        switch (c){
        case'A':
         which=9;
         break;
         
        case'B':
         which=10;
         break;
        
        case'C':
         which=12;
         break;
         
        case'O':
         which=15;
         break;
     
     }
     }
    
     
  
  }
  
  if (which){// if which isn't zero then there's something to do
      act(which);//call the action loop
      delay(100);
      which=0;
  }
  
}/* --(end main loop )-- */

/*-----( Declare User-written Functions )-----*/

void act(int which){
  //Serial.print(which);
  //Serial.println(" is incoming value");
  if (which >>3){//if bit 4 is set
    // Serial.println("Switching on");
     for (int f=0;f<3;f++){
       if (which & (1<<f)){
           //Serial.print("Switching on ");
           //Serial.println(f+1);
           mySwitch.switchOn(1,f+1);
           Serial.println(char('A'+f));
         }
     }
     which=0;
     return;
  }
  else{
    //Serial.println("switching off");
    for (int f=0;f<3;f++){
         if (which & (1<<f)){
           //Serial.print("Switching off ");
           //Serial.println(f+1);
           mySwitch.switchOff(1,f+1);
           Serial.println(char('a'+f));
           
         }
    }
    which=0;
    return;
    
  }
 which=0;
}
     
     
int translateIR() // takes action based on IR code received

// describing Car MP3 IR codes 

    {

  switch(results.value)

       {

  case 0xFFA25D:  
    //Serial.println(" POWER            ");
    return 3;//2 bits for which lights, fourth bit off

  case 0xFF629D:  
    //Serial.println(" MODE             "); 
    break;

  case 0xFFE21D:  
    //Serial.println(" MUTE            "); 
    break;

  case 0xFF22DD:  
    //Serial.println(" PLAY/PAUSE        "); 
    return 15;// fourth bit for on, 3 bits for which lights 

  case 0xFF02FD:  
    //Serial.println(" REWIND           "); 
    break;

  case 0xFFC23D:  
    //Serial.println(" FORWIND     "); 
    break;

  case 0xFFE01F:  
    //Serial.println(" EQ           "); 
    break;

  case 0xFFA857:  
    //Serial.println(" -           "); 
    break;

  case 0xFF906F:  
    //Serial.println(" +             "); 
    break;

  case 0xFF6897:  
    //Serial.println(" 0              ");
    break;


  case 0xFF30CF:  
    //Serial.print(" 1            ");
    break;

  case 0xFF18E7:  
    //Serial.println(" 2              "); 
    break;

  case 0xFF7A85:  
    //Serial.println(" 3              "); 
    return 4; //third bit for light 3, fourth bit 0 for off

  case 0xFF10EF:  
    //Serial.println(" 4              "); 
    break;

  case 0xFF38C7:  
    //Serial.println(" 5              "); 
    break;

  case 0xFF5AA5:  
    //Serial.println(" 6              "); 
    break;

  case 0xFF42BD:  
    //Serial.println(" 7              "); 
    break;

  case 0xFF4AB5:  
    //Serial.println(" 8              "); 
    break;

  case 0xFF52AD:  
    //Serial.println(" 9              "); 
    break;
    
  case 0xFF9867:
    //Serial.println(" Switch        ");
    break;
  
  case 0xFFB04F:
    //Serial.println(" U/SD         ");
    break;

  default: 
    //Serial.println(" other button   ");
    return 0;
    break;

  }

  delay(500);


} //END translateIR



/* ( THE END ) */

