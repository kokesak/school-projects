/** Projekt:    IFJ2018
 *              Implementace překladače imperativního jazyka IFJ18   
 * 
 * Tym 012 
 * Clenove:     Michael Kinc (xkincm02)
 *              Martin Litwora (xlitwo00)
 *              Marek Mundl (xmundl00)
 *              Lukas Kadlec (xkadle36)
 * 
 * Precedencni syntakticka analyza
 * Autori:      xlitwo00, xkincm02
 */


#ifndef _PRECENDECE_H
#define _PRECEDENCE_H

#include <stdio.h>
#include <stdlib.h>
#include "scanner.h"
#include "analysis.h"
#include "stack.h"

/* vraci 0 pri uspesnem provedeni pravidel */
#define EXPRESSION_OK 0  

/* dekoduje nacteny token */
int token_decode(TToken *t);

/* vrati index posledniho vlozeneho tokenu */
int top_terminal_decode(TStack *s);

/* redukuje podle pravidla */
int rule_reduction(TStack *s);

/* hlavni fce, data2 je pro pripad ze nactu druhy token, ktery je potreba predat */
int expression(AData *data, AData *data2);

#endif