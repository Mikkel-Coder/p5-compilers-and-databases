/*
 * Skriv et lex-program, der læser en fil og udskriver de nedenfor stående 
 * leksikalske enheder
 *
 * variabel:
 *  - (dvs. en streng der starter med et bogstav efterfuldt af bogstaver, tal 
 *     og andre relevante tegn.)
 *
 * tal:
 *  - (dvs en streng af tal.)
 *
 * nogle få keywords 
 *  - (f.eks. begin og end)
 *
 * og enkelt tegn 
 *  - (f.eks. parenteser og semikolon)
 */

%{
#include <stdio.h>
%}

%option noyywrap

VARIABLE [a-zA-Z][a-zA-Z0-9]* 
NUMBER [0-9]+
KEYWORD begin|end
ONE_CHAR [\(\);]

%%
{KEYWORD}       printf("Found a keyword %s", yytext);
{ONE_CHAR}      printf("Found a one char %s", yytext);
{VARIABLE}      printf("Found a variable %s", yytext);
{NUMBER}        printf("Found a number %s", yytext);
.*              printf("Undefined %s", yytext);
%%

int main(void) {
   yylex();
   return 0;
}
