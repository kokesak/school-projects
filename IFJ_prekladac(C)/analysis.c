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

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

#include "analysis.h"
#include "errors.h"
#include "scanner.h"
//#include "symtable.c"
#include "precedence.h"
//#include "stack.h"

#define RULE_OK 0

/*bool init_AData (AData *d) {
    //htInit(&data->global_symtable);
    
    return true;
}*/
bool is_operand(TToken *t){
    if(t->token_id == TOKEN_MUL)
        return true;
    else if(t->token_id == TOKEN_DIV)
        return true;
    else if(t->token_id == TOKEN_PLUS)
        return true;
    else if(t->token_id == TOKEN_MINUS)
        return true;
    else if(t->token_id == TOKEN_LESS)
        return true;
    else if(t->token_id == TOKEN_LESS_EQUAL)
        return true;
    else if(t->token_id == TOKEN_GREATER)
        return true;
    else if(t->token_id == TOKEN_GREATER_EQUAL)
        return true;
    else if(t->token_id == TOKEN_EQUAL)
        return true;
    else if(t->token_id == TOKEN_NOT_EQUAL)
        return true;
    else
        return false;
}

int prog (AData *data) {
    int result;
    // PRAVIDLO 1: <prog> -> def id ( <param> ) eol <statement> end <prog>
    if (data->token.token_id == TOKEN_TYPE_KEYWORD && data->token.attribute.keyword == KEYWORD_DEF) {
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        if (data->token.token_id != TOKEN_IDENTIFIER) {
            return ERR_SYNTAX;
        }
        /*tData sym_data;
        sym_data.is_defined = true;
        sym_data.is_variable = false;
        sym_data.is_func = true;*/
        /*if (copy_string(data->token.attribute.array, data->id) == false) {
            return ERR_INTERN;
        }*/
        //htInsert(&data->global_symtable, data->token.attribute.array,sym_data); // symbol vložený do tabulky si budeme muset uložt někam do pomocné proměnné
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        if(data->token.token_id != TOKEN_LEFT_BRACKET) {
            return ERR_SYNTAX;
        }
        if((result = param(data)) != RULE_OK) {
            return result;
        }
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        if (data->token.token_id != TOKEN_EOL) {
            return ERR_SYNTAX;
        }
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        if((result = statement(data)) != RULE_OK) {
            return result;
        }
        if (data->token.token_id != TOKEN_TYPE_KEYWORD || data->token.attribute.keyword != KEYWORD_END) {
            return ERR_SYNTAX;
        }
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        return prog(data);

    }

    // PRAVIDLO 2: <prog> -> eol <prog>
    else if (data->token.token_id == TOKEN_EOL) {
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        return prog(data);

    }

    // PRAVIDLO 3: <prog> -> <body>
    else if ((data->token.token_id == TOKEN_TYPE_KEYWORD && data->token.attribute.keyword == KEYWORD_IF) ||
             (data->token.token_id == TOKEN_TYPE_KEYWORD && data->token.attribute.keyword == KEYWORD_WHILE) ||
             (data->token.token_id == TOKEN_IDENTIFIER) ||
             (data->token.token_id == TOKEN_TYPE_KEYWORD && data->token.attribute.keyword == KEYWORD_PRINT)){
                if((result = body(data)) != RULE_OK) {
                    return result;
                }
                return prog(data);
        }
    else if((data->token.token_id == TOKEN_EOF)){
        if ((result = end(data)) != RULE_OK) {
            return result;
        }
        return RULE_OK;
    }
    return ERR_SYNTAX;
}

int param (AData *data) {
    int result;
    if ((result = get_token(&data->token)) != SCANNER_OK) {
        return result;
    }

    //PRAVIDLO 6: <param> -> id <param_>
    if(data->token.token_id == TOKEN_IDENTIFIER) {
        /*tData sym_data;
        sym_data.is_defined = true;
        sym_data.is_variable = true;
        sym_data.is_func = false;
        htInsert(&data->global_symtable, data->id, sym_data); //musíme udělat funkci insertParam ????
        //TODO*/
        if ((result = param_n(data)) != RULE_OK) {
            return result;
        }
        return RULE_OK;
    }

    //PRAVIDLO 7: <param> -> eps
    else if (data->token.token_id == TOKEN_RIGHT_BRACKET) {
        return RULE_OK;
    }
    return ERR_SYNTAX;

}

