CC = gcc
CFLAGS = -ansi -Wall -Wextra -Werror -pedantic-errors -lm

symnmf: symnmf.o matrixmath.o matrixmath.h
	$(CC) -o symnmf symnmf.o matrixmath.o $(CFLAGS)

symnmf.o: symnmf.c matrixmath.h
	$(CC) -c symnmf.c $(CFLAGS)

matrix.o: matrixmath.c matrixmath.h
	$(CC) -c matrix.c $(CFLAGS)


clean:
	rm -f symnmf symnmf.o matrixmath.o