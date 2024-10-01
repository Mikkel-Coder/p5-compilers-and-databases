; e = 1
MOV [e], 1

; f = 2
MOV [f], 2


; e = e + f
MOV A, [e]
ADD A, [f]
MOV [e], A

; e = f + f
MOV B, [f]
ADD B, [f]
MOV [e], B
HLT

; Variables
e: DB 0
f: DB 0
g: DB 0
h: DB 0
