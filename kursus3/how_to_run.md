# Install dependencies
```bash
sudo apt install flex gcc
```
# Opgave 1
```bash
flex opgave1.l
gcc lex.yy.c -o opgave1
./opgave1 < text.txt
Found a one char (
Found a one char )
Found a one char ;
Found a variable a2131421ASDSA
Found a number 0
Found a number 858685949384
Found a number 2
Found a keyword begin
Found a keyword end
Found a variable begin2
Undefined ?end
```

# Opgave 2
```bash
flex opgave2.l
gcc lex.yy.c -o opgave2
./opgave2 < new_text.txt
```
Hvis vi kører programmet kan vi se at yylex() selv printer en masse newlines. Det kan vi ikke gøre noget ved.
```bash
(
)
;
a2131421ASDSA
0
858685949384
2
begin
end
begin2
```
| PROGRAM OUTPUT | new_text.txt   |
|----------------|----------------|
| (              | (              |
| )              | )              |
| ;              | ;              |
| a2131421ASDSA  | aa2131421ASDSA |
| 0              | 0              |
| 858685949384   | 858685949384   |
| 2              | 2              |
| begin          | begin          |
| end            | end            |
| begin2         | begin2         |
|                | **end**        |
|                | **end**        |
|                | **end**        |


Vi kan se at `end` ikke gentages i vores output da den allerede er i tabellen

# Opgave 3
We use ChatGPT to generate some random text about “Mikkel” to the text file text_mikkel.txt

Our program counts the number of times it sees a “Mikkel” and nothing else
```bash
flex opgave3.l
gcc lex.yy.c -o opgave3
./opgave1 < text_mikkel.txt
Number of "Mikkel"s is 2
```
