/** Projekt:    IFJ2018
 *              Implementace překladače imperativního jazyka IFJ18   
 * 
 * Tym 012 
 * Clenove:     Michael Kinc (xkincm02)
 *              Martin Litwora (xlitwo00)
 *              Marek Mundl (xmundl00)
 *              Lukas Kadlec (xkadle36)
 * 
 * Errory
 * Autori:      xkincm02
 */

#ifndef _ERRORS_H_
#define _ERRORS_H_

#define ERR_OK 0 //překlad proběhl bez chyb
#define ERR_LEX 1 // chyba v programu v rámci lexikální analýzy
#define ERR_SYNTAX 2 // chyba v programu v rámci syntaktické analýzy
#define ERR_SEM 3 // chyba v programu v rámci sémantické analýzy
#define ERR_SEM_TYPES 4  //sémantická/běhová chyba typové kompatibility v aritmetických, řetězcových a relačních výrazech
#define ERR_SEM_PARAM 5 //sémantická chyba v programu - špatný počet parametrů u volání funkce
#define ERR_SEM_OTHERS 6 //ostatní sémantické chyby
#define ERR_DIV_ZERO 9 //běhová chyba dělení nulou

#define SCANNER_OK 10 //lexiální analýza proběhla v pořádku

#define ERR_INTERN 99 //interní chyba překladače tj. neovlivnitelná vstupním programem (např. chyba alokace paměti atd.)

#endif //_ERRORS_H