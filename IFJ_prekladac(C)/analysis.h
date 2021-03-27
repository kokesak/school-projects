/** Projekt:    IFJ2018
 *              Implementace překladače imperativního jazyka IFJ18   
 * 
 * Tym 012 
 * Clenove:     Michael Kinc (xkincm02)
 *              Martin Litwora (xlitwo00)
 *              Marek Mundl (xmundl00)
 *              Lukas Kadlec (xkadle36)
 * 
 * Syntakticky analyzator
 * Autori:      xlitwo00, xkincm02
 */


#ifndef _ANALYSIS_H
#define _ANALYSIS_H

#include <stdio.h>
#include <stdlib.h>

#include "scanner.h"
//#include "symtable.h"
#include "help.h"

typedef struct analysData{
    TToken token;
    //tHTable global_symtable;
    TToken id; /* aktualni token, neni nutny?*/
    TToken left_side; /* token do ktereho se prirazuje */
}AData;

int prog (AData *data);

int param (AData *data);

int statement (AData *data);

int body (AData *data);

int end (AData *data);

int param_n (AData *data);

int assignment (AData *data);

int parameters (AData *data);

int right_side (AData *data);

int func_call (AData *data, AData *id);

int arg (AData *data);

int value (AData *data);

int arg_n (AData *data);

int analyser();

#endif