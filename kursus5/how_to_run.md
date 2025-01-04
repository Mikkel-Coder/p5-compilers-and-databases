```bash
make
./opgave3 < schweigi_source_code.txt
```


### Compile without `make`
```bash
bison -d opgave3.y
flex opgave3.l
gcc opgave3.tab.c lex.yy.c opgave3.tab.h -o opgave3
```