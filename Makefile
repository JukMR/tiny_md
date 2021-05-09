CC      =  icc
CFLAGS  = -O3 -xHost $(particles) #-fp-model fast=2 -no-prec-div -funro>
#CFLAGS  = -O3 -march=native -DN=500  # -Rpass=loop-vectorize
WFLAGS  = -std=c11 -Wall -Wextra -g
LDFLAGS = -lm
TARGETS = tiny_md viz
SOURCES = $(shell echo *.c)
OBJECTS = core.o wtime.o
particles = -DN=500
all: $(TARGETS)
viz: viz.o $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS) -lGL -lGLU -lglut
tiny_md: tiny_md.o $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)
%.o: %.c
	$(CC) $(WFLAGS) $(CPPFLAGS) $(CFLAGS) -c $<
clean:
	rm -f $(TARGETS) *.o *.xyz *.log .depend
.depend: $(SOURCES)
	$(CC) -MM $^ > $@
-include .depend
.PHONY: clean all
