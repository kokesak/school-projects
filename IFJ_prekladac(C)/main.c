/** Projekt:    IFJ2018
 *              Implementace překladače imperativního jazyka IFJ18   
 * 
 * Tym 012 
 * Clenove:     Michael Kinc (xkincm02)
 *              Martin Litwora (xlitwo00)
 *              Marek Mundl (xmundl00)
 *              Lukas Kadlec (xkadle36)
 * 
 * Hlavni program
 * Autori:      xlitwo00
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#include "scanner.h"
#include "help.h"
#include "errors.h"
#include "precedence.h"
#include "stack.h"
#include "analysis.h"

/* main fce ze ktere se budou volat jednotlive casti */
int main(){
    FILE *f; // = fopen("example3.src", "r");
    /*if (f == NULL)
        return -10;*/
    f = stdin;
    setSourceFile(f);
    Dynamic_array string;
    if(array_init(&string) == false) {
        return ERR_INTERN;
    }
    set_dyn_array(&string);
    int result = 0;
    result = analyser();
    if(result != 0){
        fprintf(stderr, "%d", result);
    }
    return result;

}
