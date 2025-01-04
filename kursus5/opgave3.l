%{
#include <stdlib.h> // exit codes
#include <string.h> // strdup
#include "opgave3.tab.h" // Token types form YACC

/* 
 * Helper function that allocates enough heap memory,
 * so that YACC is able to process ASM code without skipping
 * the selected text/token.
 * 
 * If this is not done, then LEX continues to the next input 
 * token, resulting in YACC printing the wrong token. 
 */ 
char *parse_string(const char *text) {
    char *s = strdup(text);
    if (s == NULL) {
        exit(EXIT_FAILURE);
    }
    return s;
}
%}


/* 
 * We only want to read from one file, 
 * so do not wrap multiple input files 
 */
%option noyywrap

varname     [e-h]
number      [0-9]
register    [A-D]

%%
{varname}   { 
    yylval.s = parse_string(yytext);
    return VARNAME; 
}

{number}    { 
    yylval.s = parse_string(yytext);
    return NUMBER; 
}

{register}   {
    yylval.s = parse_string(yytext);
    return REG; 
}

[#;=+]     {
    /* These symbols are small enough to parse as a char 
     * in yytext. Then return them as is
     */
    return *yytext;
}
.   /* Ignore unknown text */
%%
