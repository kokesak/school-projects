/** Projekt:    IFJ2018
 *              Implementace překladače imperativního jazyka IFJ18   
 * 
 * Tym 012 
 * Clenove:     Michael Kinc (xkincm02)
 *              Martin Litwora (xlitwo00)
 *              Marek Mundl (xmundl00)
 *              Lukas Kadlec (xkadle36)
 * 
 * Pomocne funkce pro scanner
 * Autori:      xlitwo00, xkincm02
 */



#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#include "help.h"

/* inicializace pole */
bool array_init(Dynamic_array *a){
    a->string = (char *) malloc(DYNAMIC_STRING_LEN);

    if (a->string != NULL) {
        a->actual_length = 0;
        a->string[a->actual_length] = '\0';
        a->alloc_length = DYNAMIC_STRING_LEN;
        return true;
    }
    else {
        return false;
    }
}
/* pridani jednoho znaku do pole */ 
bool add_char_to_array(Dynamic_array *a, char c){
    if(a->actual_length + 1 >= a->alloc_length){
        unsigned int new_size = a->actual_length + DYNAMIC_STRING_LEN;

        a->string = (char *) realloc(a->string, new_size);
        if(a->string == NULL) {
            return false;
        }

        a->alloc_length = new_size;
    }
    a->string[a->actual_length++] = c;
    //a->actual_length++;
    a->string[a->actual_length] = '\0';
    return true;
}

/* prekopiruje obsah jednoho dynamickeho pole do druheho */
bool copy_string (Dynamic_array *src, Dynamic_array *dest) {
    unsigned int newLength = src->actual_length;
    if (newLength >= dest->alloc_length) {
        dest->string = (char *) realloc(dest->string, newLength + 1);
        if (dest->string == NULL) {
            return false;
        }
        dest->alloc_length = newLength + 1;
    }
    strcpy(dest->string, src->string);
    dest->actual_length = newLength;
    return true;
}

void array_reset(Dynamic_array *a){
    free(a->string);

}
