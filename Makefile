CC      =  clang
CFLAGS  = -O0 -march=native -DN=500
WFLAGS	= -std=c11 -Wall -Wextra -g
LDFLAGS	= -lm

TARGETS	= tiny_md viz
SOURCES	= $(shell echo *.c)
OBJECTS = core.o wtime.o forces.o

all: pre-build $(TARGETS)

pre-build:
	/home/julian/programs/ispc/ispc-v1.15.0-linux/bin/ispc --target=sse2-i32x4	forces.ispc -o forces.o


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
