/** Projekt:    IFJ2018
 *              Implementace překladače imperativního jazyka IFJ18   
 * 
 * Tym 012 
 * Clenove:     Michael Kinc (xkincm02)
 *              Martin Litwora (xlitwo00)
 *              Marek Mundl (xmundl00)
 *              Lukas Kadlec (xkadle36)
 * 
 * Pomocny zasobnik pro PSA
 * Autori:      xlitwo00
 */


#ifndef _STACK_H
#define _STACK_H

#include <stdio.h>
#include <stdlib.h>

#define ERR_STACK -1
#define STACK_OK 0

/* symboly pro zasobnik */
typedef enum symb{
    MUL,
    DIV,
    PLUS,
    MINUS,
    LESS,
    LESS_EQUAL,
    GREATER,
    GREATER_EQUAL,
    EQUAL,
    NOT_EQUAL,
    LEFT_BRACKET,
    RIGHT_BRACKET,
    IDENTIFIER,
    INTEGER,
    DOUBLE,
    STRING,
    DOLLAR,
    REDUCTION_START,
    NON_TERMINAL
} PTable_symbol;

typedef struct item{
    struct item *next;
    PTable_symbol symbol;  /* SYMBOL */
    /* nejaky datovy typ pro data??? ->nutny pro generator pri redukci pravidel*/
} TItem;

typedef struct stack{
    TItem *top;
}TStack;

void SInit(TStack *s);

int push_symbol(TStack *s, PTable_symbol smb);

void pop_symbol(TStack *s);

PTable_symbol *stack_top(TStack *s);

void free_stack(TStack *s);

TItem *get_top_terminal(TStack *s);

int shift_terminal(TStack *s, PTable_symbol smb);

#endif