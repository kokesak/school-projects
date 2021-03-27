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



#include <stdio.h>
#include <stdlib.h>
#include <ctype.h> //isspace()
#include <string.h>
#include <stdbool.h>

#include "scanner.h" //hlavičkový soubor lexikálního analyzátoru
#include "errors.h" //chybové stavy

/* stavy automatu */
#define STATE_START 100
#define STATE_GREATER 101
#define STATE_LESS 102
#define STATE_NOT_EQUAL 103
#define STATE_EQUAL_SIGN 104
#define STATE_BEGIN_BLOCK_COMMENT 105
#define STATE_B 106
#define STATE_BE 107
#define STATE_BEG 108
#define STATE_BEGI 109
#define STATE_BLOCK_COMMENT 110
#define STATE_NEW_LINE 111
#define STATE_END_BLOCK_COMMENT 112
#define STATE_E 113
#define STATE_EN 114
#define STATE_LINE_COMMENT 115
#define STATE_NUMBER 116
#define STATE_DOUBLE 117
#define STATE_EXPONENT 118
#define STATE_EXPONENT_SIGN 119
#define STATE_EXPONENT_NUMBER 120
#define STATE_STRING 121
#define STATE_STRING_ESCAPE 122
#define STATE_STRING_BEGIN_ASCII 123
#define STATE_STRING_ASCII 124
#define STATE_IDENTIFIER 125
#define STATE_EOL 126

FILE *source;
Dynamic_array *dyn_array;

/* propojeni souboru z main.c */
void setSourceFile(FILE *f) {

	source = f;
}

/* je tohle nutny mit takhle slozite? */
int check_if_keyword (Dynamic_array *array, TToken *token) {

    if(strcmp(array->string, "def") == 0) {token->attribute.keyword = KEYWORD_DEF; token->token_id = TOKEN_TYPE_KEYWORD; return SCANNER_OK;}
    else if(strcmp(array->string, "do") == 0) {token->attribute.keyword = KEYWORD_DO; token->token_id = TOKEN_TYPE_KEYWORD; return SCANNER_OK;}
    else if(strcmp(array->string, "else") == 0) {token->attribute.keyword = KEYWORD_ELSE; token->token_id = TOKEN_TYPE_KEYWORD; return SCANNER_OK;}
    else if(strcmp(array->string, "end") == 0) {token->attribute.keyword = KEYWORD_END; token->token_id = TOKEN_TYPE_KEYWORD; return SCANNER_OK;}
    else if(strcmp(array->string, "if") == 0) {token->attribute.keyword = KEYWORD_IF; token->token_id = TOKEN_TYPE_KEYWORD; return SCANNER_OK;}
    else if(strcmp(array->string, "not") == 0) {token->attribute.keyword = KEYWORD_NOT; token->token_id = TOKEN_TYPE_KEYWORD; return SCANNER_OK;}
    else if(strcmp(array->string, "nil") == 0) {token->attribute.keyword = KEYWORD_NIL; token->token_id = TOKEN_TYPE_KEYWORD; return SCANNER_OK;}
    else if(strcmp(array->string, "then") == 0) {token->attribute.keyword = KEYWORD_THEN; token->token_id = TOKEN_TYPE_KEYWORD; return SCANNER_OK;}
    else if(strcmp(array->string, "while") == 0) {token->attribute.keyword = KEYWORD_WHILE; token->token_id = TOKEN_TYPE_KEYWORD; return SCANNER_OK;}
    else if(strcmp(array->string, "inputs") == 0) {token->attribute.keyword = KEYWORD_INPUTS; token->token_id = TOKEN_TYPE_KEYWORD; return SCANNER_OK;}
    else if(strcmp(array->string, "inputi") == 0) {token->attribute.keyword = KEYWORD_INPUTI; token->token_id = TOKEN_TYPE_KEYWORD; return SCANNER_OK;}
    else if(strcmp(array->string, "inputf") == 0) {token->attribute.keyword = KEYWORD_INPUTF; token->token_id = TOKEN_TYPE_KEYWORD; return SCANNER_OK;}
    else if(strcmp(array->string, "length") == 0) {token->attribute.keyword = KEYWORD_LENGTH; token->token_id = TOKEN_TYPE_KEYWORD; return SCANNER_OK;}
    else if(strcmp(array->string, "substr") == 0) {token->attribute.keyword = KEYWORD_SUBSTR; token->token_id = TOKEN_TYPE_KEYWORD; return SCANNER_OK;}
    else if(strcmp(array->string, "ord") == 0) {token->attribute.keyword = KEYWORD_ORD; token->token_id = TOKEN_TYPE_KEYWORD; return SCANNER_OK;}
    else if(strcmp(array->string, "chr") == 0) {token->attribute.keyword = KEYWORD_CHR; token->token_id = TOKEN_TYPE_KEYWORD; return SCANNER_OK;}
    else if(strcmp(array->string, "print") == 0) {token->attribute.keyword = KEYWORD_PRINT; token->token_id = TOKEN_TYPE_KEYWORD; return SCANNER_OK;}
    else{
        token->token_id = TOKEN_IDENTIFIER;
    }

    /* kopirovani nactenyho do tokenu, nestaci strcmp? */
    if(copy_string(array, token->attribute.array) == false) {
        array_reset(array);
        return ERR_INTERN;
    }
    array_reset(array);
    return SCANNER_OK;
}

