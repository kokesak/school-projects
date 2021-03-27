CC = gcc
CFLAGS = -std=c99 -pedantic -Wall -Wextra -g

#main: main
main: main.c scanner.c help.c precedence.c analysis.c
	$(CC) $(CFLAGS) -o ifj18 main.c scanner.c help.c stack.c precedence.c analysis.c -lm

clean:
	rm main


	
