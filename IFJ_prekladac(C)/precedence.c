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

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "scanner.h"
#include "errors.h"
#include "analysis.h"
#include "stack.h"
#include "precedence.h"

#define TABLE_SIZE 14
#define EXPRESSION_OK 0

char prec_table[TABLE_SIZE][TABLE_SIZE] = {

        // |  *  |  /  |  +  |  -  |  <  |  <=  |  >  |  >=  |  ==  |  !=  |  (  |  )  |  i  |  $  |  //        <- terminaly na vstupu(tokeny)
           { '>' , '>' , '>' , '>',  '>' ,  '>' , '>' ,  '>' ,  '>' ,  '>' , '<' , '>' , '<' , '>' }, // *      smerem dolu jsou token na zasobniku
           { '>' , '>' , '>' , '>',  '>' ,  '>' , '>' ,  '>' ,  '>' ,  '>' , '<' , '>' , '<' , '>' }, // /      
           { '<' , '<' , '>' , '>',  '>' ,  '>' , '>' ,  '>' ,  '>' ,  '>' , '<' , '>' , '<' , '>' }, // +
           { '<' , '<' , '>' , '>',  '>' ,  '>' , '>' ,  '>' ,  '>' ,  '>' , '<' , '>' , '<' , '>' }, // -
           { '<' , '<' , '<' , '<',  '0' ,  '0' , '0' ,  '0' ,  '>' ,  '>' , '<' , '>' , '<' , '>' }, // <                                                                                        // -
           { '<' , '<' , '<' , '<',  '0' ,  '0' , '0' ,  '0' ,  '>' ,  '>' , '<' , '>' , '<' , '>' }, // <=                                                                                         // <
           { '<' , '<' , '<' , '<',  '0' ,  '0' , '0' ,  '0' ,  '>' ,  '>' , '<' , '>' , '<' , '>' }, // >                                                                                         // <=
           { '<' , '<' , '<' , '<',  '0' ,  '0' , '0' ,  '0' ,  '>' ,  '>' , '<' , '>' , '<' , '>' }, // >=                                                                                         // >
           { '<' , '<' , '<' , '<',  '<' ,  '<' , '<' ,  '<' ,  '0' ,  '0' , '<' , '>' , '<' , '>' }, // ==
           { '<' , '<' , '<' , '<',  '<' ,  '<' , '<' ,  '<' ,  '0' ,  '0' , '<' , '>' , '<' , '>' }, // !=
           { '<' , '<' , '<' , '<',  '<' ,  '<' , '<' ,  '<' ,  '<' ,  '<' , '<' , '=' , '<' , '>' }, // (
           { '>' , '>' , '>' , '>',  '>' ,  '>' , '>' ,  '>' ,  '>' ,  '>' , '0' , '>' , '0' , '0' }, // )
           { '>' , '>' , '>' , '>',  '>' ,  '>' , '>' ,  '>' ,  '>' ,  '>' , '0' , '>' , '0' , '>' }, // i
           { '<' , '<' , '<' , '<',  '<' ,  '<' , '<' ,  '<' ,  '<' ,  '<' , '<' , '0' , '<' , '0' }, // $
};

/*  funkce dekoduje obsah tokenu a prevede ho na index v tabulce */
int token_decode(TToken *t){
    if(t->token_id == TOKEN_MUL)
        return 0;
    else if(t->token_id == TOKEN_DIV)
        return 1;
    else if(t->token_id == TOKEN_PLUS)
        return 2;
    else if(t->token_id == TOKEN_MINUS)
        return 3;
    else if(t->token_id == TOKEN_LESS)
        return 4;
    else if(t->token_id == TOKEN_LESS_EQUAL)
        return 5;
    else if(t->token_id == TOKEN_GREATER)
        return 6;
    else if(t->token_id == TOKEN_GREATER_EQUAL)
        return 7;
    else if(t->token_id == TOKEN_EQUAL)
        return 8;
    else if(t->token_id == TOKEN_NOT_EQUAL)
        return 9;
    else if(t->token_id == TOKEN_LEFT_BRACKET)
        return 10;
    else if(t->token_id == TOKEN_RIGHT_BRACKET)
        return 11;
    else if(t->token_id == TOKEN_IDENTIFIER || (t->token_id == TOKEN_TYPE_KEYWORD && t->attribute.keyword == KEYWORD_NIL))
        return 12;
    else if(t->token_id == TOKEN_INT)
        return 12;
    else if(t->token_id == TOKEN_DOUBLE)
        return 12;
    else if(t->token_id == TOKEN_STRING)
        return 12;
    else
        return 13;

}

