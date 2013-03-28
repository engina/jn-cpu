TARGET = jn-vm
LIBS = -lm
CC = gcc
CFLAGS = -g -Wall -std=c99

.PHONY: default all clean

default: $(TARGET) a.outa

all: default

OBJECTS = $(patsubst %.c, obj/%.o, $(wildcard *.c))
HEADERS = $(wildcard *.h)

obj/%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

.PRECIOUS: $(TARGET) $(OBJECTS)

$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) -Wall $(LIBS) -o $@

a.outa: ass.py tests/test.asm
	./ass.py tests/test.asm

clean:
	-rm -f *.o
	-rm -f $(TARGET)