/** Projekt:    IFJ2018
 *              Implementace překladače imperativního jazyka IFJ18   
 * 
 * Tym 012 
 * Clenove:     Michael Kinc (xkincm02)
 *              Martin Litwora (xlitwo00)
 *              Marek Mundl (xmundl00)
 *              Lukas Kadlec (xkadle36)
 * 
 * Lexikalni analyzator (scanner)
 * Autori:      xlitwo00, xkincm02, xmundl00, xkadle36
 */

#ifndef _SCANNER_H
#define _SCANNER_H

#include <stdlib.h>
#include "help.h"

/* TYPY TOKENU */
typedef enum tok{
    TOKEN_DIV, //0
    TOKEN_MUL, //1
    TOKEN_PLUS, //2
    TOKEN_MINUS, //3
    TOKEN_GREATER, //4
    TOKEN_GREATER_EQUAL, //5
    TOKEN_LESS, //6
    TOKEN_LESS_EQUAL, //7
    TOKEN_NOT_EQUAL, //8
    TOKEN_ASSIGN, //9
    TOKEN_EQUAL, //10
    TOKEN_DOUBLE, //11
    TOKEN_INT, //12
    TOKEN_STRING, //13
    TOKEN_IDENTIFIER, //14
    TOKEN_RIGHT_BRACKET, //15
    TOKEN_LEFT_BRACKET, //16
    TOKEN_COMMA, //17
    TOKEN_EOL, //18
    TOKEN_EOF, //19
    TOKEN_TYPE_KEYWORD, //20

}Token_type;

/* KLICOVA SLOVA */
typedef enum{
    KEYWORD_DEF,
    KEYWORD_DO,
    KEYWORD_ELSE,
    KEYWORD_END,
    KEYWORD_IF,
    KEYWORD_NOT,
    KEYWORD_NIL,
    KEYWORD_THEN,
    KEYWORD_WHILE,
    KEYWORD_INPUTS,
    KEYWORD_INPUTI,
    KEYWORD_INPUTF,
    KEYWORD_LENGTH,
    KEYWORD_SUBSTR,
    KEYWORD_ORD,
    KEYWORD_CHR,
    KEYWORD_PRINT,
}Keyword;



/* pouze jeden typ atributu :)*/
typedef union {
    int integer_value;
    double double_value;
    Dynamic_array *array;
    Keyword keyword;
} TAttribute;

typedef struct  {
    Token_type token_id; //typ tokenu
    TAttribute attribute; //obsah tokenu
} TToken;

void setSourceFile(FILE *f);

/* funkce kontroluje jestli neni obsah array klicove slovo */
int check_if_keyword (Dynamic_array *array, TToken *token);

/* pres ukazatel predavame token, funkce vraci errory podle errors.h */ 
int get_token (TToken *token);

/* predani dynamickeho pole z mainu aby se spravne predaval dyn array */
void set_dyn_array (Dynamic_array *string);

#endif //_SCANNER_H
