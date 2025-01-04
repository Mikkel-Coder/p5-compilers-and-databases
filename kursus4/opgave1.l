/*
 * Write a recursive descend parser accepting programs/languages from the following grammar:
 *
 * PROG -> ST_LIST
 * ST_LIST -> ST \n ST_LIST
 * ST -> if() { \n ST_LIST \n};
 * 
 * where the upper case "words" denote non-terminal symbols and 
 * "if","(",")","{","}",";""\n" are terminal symbols.
 * Use lex for the lexical scanning/tokenizing.
 *
 *
 * We have the following:
 *
 * N = Non-terminal, T = Terminal, P = Production rules, S = Start Symbol
 * G={N,T,P,S}
 * N = {PROG, ST_LIST, ST}
 * T = {“if”, “(“, “)”, “{“, “}”, ”;”, ”\n”, ε}
 * P = 	PROG → ST_LIST 
 * 	ST_LIST →  ST \n ST_LIST | ε
 * 	ST → if() { \n ST_LIST \n};
 * S = {PROG}
 * 
 * “ “ (the space character) is not include in the alphabet/terminals
 *
 */

%{
#include <stdio.h>  // Used for printf
#include "tokens.h" // Used for error messages
#include <stdlib.h> // Exit codes

/* Define our Terminals */
enum Terminal {
    IF,
    OPEN_PARENTHESIS,
    CLOSED_PARENTHESIS,
    OPEN_CURLY_BRACKETS,
    CLOSED_CURLY_BRACKETS,
    SEMICOLON,
    NEWLINE,
    EOFI /* Used as return indicator when yylex() has noting more 
            to read, so that we can return from our program */
};

/* Define our Non-Terminal */ 
void PROG(void);
void ST_LIST(void);
void ST(void);

%}

%option noyywrap

/* When invalid input print the line number of the error */
%option yylineno


/* Define our production rules*/
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

// Helper function to check if current token matches the expected token
void match(enum Terminal const expected_token) {
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

/* The following functions are the non-terminals in our language */

// Start non-terminal symbol function
void PROG(void) {
    printf("PROG ⟶ ST_LIST\n");
    ST_LIST();
}

void ST_LIST(void) {
    printf("ST_LIST ⟶ ST \\n ST_LIST | ε\n");

    // Is the new terminal an IF statement?
    if (yylex() == IF) {
        ST();
        match(NEWLINE);
        ST_LIST();
    } 
}

void ST(void) {
    printf("ST ⟶ ST if() { \\n ST_LIST \\n};\n");

    // We have already check for the IF, so continue from there
    match(OPEN_PARENTHESIS);
    match(CLOSED_PARENTHESIS);
    match(OPEN_CURLY_BRACKETS);
    match(NEWLINE);
    ST_LIST();
    match(NEWLINE);
    match(CLOSED_CURLY_BRACKETS);
    match(SEMICOLON);
}