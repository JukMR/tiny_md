CU=nvcc
CUFLAGS=-O2 -Xcompiler=-Wall -Xcompiler=-Wextra -Xcompiler=$(particles) -arch=sm_75

CC      = gcc-10
CFLAGS  = -ffast-math -O3 -march=native $(particles)
WFLAGS	= -std=c11 -Wall -Wextra -g
LDFLAGS	= -lm -lgomp
TARGETS	= tiny_md viz
SOURCES	= $(shell echo *.cu)
OBJECTS = core.o wtime.o forces_gpu.o

particles = -DN=$(N)
N = 256

all: $(TARGETS)

viz: viz.o $(OBJECTS)
	$(CU) $(CUFLAGS) -o $@ $^ $(LDFLAGS) -lGL -lGLU -lglut

tiny_md: tiny_md.o $(OBJECTS)
	$(CU) $(CUFLAGS) -o $@ $^ $(LDFLAGS)

forces_gpu: forces_gpu.o $(OBJECTS)
	$(CU) $(CUFLAGS) -o $@ $^ $(LDFLAGS)

%.o: %.cu
	$(CU) $(CUFLAGS) -o $@ -c $<

clean:
	rm -f $(TARGETS) *.o *.xyz *.log .depend

.depend: $(SOURCES)
	$(CU) -MM $^ > $@

-include .depend
.PHONY: clean all
