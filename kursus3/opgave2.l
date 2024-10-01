%{
#include <stdio.h>
#include <string.h>

#define MAX_STRING_SIZE 1024
#define MAX_TABLE_SIZE 1024

char table[MAX_TABLE_SIZE][MAX_STRING_SIZE] = {0};

void addstring(char* s) {
    for (int i = 0; i < MAX_TABLE_SIZE; i++) {
        // Skip if the string is already in the table
        if (strcmp(s, table[i]) == 0) {
            return;
        }

        // Otherwise add the string to the table,
        // (in an empty cell)
        if (strlen(table[i]) == 0) {
            strcpy(table[i], s);
            return;
        }
    }
}
%}

%option noyywrap

VARIABLE [a-zA-Z][a-zA-Z0-9]*
NUMBER [0-9]+
KEYWORD begin|end
ONE_CHAR [\(\);]

%%
{KEYWORD}       addstring(yytext);
{ONE_CHAR}      addstring(yytext);
{VARIABLE}      addstring(yytext);
{NUMBER}        addstring(yytext);
.*
%%

int main(void) {
    yylex();

    // print each string in the table
    for (int i = 0; i < MAX_TABLE_SIZE; i++) {
        if (strlen(table[i]) == 0) {
            break;
        }
        printf("%s\n", table[i]);
    }
    return 0;
}
