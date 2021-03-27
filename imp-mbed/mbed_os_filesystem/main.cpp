/*
* Autor: Martin Litwora (xlitwo00)
* Date:  21.11.2019
* Project: Simulating LittleFileSystem on Mbed
*/

#include "mbed.h"
#include <stdio.h>
#include <errno.h>
#include <string.h>


// HeapBlockDevice with size of 65536 bytes, read size 1, write size 1 and erase size 512.
#include "HeapBlockDevice.h"
BlockDevice *bd = new HeapBlockDevice(65536, 1, 1, 512);


// This example uses LittleFileSystem as the default file system
#include "LittleFileSystem.h"
LittleFileSystem fs("fs");

// Uncomment the following two lines and comment the previous two to use FAT file system.
//#include "FATFileSystem.h"
//FATFileSystem fs("fs");


Serial pc(USBTX, USBRX);

int main() {

    // Try to mount the filesystem
    printf("Mounting the filesystem... ");
    fflush(stdout);
    int err = fs.mount(bd);
    printf("%s\n", (err ? "Fail :(" : "OK"));
    if (err) {
        // Reformat if we can't mount the filesystem
        printf("No filesystem found, formatting... ");
        fflush(stdout);
        err = fs.reformat(bd);
        printf("%s\n", (err ? "Fail :(" : "OK"));
        if (err) {
            error("error: %s (%d)\n", strerror(-err), err);
        }
    }
    int cont = 1;
    while(cont == 1){
        // Display the root directory
        printf("Opening the root directory... ");
        DIR *d = opendir("/fs/");
        printf("%s\n", (!d ? "Fail :(" : "OK"));
        if (!d) {
            error("error: %s (%d)\n", strerror(errno), -errno);
        }
        printf("root directory:\n");
        while (true) {
            struct dirent *e = readdir(d);
            if (!e) {
                break;
            }
            printf("    %s\n", e->d_name);
        }        
        fflush(stdout);
        err = closedir(d);
        char z;
        pc.printf("Enter name of the file \n");
        char buff[40];
        buff[0] = '\0';
        z = pc.getc();
        while(z != 0x0D){
            pc.putc(z);
            strncat(buff, &z,1);
            z = pc.getc();
        }
        fflush(stdout);
        char file_name[45];
        strcpy(file_name, "/fs/");
        strcat(file_name, buff);
        pc.printf("\nYour name of the file: %s \n", file_name);
        fflush(stdout);
        pc.printf("What do you want to do with the file? \n");
        pc.printf("Press 'r' to read the file \n");
        pc.printf("Press 'w' to write to the file \n");
        pc.printf("Press 'd' to write to the file \n");
        char mode = pc.getc();
        FILE *f;
        switch(mode){
            case 'w':
                f = fopen(file_name, "a+");
                pc.printf("Type your string ending with newline \n");
                while(1){
                    z = pc.getc();
                    while(z != 0x0D){
                        pc.putc(z);
                        fputc(z,f);
                        z = pc.getc();
                    }
                    fputc('\n',f);
                    fflush(stdout);
                    pc.printf("\nDo you want to add another line? y/n \n");
                    if(pc.getc() == 'n'){
                        pc.printf("n\n");
                        break;
                    }
                    else{
                        pc.printf("y\nType:\n");
                    }
                }
                fclose(f);
                break;
            case 'r':
                f = fopen(file_name, "r+");
                if (!f) {
                    printf("No file found");
                    fflush(stdout);
                    error("error: %s (%d)\n", strerror(errno), -errno);
                }
                pc.printf("\nFile content:\n");
                int c = fgetc(f);
                while (c != EOF) {
                    pc.printf("%c", c);
                    c = fgetc(f);
                }
                fflush(stdout);
                fclose(f);
                break;
            case 'd':
                if (remove(file_name) == 0) 
                    pc.printf("Deleted successfully"); 
                else
                    pc.printf("Unable to delete the file");
                break; 
            default:
                error("error: %s (%d)\n", strerror(errno), -errno);
                break;
    
        }
        pc.printf("\nDo you want to repeat? y/n \n");
        char znak = pc.getc();
        switch(znak){
            case 'y':
                cont = 1;
                break;
            case 'n':
                cont = 0;
                break;
            default:
                error("error: %s (%d)\n", strerror(errno), -errno);
                break;
                       
        }

    }
     
    // Clean up
    printf("Unmounting... ");
    fflush(stdout);
    err = fs.unmount();
    printf("%s\n", (err < 0 ? "Fail :(" : "OK"));
    if (err < 0) {
        error("error: %s (%d)\n", strerror(-err), err);
    }
        
    printf("Mbed OS filesystem example done!\n");
}

