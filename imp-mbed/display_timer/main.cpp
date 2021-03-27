/*
* Autor: Martin Litwora (xlitwo00)
* Date:  20.11.2019
* Project: Printing out timer into display
*         A
*       ****
*    F *    * B
*      *  G *
*       ****
*    E *    * C
*      *  D *
*       ****
*
*          |      |      |      |      |      |      |
*   ---------------------------------------------------------
*   |      O      O      O      O      O      O      O      |
*   |      E   4.d       G      F      :      A      B      |
*   |                                                       |
*   |                                                       |
*   |          ld/3.d  ud/2.d   C       D       1.d         |
*   |            O      O       O       O       O           |
*   ---------------------------------------------------------
*                |      |       |       |       |     
*/

#include "mbed.h"

#define MAX_VAL          9999

#define CHAR_TURN_OFF    1
#define DIGIT_TURN_OFF   0

#define CHAR_TURN_ON     0
#define DIGIT_TURN_ON    1

#define TURN_OFF_A       0x1
#define TURN_OFF_B       0x2
#define TURN_OFF_C       0x4
#define TURN_OFF_D       0x8
#define TURN_OFF_E       0x10
#define TURN_OFF_F       0x20
#define TURN_OFF_G       0x40

// B base
DigitalOut digit_4(PTB0);
DigitalOut G_char(PTB1);
DigitalOut F_char(PTB2);
DigitalOut Dot_l(PTB3);

// C base
DigitalOut A_char(PTC2);
DigitalOut B_char(PTC1);

// D base
DigitalOut digit_3_LD(PTE20); // digit 3 or lower dot
DigitalOut digit_2_UD(PTE21); // digit 2 or upper dot
DigitalOut C_char(PTE22);
DigitalOut D_char(PTE23);
DigitalOut digit_1(PTE29);
DigitalOut E_char(PTE30);

uint16_t sec = 0;
void callback( void ){
    sec++;
}



inline void pinClear( void ){
    digit_4     = DIGIT_TURN_OFF;
    G_char      = CHAR_TURN_OFF;
    F_char      = CHAR_TURN_OFF;
    Dot_l       = CHAR_TURN_OFF;
    A_char      = CHAR_TURN_OFF;
    B_char      = CHAR_TURN_OFF;
    digit_3_LD  = DIGIT_TURN_OFF;
    digit_2_UD  = DIGIT_TURN_OFF;
    C_char      = CHAR_TURN_OFF;
    D_char      = CHAR_TURN_OFF;
    digit_1     = DIGIT_TURN_OFF;
    E_char      = CHAR_TURN_OFF;
}

inline void print_digit_numb( uint8_t digit, uint8_t numb){
    if(digit > 4)
        digit = 4;
    else if(digit == 0)
        digit = 1;
        
    uint8_t char_mask  = 0xff;  // XGFE DCBA
    uint8_t digit_mask = 0x1 << (digit-1);
 
    switch( numb ){
        case 0:
            char_mask = 0 | TURN_OFF_G;   
            break;
        case 1:
            char_mask = 0 | ~(TURN_OFF_B | TURN_OFF_C);
            break;
        case 2:
            char_mask = 0 | (TURN_OFF_C | TURN_OFF_F);  
            break;
        case 3:
            char_mask = 0 | (TURN_OFF_E | TURN_OFF_F);
            break;
        case 4: 
            char_mask = 0 | (TURN_OFF_A | TURN_OFF_D | TURN_OFF_E);   
            break;
        case 5:
            char_mask = 0 | (TURN_OFF_B | TURN_OFF_E);
            break;
        case 6:
            char_mask = 0 | (TURN_OFF_B);
            break;
        case 7:
            char_mask = 0 | (TURN_OFF_D | TURN_OFF_E | TURN_OFF_F | TURN_OFF_G);
            break;
        case 8:
            char_mask = 0x0;
            break;
        case 9:
            char_mask = 0 | (TURN_OFF_D | TURN_OFF_E);
            break;
    }
    pinClear();
    digit_1 = digit_mask & 0x1;
    digit_2_UD = digit_mask & 0x2;
    digit_3_LD = digit_mask & 0x4;
    digit_4 = digit_mask & 0x8;
    
    A_char  =  char_mask & 0x1;
    B_char  =  char_mask & 0x2;
    C_char  =  char_mask & 0x4;
    D_char  =  char_mask & 0x8;
    E_char  =  char_mask & 0x10;
    F_char  =  char_mask & 0x20;
    G_char  =  char_mask & 0x40;
}

void print_numb( int number ){
    if(number > MAX_VAL)
        number = MAX_VAL;
    
    if(!number)
        print_digit_numb( 1, 0 );
    
    int pos = 1;
    while(number > 0){
        print_digit_numb( pos++, (number % 10) );
        number /= 10;    
        wait(0.001);
    }
}

int main(){
    pinClear();
    Ticker tick;    
    tick.attach(&callback, 1.0);
    
    while(1){
        print_numb(sec);
    }
}