void set_dyn_array (Dynamic_array *string) {
    dyn_array = string;
}

int get_token (TToken *token) {
    if (source == NULL) {
        return ERR_INTERN;
    }

    token->attribute.array = dyn_array;
    Dynamic_array arra;
    Dynamic_array *arr = &arra;
    if(array_init(arr) == false) {
        return ERR_INTERN;
    }
    int state = STATE_START; //inicializace počátečního stavu
    char *endptr, escnum[2];
    while (1) {
        char znak;
        znak = (char) getc(source); // přečtu znak ze souboru
        switch (state) {
            case STATE_START:
                if (znak == ' ' || znak == '\t' || znak == '\v' || znak == '\f' || znak == '\r') {
                    state = STATE_START;
                    break;
                }
                if (znak == '/') {
                    token->token_id = TOKEN_DIV;
                    array_reset(arr);
                    return (SCANNER_OK);
                } else if (znak == '*') {
                    token->token_id = TOKEN_MUL;
                    array_reset(arr);
                    return (SCANNER_OK);
                } else if (znak == '+') {
                    token->token_id = TOKEN_PLUS;
                    array_reset(arr);
                    return (SCANNER_OK);
                } else if (znak == '-') {
                    token->token_id = TOKEN_MINUS;
                    array_reset(arr);
                    return (SCANNER_OK);
                } else if (znak == '>') {
                    state = STATE_GREATER;
                } else if (znak == '<') {
                    state = STATE_LESS;
                } else if (znak == '!') {
                    state = STATE_NOT_EQUAL;
                } else if (znak == '=') {
                    state = STATE_EQUAL_SIGN;
                } else if (znak == '#') {
                    state = STATE_LINE_COMMENT;
                } else if (znak == '(') {
                    token->token_id = TOKEN_LEFT_BRACKET;
                    array_reset(arr);
                    return (SCANNER_OK);
                } else if (znak == ')') {
                    token->token_id = TOKEN_RIGHT_BRACKET;
                    array_reset(arr);
                    return (SCANNER_OK);
                } else if (znak == '\n') {
                    state = STATE_EOL;
                } else if (znak == EOF) {
                    token->token_id = TOKEN_EOF;
                    array_reset(arr);
                    return (SCANNER_OK);
                } else if (znak == ',') {
                    token->token_id = TOKEN_COMMA;
                    array_reset(arr);
                    return (SCANNER_OK);
                } else if (isdigit(znak)) { //na zacatku cisla nemuze byt nula!!, ale muze!
                    if (add_char_to_array(arr, znak) == false) {
                        array_reset(arr);
                        return (ERR_INTERN);
                    }
                    state = STATE_NUMBER;
                }
                else if (znak == '"') {
                    state = STATE_STRING;
                }
                else if (islower(znak) || znak == '_') {
                    if (add_char_to_array(arr, znak) == false) {
                        array_reset(arr);
                        return (ERR_INTERN);
                    }
                    state = STATE_IDENTIFIER;
                } else {
                    array_reset(arr);
                    return ERR_LEX;
                }
                break;

            case STATE_GREATER:
                if (znak == '=') {
                    token->token_id = TOKEN_GREATER_EQUAL;
                } else {
                    ungetc(znak, source);
                    token->token_id = TOKEN_GREATER;
                }
                array_reset(arr);
                return (SCANNER_OK);
                break;

            case STATE_LESS:
                if (znak == '=') {
                    token->token_id = TOKEN_LESS_EQUAL;
                } else {
                    ungetc(znak, source);
                    token->token_id = TOKEN_LESS;
                }
                array_reset(arr);
                return (SCANNER_OK);
                break;

            case STATE_NOT_EQUAL:
                if (znak == '=') {
                    token->token_id = TOKEN_NOT_EQUAL;
                    array_reset(arr);
                    return (SCANNER_OK);
                }
                else {
                    array_reset(arr);
                    return (ERR_LEX);
                }
                break;

            case STATE_EOL:
                if (znak == '=') {
                    state = STATE_BEGIN_BLOCK_COMMENT;
                }
                else if (isspace(znak)) {
                    break;
                }
                else {
                    token->token_id = TOKEN_EOL;
                    ungetc(znak, source);
                    array_reset(arr);
                    return SCANNER_OK;
                }
                break;


            case STATE_EQUAL_SIGN:
                if (znak == '=') {
                    token->token_id = TOKEN_EQUAL;
                    array_reset(arr);
                    return (SCANNER_OK);
                }
                else {
                    token->token_id = TOKEN_ASSIGN;
		            ungetc(znak, source);
                    array_reset(arr);
                    return (SCANNER_OK);
                }
                break;

            case STATE_LINE_COMMENT:
                if (znak == '\n') {
                    token->token_id = TOKEN_EOL;
                    return (SCANNER_OK);
                }
                else if(znak == EOF){
                    token->token_id = TOKEN_EOF;
                    return (SCANNER_OK);
                }
                break;

            case STATE_NUMBER:
                if (isdigit(znak) ) {
                    if (add_char_to_array(arr, znak) == false) {
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                } else if (znak == '.') {
                    if (add_char_to_array(arr, znak) == false) {
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                    state = STATE_DOUBLE;
                } else {
                    ungetc(znak, source);
                    char *ptr;
                    token->attribute.integer_value = (int) strtol(arr->string, &ptr, 10);
                    token->token_id = TOKEN_INT;
                    array_reset(arr);
                    return SCANNER_OK;
                }
                break;

            case STATE_DOUBLE:
                if (isdigit(znak)) {
                    if (add_char_to_array(arr, znak) == false) {
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                    state = STATE_DOUBLE;
                } else if (znak == 'e' || znak == 'E') {
                    if (add_char_to_array(arr, znak) == false) {
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                    state = STATE_EXPONENT;
                } else {
                    ungetc(znak, source);
                    char *ptr;
                    token->attribute.double_value = (double)strtod(arr->string, &ptr);
                    token->token_id = TOKEN_DOUBLE;
                    array_reset(arr);
                    return SCANNER_OK;
                }
                break;

            case STATE_EXPONENT:
                if (isdigit(znak)) {
                    if (add_char_to_array(arr, znak) == false) {
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                    state = STATE_EXPONENT_NUMBER;
                } else if (znak == '+' || znak == '-') {
                    state = STATE_EXPONENT_SIGN;
		            if (add_char_to_array(arr, znak) == false) {
                    	array_reset(arr);
                    	return ERR_INTERN;
                    }
                } else {
                    array_reset(arr);
                    return ERR_LEX;
                }
                break;

            case STATE_EXPONENT_SIGN:
                if (isdigit(znak)) {
                    if (add_char_to_array(arr, znak) == false) {
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                    state = STATE_EXPONENT_NUMBER;
                } else {
                    array_reset(arr);
                    return ERR_LEX;
                }
                break;

            case STATE_EXPONENT_NUMBER:
                if (isdigit(znak)) {
                    if (add_char_to_array(arr, znak) == false) {
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                    state = STATE_EXPONENT_NUMBER;
                }
                else {
                    ungetc(znak, source);
                    if (add_char_to_array(arr, '0') == false) { /* pridam nulu na konec */
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                    char *ptr;
                    token->attribute.double_value = strtod(arr->string, &ptr);
                    token->token_id = TOKEN_DOUBLE;
                    array_reset(arr);
                    return SCANNER_OK;
                }
                break;

            case STATE_STRING:
                if (znak == '\\') {
                    state = STATE_STRING_ESCAPE;
                }
                else if (znak == '"') {
                    if (!(strcpy(token->attribute.array->string, arr->string))) {
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                    token->token_id = TOKEN_STRING;
                    array_reset(arr);
                    return SCANNER_OK;
                }
                else {
                    if (add_char_to_array(arr, znak) == false) {
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                    state = STATE_STRING;
                }
                break;

            case STATE_STRING_ESCAPE:
                if (znak == '"') {
                    znak = '"'; //  \" -> "
                    if (add_char_to_array(arr, znak) == false) {
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                    state = STATE_STRING;
                }
                else if (znak == 'n') {
                    znak = '\n'; // \n -> konec radku
                    if (add_char_to_array(arr, znak) == false) {
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                    state = STATE_STRING;
                }
                else if (znak == 't') {
                    znak = '\t'; //  \t -> tab
                    if (add_char_to_array(arr, znak) == false) {
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                    state = STATE_STRING;
                }
                else if (znak == 's') {
                    znak = ' '; // \s -> mezera
                    if (add_char_to_array(arr, znak) == false) {
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                    state = STATE_STRING;
                }
                else if (znak == '\\') {
                    znak = '\\';
                    if (add_char_to_array(arr, znak) == false) {
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                    state = STATE_STRING;
                }
                else if (znak == 'x') {
                    state = STATE_STRING_BEGIN_ASCII;
                }
                else {
                    array_reset(arr);
                    return ERR_LEX;
                }
                break;

            case STATE_STRING_BEGIN_ASCII:
                if (isdigit(znak) || znak == 'A' || znak == 'B' || znak == 'C' || znak == 'D' || znak == 'E' || znak == 'F') {
                    escnum[0] = znak;
                    state = STATE_STRING_ASCII;
                }
                else {
                    array_reset(arr);
                    return ERR_LEX;
                }
                break;

            case STATE_STRING_ASCII:
                if (isdigit(znak) || znak == 'A' || znak == 'B' || znak == 'C' || znak == 'D' || znak == 'E' || znak == 'F') {
                    escnum[1] = znak;
                    int temp = (int) strtol(escnum, &endptr, 10);
                    if (*endptr) {
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                    znak = (char) temp;
                    if (add_char_to_array(arr, znak) == false) {
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                    state = STATE_STRING;

                }
                else {
                    int temp = (int) strtol(escnum, &endptr, 10);
                    if (*endptr) {
                        return ERR_INTERN;
                    }
                    znak = (char) temp;
                    if (add_char_to_array(arr, znak) == false) {
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                    ungetc(znak, source);
                    state = STATE_STRING;
                }
                break;


            case STATE_IDENTIFIER:
                if (isalnum(znak) || znak == '_') {
                    if (add_char_to_array(arr, znak) == false) {
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                    state = STATE_IDENTIFIER;
                }
                else if(znak == '?' || znak == '!'){
                    if(add_char_to_array(arr, znak) == false){
                        array_reset(arr);
                        return ERR_INTERN;
                    }
                    return check_if_keyword(arr, token);
                }
                else {
                    ungetc(znak, source);
                    return check_if_keyword(arr, token);
                }
                break;

            case STATE_BEGIN_BLOCK_COMMENT:
                if (znak == 'b') {
                    state = STATE_B;
                }
                else {
                    array_reset(arr);
                    return ERR_LEX;
                }
                break;

            case STATE_B:
                if (znak == 'e') {
                    state = STATE_BE;
                } else {
                    array_reset(arr);
                    return ERR_LEX;
                }
                break;

            case STATE_BE:
                if (znak == 'g') {
                    state = STATE_BEG;
                }
                else {
                    array_reset(arr);
                    return ERR_LEX;
                }
                break;

            case STATE_BEG:
                if (znak == 'i') {
                    state = STATE_BEGI;
                }
                else {
                    array_reset(arr);
                    return ERR_LEX;
                }
                break;

            case STATE_BEGI:
                if (znak == 'n') {
                    state = STATE_BLOCK_COMMENT;
                }
                else {
                    array_reset(arr);
                    return ERR_LEX;
                }
                break;

            case STATE_BLOCK_COMMENT:
                if (znak == '\n') {
                    state = STATE_NEW_LINE;
                }
                else {
                    state = STATE_BLOCK_COMMENT;
                }
                break;

            case STATE_NEW_LINE:
                if (znak == '=') {
                    state = STATE_END_BLOCK_COMMENT;
                }
                else {
                    state = STATE_BLOCK_COMMENT;
                }
                break;

            case STATE_END_BLOCK_COMMENT:
                if (znak == 'e') {
                    state = STATE_E;
                }
                else {
                    state = STATE_BLOCK_COMMENT;
                }
                break;

            case STATE_E:
                if (znak == 'n') {
                    state = STATE_EN;
                }
                else {
                    state = STATE_BLOCK_COMMENT;
                }
                break;

            case STATE_EN:
                if (znak == 'd') {
                    state = STATE_START;
                }
                else {
                    state = STATE_BLOCK_COMMENT;
                }
                break;
            default:
                break;
        }

    }
}
