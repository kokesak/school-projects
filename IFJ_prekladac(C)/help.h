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


#ifndef _HELP_H
#define _HELP_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


typedef struct {
    char *string;                   /* pole znaku */
    unsigned int actual_length;     /* aktualni zaplnenost pole */
    unsigned int alloc_length;      /* alokovana velikost pole */
} Dynamic_array;

#define DYNAMIC_STRING_LEN 10

/* inicializace dynamickeho pole */
bool array_init(Dynamic_array *a);

/* pridani znaku do pole */
bool add_char_to_array(Dynamic_array *a, char c);

/* prekopirovani jednoho dyn. pole do druheho */
bool copy_string (Dynamic_array *src, Dynamic_array *dest);

/* free */
void array_reset(Dynamic_array *a);

#endif