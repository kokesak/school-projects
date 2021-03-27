# Makefile
#	make - pro sestaveni
#	rm - pro smazani

CFLAGS=-std=gnu99 -Wall -Wextra -Werror -pedantic
CC=gcc
LFLAGS=-lpthread
BIN=proj2
SOURCE=proj2.c

all:
	$(CC) $(CFLAGS) $(SOURCE) -o $(BIN) $(LFLAGS)

clean:
	rm $(BIN)