int param_n (AData *data) {
    int result;
    if ((result = get_token(&data->token)) != SCANNER_OK) {
        return result;
    }

    // PRAVIDLO 8: <param_n> -> , id <param_n>
    if (data->token.token_id == TOKEN_COMMA) {
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        if (data->token.token_id == TOKEN_IDENTIFIER ||
            (data->token.token_id == TOKEN_INT) ||
            (data->token.token_id == TOKEN_DOUBLE) ||
            (data->token.token_id == TOKEN_STRING)) {
            
            return param_n(data);
            
            
        }
        else 
            return ERR_LEX;
        /*tData sym_data;
        sym_data.is_defined = true;
        sym_data.is_variable = true;
        sym_data.is_func = false;
        //htInsert(&data->global_symtable, data->id, sym_data); //musíme udělat funkci insertParam ????
        //TODO*/

    }

    // PRAVIDLO 9: <param_n> -> eps
    else if (data->token.token_id == TOKEN_RIGHT_BRACKET) {
        return RULE_OK;
    }
    return ERR_SYNTAX;
}

int body (AData *data) {
    int result;
    // PRAVIDLO 4: <body> -> <statement> <end>
    if ((data->token.token_id == TOKEN_TYPE_KEYWORD && data->token.attribute.keyword == KEYWORD_IF) ||
        (data->token.token_id == TOKEN_TYPE_KEYWORD && data->token.attribute.keyword == KEYWORD_WHILE) ||
        (data->token.token_id == TOKEN_IDENTIFIER) || (data->token.token_id == TOKEN_EOL) ||
        (data->token.token_id == TOKEN_TYPE_KEYWORD && data->token.attribute.keyword == KEYWORD_PRINT)) {
        if ((result = statement(data)) != RULE_OK) {
            return result;
        }
        return RULE_OK;
        /*if ((result = end(data)) != RULE_OK) {
            return result;
        }
        return RULE_OK;*/
    }
    else if((data->token.token_id == TOKEN_EOF) ){
        return RULE_OK;
    }
    return ERR_SYNTAX;

}

int end (AData *data) {

    // PRAVDLO 5: <end> -> eof
    if (data->token.token_id == TOKEN_EOF) {
        return RULE_OK;
    }
    else {
        return ERR_SYNTAX;
    }
}

