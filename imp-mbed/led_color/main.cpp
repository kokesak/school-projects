/*
* Autor: Martin Litwora (xlitwo00)
* Date:  21.11.2019
* Project: User comunicate with Mbed using terminal commands
*/

#include "mbed.h"


Serial pc(USBTX, USBRX); // tx, rx

DigitalOut r(LED1);
DigitalOut g(LED2);
DigitalOut b(LED3);


int main() {
    r = 1.0;
    g = 1.0;
    b = 1.0;
     
    
    pc.printf("Press 'r' for red, 'g' for green, 'b' for blue, 'x' for no light and 'w' for white \n");

    while(1) {
        if(pc.readable()){
            char c = pc.getc();
            if(c == 'r') {
                g = 1.0;
                b = 1.0;
                r = 0.0;
            }
            if(c == 'g') {
                g = 0.0;
                b = 1.0;
                r = 1.0;
            }
            if(c == 'b') {
                g = 1.0;
                b = 0.0;
                r = 1.0;
            }
            if(c == 'x') {
                g = 1.0;
                b = 1.0;
                r = 1.0;
            }
            if(c == 'w') {
                g = 0.0;
                b = 0.0;
                r = 0.0;
            }
        }
    }
}