%{
#include <stdio.h>
#include "tokens.h"
#include <stdlib.h>

/* Define our Terminals */
enum Terminal {
    IF,
    OPEN_PARENTHESIS,
    CLOSED_PARENTHESIS,
    OPEN_CURLY_BRACKETS,
    CLOSED_CURLY_BRACKETS,
    SEMICOLON,
    NEWLINE,
    EOFI /* Used as return when yylex() has noting more to
          * read, so that we can return from our program */
};

/* Define our Non-Terminal */ 
void PROG(void);
void ST_LIST(void);
void ST(void);

%}

%option noyywrap
%option yylineno

%%
"if"      return IF;
"("       return OPEN_PARENTHESIS;
")"       return CLOSED_PARENTHESIS;
"{"       return OPEN_CURLY_BRACKETS;
"}"       return CLOSED_CURLY_BRACKETS;
";"       return SEMICOLON;
"\n"      return NEWLINE;
<<EOF>>   return EOFI;
.       /* Ignore any other chars */
%%

void match(enum Terminal expected_token) {
    enum Terminal current_token = yylex();
    if (expected_token != current_token) {
        printf("Error at line %d\n", yylineno);
        printf("Expected \"%s\". Got \"%s\"\n", token_str[expected_token], token_str[current_token]);
        exit(EXIT_FAILURE);
    }
}

int main(void) {
    PROG();
    printf("SUCCESS!\n");
    return EXIT_SUCCESS;
}

void PROG(void) {
    printf("PROG ⟶ ST_LIST\n");
    ST_LIST();
}

void ST_LIST(void) {
    printf("ST_LIST ⟶ ST \\n ST_LIST | ε\n");

    if (yylex() == IF) {
        ST();
        match(NEWLINE);
        ST_LIST();
    } 
}

void ST(void) {
    printf("ST ⟶ ST if() { \\n ST_LIST \\n};\n");

    match(OPEN_PARENTHESIS);
    match(CLOSED_PARENTHESIS);
    match(OPEN_CURLY_BRACKETS);
    match(NEWLINE);
    ST_LIST();
    match(NEWLINE);
    match(CLOSED_CURLY_BRACKETS);
    match(SEMICOLON);
}