int statement (AData *data) {
    int result;

    // PRAVIDLO 10: <statement> -> if <expression> then eol <statement> else eol <statement> end eol <statement>
    if (data->token.token_id == TOKEN_TYPE_KEYWORD && data->token.attribute.keyword == KEYWORD_IF) {
        // ted tady podle toho pravidla mám volat <expression> --> vyřešit
        //TODO
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        if ((result = expression(data, NULL)) != EXPRESSION_OK) {
            return result;
        }
        if ((data->token.token_id != TOKEN_TYPE_KEYWORD) || (data->token.attribute.keyword != KEYWORD_THEN)) {
            return ERR_SYNTAX;
        }
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        if (data->token.token_id != TOKEN_EOL) {
            return ERR_SYNTAX;
        }
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        if ((result = statement(data)) != RULE_OK) {
            return result;
        }
        if ((data->token.token_id != TOKEN_TYPE_KEYWORD) || (data->token.attribute.keyword != KEYWORD_ELSE)) {
            return ERR_SYNTAX;
        }
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        if (data->token.token_id != TOKEN_EOL) {
            return ERR_SYNTAX;
        }
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        if ((result = statement(data)) != RULE_OK) {
            return result;
        }
        if ((data->token.token_id != TOKEN_TYPE_KEYWORD) || (data->token.attribute.keyword != KEYWORD_END)) {
            return ERR_SYNTAX;
        }
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        if ((data->token.token_id != TOKEN_EOL) && (data->token.token_id != TOKEN_EOF)) {
            return ERR_SYNTAX;
        }
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        return statement(data);
    }

    // PRAVIDLO 11: <statement> -> while <expression> do eol <statement> end eol <statement>
    else if (data->token.token_id == TOKEN_TYPE_KEYWORD && data->token.attribute.keyword == KEYWORD_WHILE) {
        // ted tady podle toho pravidla mám volat <expression> --> vyřešit
        //TODO
        
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        if ((result = expression (data, NULL)) != EXPRESSION_OK) {
            return result;
        }
        if ((data->token.token_id != TOKEN_TYPE_KEYWORD) || (data->token.attribute.keyword != KEYWORD_DO)) {
            return ERR_SYNTAX;
        }
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        if (data->token.token_id != TOKEN_EOL) {
            return ERR_SYNTAX;
        }
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        
        if ((result = statement(data)) != RULE_OK) {
            return result;
        }

        /*if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }*/
        if ((data->token.token_id != TOKEN_TYPE_KEYWORD) || (data->token.attribute.keyword != KEYWORD_END)) {
            return ERR_SYNTAX;
        }
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        if ((data->token.token_id != TOKEN_EOL) && (data->token.token_id != TOKEN_EOF)) {
            return ERR_SYNTAX;
        }
        /* nutne nacist dalsi token ne? */
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }

        return statement(data);
    }

    // PRAVIDLO 12: <statement> -> id <assignment> eol <statement>
    // PRAVIDLO 13: <statement> -> <expression> eol <statement>

    /* bud je to value, nebo leva zavorka -> potom to je urcite expression */
    else if(data->token.token_id == TOKEN_INT || data->token.token_id == TOKEN_DOUBLE 
            || data->token.token_id == TOKEN_STRING || data->token.token_id == TOKEN_LEFT_BRACKET){
        if ((result = expression(data, NULL)) != EXPRESSION_OK) {
            return result;
        }
        if (data->token.token_id != TOKEN_EOL) {
            return ERR_SYNTAX;
        }
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        return statement(data);
    }
    /* nwm co bude dal -> budu si ukladat token */
    else if (data->token.token_id == TOKEN_IDENTIFIER) {
        /* TO DO tady se muzu zeptat zda li se nejedna o jednu z vestavenych fci */
        AData tmp = *data;
        //AData *tmp = &ahoj; /* nema bejt amprsant?? */

        /*
         * id = funkce 
         * id = id   -- kdyz nenajdu v SYMTABLU tak je automaticky fce?? jo protoze jinak by se to muselo nejspis predelat jinak 
         * funkce       
         * (id*id2)  -- expression
         * id*id     -- expression
         */
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        /* nacetl sem assign, ulozeny token bude L-hodnota, nemuze tedy byt veden jako fce ale jako promenna */
        if(data->token.token_id == TOKEN_ASSIGN) {
            /* kontrola zda tmp neni v tabulce symbolu veden jako fce, popripade ho nastavit jako promenna */
            data->left_side = tmp.token;
            if ((result = get_token(&data->token)) != SCANNER_OK) {
                return result;
            }
            /* jestli to je cislo nebo left bracket -> urcite je to expression */
            if(data->token.token_id == TOKEN_INT || data->token.token_id == TOKEN_DOUBLE 
                || data->token.token_id == TOKEN_STRING || data->token.token_id == TOKEN_LEFT_BRACKET){
                if ((result = expression(data, NULL)) != EXPRESSION_OK) {
                    return result;
                }
                if (data->token.token_id != TOKEN_EOL) {
                    return ERR_SYNTAX;
                }
                if ((result = get_token(&data->token)) != SCANNER_OK) {
                    return result;
                }
                return statement(data);
                }
            else if(data->token.token_id == TOKEN_IDENTIFIER || data->token.token_id == TOKEN_TYPE_KEYWORD){
                tmp = *data;

                if ((result = get_token(&data->token)) != SCANNER_OK) {
                    return result;
                }

                /* musim rozhodnout jestli je to express or argument fce, ulozim si soucasny token a podivam se dal */
                if(is_operand(&data->token) == true){
                    if ((result = expression(data, &tmp)) != EXPRESSION_OK) {
                        return result;
                    }
                    if (data->token.token_id != TOKEN_EOL) {
                        return ERR_SYNTAX;
                    }
                    if ((result = get_token(&data->token)) != SCANNER_OK) {
                        return result;
                    }
                    return statement(data);
                }
                /* pokud neprojde nikam tak to budu brat jako parametry fce */
                /* tmp bude teda potreba nastavit jako fce */
                else{

                    if ((result = func_call(data, &tmp)) != RULE_OK) {
                        return result;
                    }
                    /* co tady dale?? jakoze bude eol a zase statement? || nemuze byt EOF? */ 
                    if(data->token.token_id != TOKEN_EOL){
                    return ERR_SYNTAX;
                    }
                    if ((result = get_token(&data->token)) != SCANNER_OK) {
                        return result;
                    }
                    return statement(data);
                }

            }
        }
        /* dalsi token je operand -> expression */
        // PRAVIDLO 13: <statement> -> <expression> eol <statement>  
        else if(is_operand(&data->token) == true){
            if ((result = expression(data, &tmp)) != EXPRESSION_OK) {
                return result;
            }
            if (data->token.token_id != TOKEN_EOL) {
                return ERR_SYNTAX;
            }
            if ((result = get_token(&data->token)) != SCANNER_OK) {
                return result;
            }
            return statement(data);
        }
        /* pokud neprojde nikam tak to budu brat jako parametry fce */
        /* tmp bude teda potreba nastavit jako fce */
        else{
            if ((result = func_call(data, &tmp)) != RULE_OK) {
                return result;
            }
            /* co tady dale?? jakoze bude eol a zase statement? || nemuze byt EOF? */ 
            if(data->token.token_id != TOKEN_EOL){
                return ERR_SYNTAX;
            }
            return statement(data);
        }

    }

    // PRAVIDLO 14: <statement> -> print <parametres> eol <statement>
    else if (data->token.attribute.keyword == KEYWORD_PRINT) {
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }

        if ((result = parameters(data)) != RULE_OK) {
            return result;
        }
        
        /*if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }*/

        if (data->token.token_id != TOKEN_EOL) {
            return ERR_SYNTAX;
        }
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        return statement(data);
        
    }

    // PRAVIDLO 15: <statement> -> eps
    else if ((data->token.token_id == TOKEN_TYPE_KEYWORD && data->token.attribute.keyword == KEYWORD_END) ||
             (data->token.token_id == TOKEN_EOF) ||
             (data->token.token_id == TOKEN_TYPE_KEYWORD && data->token.attribute.keyword == KEYWORD_ELSE)) {
        return RULE_OK;
    }
    else if(data->token.token_id == TOKEN_EOL){
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        return statement(data);
    }
    else if((data->token.token_id == TOKEN_TYPE_KEYWORD) && (data->token.attribute.keyword == KEYWORD_DEF)){
        return RULE_OK;
    }
    return ERR_SYNTAX;
}

