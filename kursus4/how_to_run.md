```bash
flex opgave1-l
gcc lex.yy.c -o opgave1
./opgave1 < input_text.txt
PROG ⟶ ST_LIST
ST_LIST ⟶ ST \n ST_LIST | ε
ST ⟶ ST if() { \n ST_LIST \n};
ST_LIST ⟶ ST \n ST_LIST | ε
ST_LIST ⟶ ST \n ST_LIST | ε
SUCCESS!
./opgave1 < input_error.txt
PROG ⟶ ST_LIST
ST_LIST ⟶ ST \n ST_LIST | ε
ST ⟶ ST if() { \n ST_LIST \n};
ST_LIST ⟶ ST \n ST_LIST | ε
Error at line 4
Expected "\n". Got "(null)"
```

Notice that `input_error.txt` is missing a `\n` (newline) at the end. This is required by the language!