/* funkce zjisti nejposlednejsi terminal na stacku */
int top_terminal_decode(TStack *s){
    TItem *term = get_top_terminal(s);

    if(term->symbol == MUL)
        return 0;
    else if(term->symbol == DIV)
        return 1;
    else if(term->symbol == PLUS)
        return 2;
    else if(term->symbol == MINUS)
        return 3;
    else if (term->symbol == LESS)
        return 4;
    else if(term->symbol == LESS_EQUAL)
        return 5;
    else if(term->symbol == GREATER)
        return 6;
    else if(term->symbol == GREATER_EQUAL)
        return 7;
    else if(term->symbol == EQUAL)
        return 8;
    else if(term->symbol == NOT_EQUAL)
        return 9;
    else if(term->symbol == LEFT_BRACKET)
        return 10;
    else if(term->symbol == RIGHT_BRACKET)
        return 11;
    else if(term->symbol == IDENTIFIER)
        return 12;
    else if(term->symbol == INTEGER)
        return 12;
    else if(term->symbol == DOUBLE)
        return 12;
    else if(term->symbol == STRING)
        return 12;
    else
        return 13;
}

/* funkce provadi redukci pravidla podle poctu NONterminalu na vrcholu zasobniku*/
int rule_reduction(TStack *s){
    //budeme potřebovat v parametrech AData *data pro generator
    TItem *tmp = s->top;

    int number_symbol;
    number_symbol = 0;

    while(((tmp->symbol) != REDUCTION_START)){
        number_symbol++;
        tmp = tmp->next;
    }
    if(tmp == NULL){
        return ERR_SYNTAX;
    }

    if(number_symbol == 1){
        /* E -> i */
        TItem *op1 = s->top; 
        if((op1->symbol != IDENTIFIER) && (op1->symbol != INTEGER) && (op1->symbol != DOUBLE) && (op1->symbol != STRING)){
            return ERR_SYNTAX;
        }


        pop_symbol(s);
        pop_symbol(s);
        push_symbol(s, NON_TERMINAL);
        return EXPRESSION_OK;
    }
    else if(number_symbol == 3){
        TItem *op3 = s->top;                /* operand, ktery byl naposled vlozen */
        TItem *op2 = s->top->next;
        TItem *op1 = s->top->next->next;
       /*
        * E -> E*E
        * E -> E/E
        * E -> E+E
        * E -> E-E
        * E -> E<E
        * E -> E<=E
        * E -> E>E
        * E -> E>=E
        * E -> E==E
        * E -> E!=E
        * E -> (E)
        */

       /* E -> E*E */
       if((op1->symbol == NON_TERMINAL) && op2->symbol == MUL && (op3->symbol == NON_TERMINAL)){
           /* generuj kod pro nasobeni */ 
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           push_symbol(s, NON_TERMINAL);
           return EXPRESSION_OK;
       }
       /* E -> E/E */
       if((op1->symbol == NON_TERMINAL) && op2->symbol == DIV && (op3->symbol == NON_TERMINAL)){
           /* generuj kod pro deleni */ 
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           push_symbol(s, NON_TERMINAL);
           return EXPRESSION_OK;
        }
        /* E -> E+E */
        if((op1->symbol == NON_TERMINAL) && op2->symbol == PLUS && (op3->symbol == NON_TERMINAL)){
           /* generuj kod pro scitani */
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           push_symbol(s, NON_TERMINAL);
           return EXPRESSION_OK;
        }
        /* E -> E-E */
        if((op1->symbol == NON_TERMINAL) && op2->symbol == MINUS && (op3->symbol == NON_TERMINAL)){
           /* generuj kod pro odcitani */ 
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           push_symbol(s, NON_TERMINAL);
           return EXPRESSION_OK;
        }
        /* E -> E<E */
        if((op1->symbol == NON_TERMINAL) && op2->symbol == LESS && (op3->symbol == NON_TERMINAL)){
           /* generuj kod pro operaci mensi */
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           push_symbol(s, NON_TERMINAL);
           return EXPRESSION_OK;
        }
        /* E -> E<=E */
        if((op1->symbol == NON_TERMINAL) && op2->symbol == LESS_EQUAL && (op3->symbol == NON_TERMINAL)){
           /* generuj kod pro operaci mensi rovno */ 
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           push_symbol(s, NON_TERMINAL);
           return EXPRESSION_OK;
        }
        /* E -> E>E */
        if((op1->symbol == NON_TERMINAL) && op2->symbol == GREATER && (op3->symbol == NON_TERMINAL)){
           /* generuj kod pro operaci vetsi */ 
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           push_symbol(s, NON_TERMINAL);
           return EXPRESSION_OK;
        }
        /* E -> E>=E */
        if((op1->symbol == NON_TERMINAL) && op2->symbol == GREATER_EQUAL && (op3->symbol == NON_TERMINAL)){
           /* generuj kod pro operaci vetsi rovno */ 
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           push_symbol(s, NON_TERMINAL);
           return EXPRESSION_OK;
        }
        /* E -> E=E */
        if((op1->symbol == NON_TERMINAL) && op2->symbol == EQUAL && (op3->symbol == NON_TERMINAL)){
           /* generuj kod pro rovnost */ 
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           push_symbol(s, NON_TERMINAL);
           return EXPRESSION_OK;
        }
        /* E -> E!=E */
        if((op1->symbol == NON_TERMINAL) && op2->symbol == NOT_EQUAL && (op3->symbol == NON_TERMINAL)){
           /* generuj kod pro deleni */ 
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           push_symbol(s, NON_TERMINAL);
           return EXPRESSION_OK;
        }
        /* E -> (E) */
        if((op1->symbol == LEFT_BRACKET) && op2->symbol == NON_TERMINAL && (op3->symbol == RIGHT_BRACKET)){
           /* generuj kod pro reducki zavorek */
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           pop_symbol(s);
           push_symbol(s, NON_TERMINAL);
           return EXPRESSION_OK;
        }
    }
    return ERR_SYNTAX;
}

