CC      =  clang
CFLAGS  = -O3 -march=native $(particles)
WFLAGS	= -std=c11 -Wall -Wextra -g
LDFLAGS	= -lm
#CC	=  icc
#CFLAGS  = -O3 -xHost -DN=500
TARGETS	= tiny_md # viz
SOURCES	= $(shell echo *.c)
OBJECTS = core.o wtime.o forces.o

all: pre-build $(TARGETS)

pre-build:
	$(ispc) $(particles) $(ispc_flags) forces.ispc -o forces.o -h forces.h

ispc = /opt/ispc/1.15.0/bin/ispc
ispc_flags = -g -O3 --target=avx2-i64x4 --cpu=core-avx2

particles = -DN=500

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
