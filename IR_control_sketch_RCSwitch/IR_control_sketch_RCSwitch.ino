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
  Serial.println("IR Receiver Raw Data + Button Decode Test");
  irrecv.enableIRIn(); // Start the receiver
  mySwitch.enableTransmit(10);//RC switch setup

}/*--(end setup )---*/


void loop()   /*----( LOOP: RUNS CONSTANTLY )----*/
{
  if (irrecv.decode(&results)) // have we received an IR signal?

  {
//    Serial.println(results.value, HEX);  UN Comment to see raw values
    translateIR(); 
    irrecv.resume(); // receive the next value
  }  
  
}/* --(end main loop )-- */

/*-----( Declare User-written Functions )-----*/
void translateIR() // takes action based on IR code received

// describing Car MP3 IR codes 

{

  switch(results.value)

  {

  case 0xFFA25D:  
    Serial.println(" POWER            ");
    mySwitch.switchOff(1, 1);
    mySwitch.switchOff(1,2);
    break;

  case 0xFF629D:  
    Serial.println(" MODE             "); 
    break;

  case 0xFFE21D:  
    Serial.println(" MUTE            "); 
    break;

  case 0xFF22DD:  
    Serial.println(" PLAY/PAUSE        "); 
    break;

  case 0xFF02FD:  
    Serial.println(" REWIND           "); 
    break;

  case 0xFFC23D:  
    Serial.println(" FORWIND     "); 
    break;

  case 0xFFE01F:  
    Serial.println(" EQ           "); 
    break;

  case 0xFFA857:  
    Serial.println(" -           "); 
    break;

  case 0xFF906F:  
    Serial.println(" +             "); 
    break;

  case 0xFF6897:  
    Serial.println(" 0              ");
    mySwitch.switchOn(1, 1); 
    mySwitch.switchOn(1,2);
    break;


  case 0xFF30CF:  
    Serial.print(" 1            ");
    break;

  case 0xFF18E7:  
    Serial.println(" 2              "); 
    break;

  case 0xFF7A85:  
    Serial.println(" 3              "); 
    break;

  case 0xFF10EF:  
    Serial.println(" 4              "); 
    break;

  case 0xFF38C7:  
    Serial.println(" 5              "); 
    break;

  case 0xFF5AA5:  
    Serial.println(" 6              "); 
    break;

  case 0xFF42BD:  
    Serial.println(" 7              "); 
    break;

  case 0xFF4AB5:  
    Serial.println(" 8              "); 
    break;

  case 0xFF52AD:  
    Serial.println(" 9              "); 
    break;
    
  case 0xFF9867:
    Serial.println(" Switch        ");
    break;
  
  case 0xFFB04F:
    Serial.println(" U/SD         ");
    break;

  default: 
    Serial.println(" other button   ");

  }

  delay(500);


} //END translateIR



/* ( THE END ) */

