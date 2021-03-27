/*
* Autor: Martin Litwora (xlitwo00)
* Date:  21.11.2019
* Project: Interrupt on the pin
*/


#include "mbed.h"
#include <stdbool.h>

 
Ticker flipper;
DigitalOut led1(LED3);
InterruptIn pin(PTA12);
TSISensor tsi;
bool blink = false;
 
void flip() {
    blink = !blink;
}

DigitalOut x(PTA1);
DigitalIn y(PTA12);
 
int main() {
    led1 = 1.0;
    pin.fall(&flip);
    x = 1.0;
    while(1){
        //led1 = 0.0;
        wait(0.2);
        if(blink){
            led1 = 0.0;
        }else{
            led1 = 1.0;
        }
        printf("x has value : %d \n\r", x.read());
        printf("y has value : %d \n\r", y.read());
    }  
}