## C like code
```
e=1;
f=2;

#A e=e+f; 
#B e=f+f;
```
## Expected schweigi ASM code
```
MOV [e], 1
MOV [f], 2

MOV A, [e]
ADD A, [f]
MOV [e], A

MOV B, [f]
ADD B, [f]
MOV [e],B

e: DB 0
f: DB 0
g: DB 0
h: DB 0
```






