%{
#include <stdio.h>
unsigned int number_of_mikkels = 0;
%}

%option noyywrap

%%
Mikkel       number_of_mikkels++;
.
%%

int main(void) {
    yylex();
    printf("Number of \"Mikkel\"s is %d\n", number_of_mikkels);
    return 0;
}
