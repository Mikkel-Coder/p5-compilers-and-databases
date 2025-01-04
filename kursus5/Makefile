CC = gcc # C Compiler
YACC = bison # Yet Another Compiler Compiler
LEX = flex # Fast LEX
EXECUTABLE = opgave3
YACC_FILE = $(EXECUTABLE).y
LEX_FILE = $(EXECUTABLE).l
YACC_HEADER = $(EXECUTABLE).tab.h
YACC_C = $(EXECUTABLE).tab.c
LEX_C = lex.yy.c

all: $(EXECUTABLE)

# Use YACC to compile our grammer (production rules)
# -d is used to output header file for cross referens in LEX
$(YACC_C) $(YACC_HEADER): $(YACC_FILE)
	@$(YACC) -d $(YACC_FILE)

# Compile our lexical
$(LEX_C): $(LEX_FILE)
	@$(LEX) $(LEX_FILE)

# Now compile our yacc and flex code to get an executable
$(EXECUTABLE): $(YACC_C) $(LEX_C) $(YACC_HEADER)
	@$(CC) $(YACC_C) $(LEX_C) $(YACC_HEADER) -o $(EXECUTABLE)

clean:
	@rm $(EXECUTABLE) $(YACC_C) $(LEX_C) $(YACC_HEADER)

.PHONY: all clean