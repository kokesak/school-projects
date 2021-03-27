/*
 *  Projekt IOS_2 synchronizace procesu - The Senate Bus Problem
 *  Autor: Martin Litwora
 *  Datum: 1.5.2018
 */


// podmineni prekladu
#ifndef _PROJ2_H
#define _PROJ2_H


// knihovny
#include <time.h>           // pro funkci rand, srand
#include <unistd.h>         // funkcefork(), usleep
#include <semaphore.h>      // pro praci se semafory
#include <fcntl.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/stat.h>
#include <signal.h>


// inicializuje a otevre semafory
void set_semaphores();


// vytvori sdilene promenne
void set_shared();


// uzavre semafory a uklidi sdilene promenne
void close_resources();


// vrati nahodne cislo, pro funkci usleep
// int max = maximalni nahodna hodnota
int rand_value(int max);


// funkce pro procesy rider
void rider();


// funkce pro proces bus
void bus();


// funkce pro kontrolu paramtru
// vraci int -1 pri spatnych argumentech, jinak 0
int arguments(int argc, char *argv[]);


// hlavni funkce, tvori se zde procesy bus a rider
int main(int argc, char *argv[]);


#endif
