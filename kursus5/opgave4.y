%{
#include <stdlib.h> // Exit codes
#include <stdio.h> // fprintf

/* External function implemented by LEX. */
extern int yylex(void);

/* 
 * Used to redirect our ASM code to a file,
 * instead of using the terminal.
 */
extern FILE *yyout;

/* We must define and implement our own yyerror function. */
void yyerror(const char*);
%}

/* 
 * Tell YACC what kind of data yylval can store 
 * For our example, C-like strings are the only things
 * that yylval can store.
 */ 
%union {
    char *s;
};

/* 
 * Every token is a C string.
 * This includes numbers also, 
 * because the resulting ASM code is only text. 
 */
%token <s> VARNAME 
%token <s> NUMBER 
%token <s> REG 

%% 

program: 
    statement ';' program
    | /* epsilon */
    ;

statement: 
    normal_assignment
    | register_assignment
    ;

normal_assignment:
    VARNAME '=' NUMBER {
        /* Print the ASM code including comments. */
        fprintf(yyout, "; %s = %s\n", $1, $3);
        fprintf(yyout, "MOV [%s], %s\n", $1, $3);
        
        /* Remember to free. */
        free($1);
        free($3);
    }
    ;

register_assignment:
    '#' REG VARNAME '=' VARNAME '+' VARNAME {
        /* Print the ASM code including comments. */
        fprintf(yyout, "; %s = %s + %s\n", $3, $5, $7);
        fprintf(yyout, "MOV %s, [%s]\n", $2, $5);
        fprintf(yyout, "ADD %s, [%s]\n", $2, $7);
        fprintf(yyout, "MOV [%s], %s\n", $3, $2);
        
        /* 
         * As our tokens are allocated using strdup, 
         * remember to free them.
         */
        free($3);
        free($5);
        free($7);
        free($2);
    }
    /* Perhaps implement subtraction here?... */
    ;

%% 

/* Our own small implementation of yyerror. */ 
void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main(void) {

    /* Write the ASM code to a file. */
    yyout = fopen("schweigi_ASM.s", "w");
    if (yyout == NULL)
        return EXIT_FAILURE;

    /* Run and check if LEX is successful. */
    if (yyparse())
        return EXIT_FAILURE;

    /* Print DBs for all varnames. */
    fprintf(yyout, "HLT\n\n");
    fprintf(yyout, "; Variables\n");
    fprintf(yyout, "e: DB 0\n");
    fprintf(yyout, "f: DB 0\n");
    fprintf(yyout, "g: DB 0\n");
    fprintf(yyout, "h: DB 0\n");

    /* Remember to close our file */ 
    fclose(yyout);
    
    return EXIT_SUCCESS;
}