/* druha data slouzi pro specialni pripady kdy predavam druhy token(ten vsak byl nacteny jako prvni) */
int expression(AData *data, AData *data2){
    TStack *stack = malloc(sizeof(TStack));
    SInit(stack);
    if(push_symbol(stack, DOLLAR) == ERR_STACK){
        free_stack(stack);
        return ERR_INTERN;
    }
    int read_token_index;
    int top_terminal_index;
    char sign;
    int result = 0;

    if(data2 != NULL){
        read_token_index = token_decode(&data2->token);
        top_terminal_index = top_terminal_decode(stack);

        sign = prec_table[top_terminal_index][read_token_index];
        if (sign == '<'){
            /* shift to stack */
            if(shift_terminal(stack, read_token_index) == ERR_STACK){
                free_stack(stack);
                return ERR_INTERN;
            }
            
        }
        else if(sign == '>'){
            /* reduction rules */
            if((result = rule_reduction(stack)) != EXPRESSION_OK){
                free_stack(stack);
                return result;
            }

        }
        else if(sign == '='){
            /* eliminace zavorek */
            push_symbol(stack, read_token_index);
        }
        else if(sign == '0'){
            if(read_token_index == 13 && top_terminal_index == 13)
                return EXPRESSION_OK; /* expression ok */
            else{
                free_stack(stack);
                return ERR_SYNTAX;
            }
        }
    }    
    
    while(1){
        read_token_index = token_decode(&data->token);
        top_terminal_index = top_terminal_decode(stack);

        sign = prec_table[top_terminal_index][read_token_index];
        if (sign == '<'){
            /* shift to stack */
            if(shift_terminal(stack, read_token_index) == ERR_STACK){
                free_stack(stack);
                return ERR_INTERN;
            }

            result = get_token(&data->token);
            if(result != SCANNER_OK){
                free_stack(stack);
                return result;
            }
        }
        else if(sign == '>'){
            /* reduction rules */
            if((result = rule_reduction(stack))  != EXPRESSION_OK){
                free_stack(stack);
                return result;
            }

        }
        else if(sign == '='){
            /* eliminace zavorek */
            result = get_token(&data->token);
            if(result != SCANNER_OK){
                free_stack(stack);
                return result;
            }
            if(data->token.token_id == TOKEN_EOL || data->token.token_id == TOKEN_TYPE_KEYWORD){ // pro pripad ze by byl vyraz typu (id operator id)
                push_symbol(stack, read_token_index);
                if((result = rule_reduction(stack))  != EXPRESSION_OK){
                    free_stack(stack);
                    return result;
                }
            }
            else{
                push_symbol(stack, read_token_index);
            }
        }
        else if(sign == '0'){
            if(read_token_index == 13 && top_terminal_index == 13){
                free_stack(stack);
                return EXPRESSION_OK; /* expression ok */
            }
            else{
                free_stack(stack);
                return ERR_SYNTAX;
            }
        }
    }
}
