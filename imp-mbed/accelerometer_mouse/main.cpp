/*
* Autor: Martin Litwora (xlitwo00)
* Date:  20.11.2019
* Project: Simulating mouse device using accelerometer
*/

#include "mbed.h"
#include "MMA8451Q.h"
#include "USBMouse.h"
#include "TSISensor.h"

#if   defined (TARGET_KL25Z) || defined (TARGET_KL46Z)
  PinName const SDA = PTE25;
  PinName const SCL = PTE24;
#elif defined (TARGET_KL05Z)
  PinName const SDA = PTB4;
  PinName const SCL = PTB3;
#elif defined (TARGET_K20D50M)
  PinName const SDA = PTB1;
  PinName const SCL = PTB0;
#else
  #error TARGET NOT DEFINED
#endif

#define MMA8451_I2C_ADDRESS (0x1d<<1)

USBMouse mouse;
TSISensor tsi;

int main(void)
{
    MMA8451Q acc(SDA, SCL, MMA8451_I2C_ADDRESS);
    PwmOut rled(LED1);
    PwmOut gled(LED2);
    PwmOut bled(LED3);

    printf("MMA8451 ID: %d\n", acc.getWhoAmI());

    while (true) {
        float x, y, z;
        x = acc.getAccX();
        y = acc.getAccY();
        z = acc.getAccZ();
        rled = 1.0f - abs(x);
        gled = 1.0f - abs(y);
        bled = 1.0f - abs(z);
        printf("X: %1.2f, Y: %1.2f, Z: %1.2f\n", x, y, z);
        x = x * 10;
        y = y * 10;
        mouse.move(-y, x);
        
        //left click
        if (tsi.readPercentage() > 0.7)
        {
            mouse.press(MOUSE_LEFT);
        }
        else
        {
            mouse.release(MOUSE_LEFT);
        }
        
        //right click
        if (tsi.readPercentage() < 0.3 && tsi.readPercentage() > 0)
        {
            mouse.press(MOUSE_RIGHT);
        }
        else
        {
            mouse.release(MOUSE_RIGHT);
        }
    }
}