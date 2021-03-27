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


#include <stdio.h>
#include <stdlib.h>

#include "precedence.h"
#include "stack.h"
#include "errors.h"

void SInit(TStack *s){
    s->top = NULL;
}

int push_symbol(TStack *s, PTable_symbol smb){
    TItem *newItem = (TItem *) malloc(sizeof(TItem));
    if (newItem == NULL){
        return ERR_INTERN;
    }
    newItem->next = s->top;
    newItem->symbol = smb;
    s->top = newItem;
    return STACK_OK;
}

void pop_symbol(TStack *s){
    if(s->top != NULL){
        TItem *tmp;
        tmp = s->top;
        s->top = s->top->next;
        free(tmp);
    }
}

/* funkce vrati symbol z vrcholu ne cely item */
PTable_symbol *stack_top(TStack *s){
    return (&s->top->symbol);
}

void free_stack(TStack *s){
    while(s->top != NULL){
        pop_symbol(s);
    }
}

/* vrati nejvyssi terminal */
TItem *get_top_terminal(TStack *s){
    TItem *tmp = s->top;
    while(tmp != NULL && tmp->symbol >= REDUCTION_START){
        tmp = tmp->next;
    }
    if (tmp != NULL)
        return tmp;
    else 
        return NULL;
}

/* provede operaci shift do zasobniku */
int shift_terminal(TStack *s, PTable_symbol smb){
    TItem *tmp = s->top;
    
    /* prvni symbol na stacku je terminal */
    if(tmp->symbol < REDUCTION_START){
        if (push_symbol(s, REDUCTION_START) == STACK_OK)
            if(push_symbol(s, smb) == STACK_OK)
                return STACK_OK;
        
        return ERR_INTERN; 
    }
    /* hledam prvek za kterym je non terminal */
    while((tmp->next != NULL) && (tmp->next->symbol >= REDUCTION_START)){
        tmp = tmp->next;
    }
    if(tmp->next == NULL)
        return ERR_SYNTAX;
    
    TItem *newItem = (TItem *) malloc(sizeof(TItem));
    if (newItem == NULL){
        return ERR_INTERN;
    }
    newItem->next = tmp->next;
    newItem->symbol = REDUCTION_START;  // vlozim symbol redukce
    tmp->next = newItem;
    if(push_symbol(s, smb) == STACK_OK)
        return STACK_OK;
    else 
        return ERR_INTERN;
    
    
}