int parameters (AData *data) {
    int result;
    //PRAVIDLO 28: <parameters> -> ( <arg> )
    if (data->token.token_id == TOKEN_LEFT_BRACKET) {
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        if ((result = arg(data)) != RULE_OK) {
            return result;
        }
        return RULE_OK;
    }

    //PRAVIDLO 29: <parameters> -> <arg>
    else if ((data->token.token_id == TOKEN_IDENTIFIER) ||
        (data->token.token_id == TOKEN_EOL) ||
        ((data->token.token_id == TOKEN_TYPE_KEYWORD) && (data->token.attribute.keyword == KEYWORD_END)) ||
        (data->token.token_id == TOKEN_EOF) ||
        ((data->token.token_id == TOKEN_TYPE_KEYWORD) && (data->token.attribute.keyword == KEYWORD_ELSE)) ||
        (data->token.token_id == TOKEN_INT) ||
        (data->token.token_id == TOKEN_DOUBLE) ||
        (data->token.token_id == TOKEN_STRING)){
        if ((result = arg(data)) != RULE_OK) {
            return result;
        }
        return RULE_OK;
    }
    else {
        return ERR_SYNTAX;
    }
}

int arg (AData *data) {
    int result;
    // PRAVIDLO 30: <arg> -> <value> <arg_n>
    if ((data->token.token_id == TOKEN_IDENTIFIER) ||
        (data->token.token_id == TOKEN_INT) ||
        (data->token.token_id == TOKEN_DOUBLE) ||
        (data->token.token_id == TOKEN_STRING)) {
        if ((result = value(data)) != RULE_OK) {
            return result;
        }
        if ((result = arg_n(data)) != RULE_OK) {
            return result;
        }
        return RULE_OK;
    }
    // PRAVIDLO 31: <arg> -> eps
     /* tohle bylo v podmince */
    /*((data->token.token_id == TOKEN_TYPE_KEYWORD) && (data->token.attribute.keyword == KEYWORD_END)) ||
             ((data->token.token_id == TOKEN_TYPE_KEYWORD) && (data->token.attribute.keyword == KEYWORD_ELSE)
    */
    else if ((data->token.token_id == TOKEN_RIGHT_BRACKET) ){
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }         
        return RULE_OK;
    }
    else if((data->token.token_id == TOKEN_EOL) || (data->token.token_id == TOKEN_EOF)){
        return RULE_OK;
    }
    else {
        return ERR_SYNTAX;
    }
}

