CC      =  clang
CFLAGS  = -fopenmp -O3 -march=native $(particles)
WFLAGS	= -std=c11 -Wall -Wextra -g
LDFLAGS	= -lm
TARGETS	= tiny_md viz
SOURCES	= $(shell echo *.c)
OBJECTS = core.o wtime.o forces.o

ispc = /opt/ispc/1.15.0/bin/ispc
ispc_flags = -g -O3 --target=avx2-i64x4 --cpu=core-avx2 $(particles) --pic

particles = -DN=$(N)
N = 500

all: pre-build $(TARGETS)

pre-build:
	$(ispc) $(ispc_flags) forces.ispc -o forces.o -h forces.h

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