int value (AData *data) {
    //uplne si nejsem jistej, proc my tady to value máme, ale pravdepodobne proto, abychom rozlišili ten typ toho parametru funkce, ale má se to provádět tady?

    // PRAVIDLO 34: <value> -> double
    if (data->token.token_id == TOKEN_DOUBLE) {
        return RULE_OK;
    }

    // PRAVIDLO 35: <value> -> integer
    else if (data->token.token_id == TOKEN_INT) {
        return RULE_OK;
    }

    // PRAVIDLO 36: <value> -> string
    else if (data->token.token_id == TOKEN_STRING) {
        return RULE_OK;
    }
    // PRAVIDLO 37: <value> -> id
    else if (data->token.token_id == TOKEN_IDENTIFIER) {
        return RULE_OK;
    }
    else {
        return ERR_SYNTAX;
    }
}

int arg_n (AData *data) {
    int result;
    if ((result = get_token(&data->token)) != SCANNER_OK) {
        return result;
    }
    // PRAVIDLO 32: <arg_n> -> , id <arg_n>
    if (data->token.token_id == TOKEN_COMMA) {
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        if (data->token.token_id == TOKEN_IDENTIFIER ||
            (data->token.token_id == TOKEN_INT) ||
            (data->token.token_id == TOKEN_DOUBLE) ||
            (data->token.token_id == TOKEN_STRING)) {
            //asi nějaky ukladani do symtablu?
            //TODO

            return arg_n(data);
        }
        else
            return ERR_SYNTAX;
    }

    // PRAVIDLO 31: <arg_n> -> eps
    else if ((data->token.token_id == TOKEN_RIGHT_BRACKET) ||
             ((data->token.token_id == TOKEN_TYPE_KEYWORD) && (data->token.attribute.keyword == KEYWORD_END)) ||
             ((data->token.token_id == TOKEN_TYPE_KEYWORD) && (data->token.attribute.keyword == KEYWORD_ELSE)) ){
        
        if ((result = get_token(&data->token)) != SCANNER_OK) {
            return result;
        }
        return RULE_OK;
    }
    else if(data->token.token_id == TOKEN_EOL || data->token.token_id == TOKEN_EOF){
        return RULE_OK;
    }
    return ERR_SYNTAX;

}

// v data je ulozen prvni parametr, v id je nazev a identifkator 
int func_call (AData *data, AData *id) {
    int result;
    // PRAVIDLO 20: <func_call> -> inputs <parameters>
    // PRAVIDLO 21: <func_call> -> inputi <parameters>
    // PRAVIDLO 22: <func_call> -> inputf <parameters>
    // PRAVIDLO 23: <func_call> -> length <parameters>
    // PRAVIDLO 24: <func_call> -> substr <parameters>
    // PRAVIDLO 25: <func_call> -> ord <parameters>
    // PRAVIDLO 26: <func_call> -> chr <parameters>
    // PRAVIDLO 27: <func_call> -> id <parameters>
    
    /* jedna se o volani konktertni vestavene fce */
    if(id->token.token_id == TOKEN_TYPE_KEYWORD && (id->token.attribute.keyword == KEYWORD_INPUTI || id->token.attribute.keyword == KEYWORD_INPUTS || 
        id->token.attribute.keyword == KEYWORD_INPUTF || id->token.attribute.keyword == KEYWORD_LENGTH || id->token.attribute.keyword == KEYWORD_SUBSTR || 
        id->token.attribute.keyword == KEYWORD_ORD || id->token.attribute.keyword == KEYWORD_CHR)){

            if((result = parameters(data)) != RULE_OK){
                return result;
            }
            return RULE_OK;
        }
    else if(id->token.token_id == TOKEN_IDENTIFIER){
            if((result = parameters(data)) != RULE_OK){
                return result;
            }
            return RULE_OK;
    }
    return ERR_LEX;
}

int analyser () {

    int analyser_result = 0;
    AData data;

    /*if (init_AData(&data) == false) {
        return ERR_INTERN;
    }*/
    analyser_result = get_token(&data.token);
    if (analyser_result == SCANNER_OK) {
        analyser_result = prog(&data);
    }
    return analyser_result;
}