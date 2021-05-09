#!/bin/bash
#SBATCH --job-name=tinymd
##SBATCH --nodes=1
#SBATCH --ntasks-per-node=1

echo "CFLAG	time	stdevtime	GFLOPS	insn" > results.plot

cat > Makefile <<'EOF'
CC      =  clang #icc #clang
#CFLAGS  = -Ofast -xHost -DN=500 #-fp-model fast=2 -no-prec-div -funro>
CFLAGS  = -O3 -march=native $(particles)  # -Rpass=loop-vectorize
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
EOF
srun make clean && make && perf stat -r 10 ./tiny_md
vtime=$(tail slurm-$SLURM_JOB_ID.out | grep elapsed | cut -d + -f 1 | xargs)
vtimeerr=$(tail slurm-$SLURM_JOB_ID.out | grep elapsed | cut -d - -f 2 |cut -d s -f 1 | xargs)
vGFLOPS=$(tail -n 4 statics.res | grep GFLOPS| cut -d : -f 2 | xargs)
vinsn=$(tail slurm-$SLURM_JOB_ID.out | grep insn | cut -d '#' -f 2 | cut -d i -f 1| xargs)
echo "clang -O3 -march=native",$vtime,$vtimeerr,$vGFLOPS,$vinsn >> results.plot
#####################################################################################################
source /opt/intel/oneapi/setvars.sh
cat > Makefile <<'EOF'
CC      =  clang #icc #clang
#CFLAGS  = -Ofast -xHost -DN=500 #-fp-model fast=2 -no-prec-div -funro>
CFLAGS  = -O3 -march=native $(particles)  # -Rpass=loop-vectorize
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
EOF
srun make clean && make && perf stat -r 10 ./tiny_md
vtime=$(tail slurm-$SLURM_JOB_ID.out | grep elapsed | cut -d + -f 1 | xargs)
vtimeerr=$(tail slurm-$SLURM_JOB_ID.out | grep elapsed | cut -d - -f 2 |cut -d s -f 1 | xargs)
vGFLOPS=$(tail -n 4 statics.res | grep GFLOPS| cut -d : -f 2 | xargs)
vinsn=$(tail slurm-$SLURM_JOB_ID.out | grep insn | cut -d '#' -f 2 | cut -d i -f 1| xargs)
echo "(intel)clang -O3 -march=native",$vtime,$vtimeerr,$vGFLOPS,$vinsn >> results.plot
#####################################################################################################
cat > Makefile <<'EOF'
CC      =  gcc-10 #icc #clang
#CFLAGS  = -Ofast -xHost -DN=500 #-fp-model fast=2 -no-prec-div -funro>
CFLAGS  = -O3 -march=native $(particles)  # -Rpass=loop-vectorize
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
EOF
srun make clean && make && perf stat -r 10 ./tiny_md
vtime=$(tail slurm-$SLURM_JOB_ID.out | grep elapsed | cut -d + -f 1 | xargs)
vtimeerr=$(tail slurm-$SLURM_JOB_ID.out | grep elapsed | cut -d - -f 2 |cut -d s -f 1 | xargs)
vGFLOPS=$(tail -n 4 statics.res | grep GFLOPS| cut -d : -f 2 | xargs)
vinsn=$(tail slurm-$SLURM_JOB_ID.out | grep insn | cut -d '#' -f 2 | cut -d i -f 1| xargs)
echo "gcc-10 -O3 -march=native",$vtime,$vtimeerr,$vGFLOPS,$vinsn >> results.plot
#####################################################################################################
cat > Makefile <<'EOF'
CC      =  icc #clang
CFLAGS  = -O2 -xHost $(particles) #-fp-model fast=2 -no-prec-div -funro>
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
EOF
srun make clean && make && perf stat -r 10 ./tiny_md
vtime=$(tail slurm-$SLURM_JOB_ID.out | grep elapsed | cut -d + -f 1 | xargs)
vtimeerr=$(tail slurm-$SLURM_JOB_ID.out | grep elapsed | cut -d - -f 2 |cut -d s -f 1 | xargs)
vGFLOPS=$(tail -n 4 statics.res | grep GFLOPS| cut -d : -f 2 | xargs)
vinsn=$(tail slurm-$SLURM_JOB_ID.out | grep insn | cut -d '#' -f 2 | cut -d i -f 1| xargs)
echo "icc -O2 -xHost",$vtime,$vtimeerr,$vGFLOPS,$vinsn >> results.plot
#####################################################################################################
cat > Makefile <<'EOF'
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
EOF
srun make clean && make && perf stat -r 10 ./tiny_md
vtime=$(tail slurm-$SLURM_JOB_ID.out | grep elapsed | cut -d + -f 1 | xargs)
vtimeerr=$(tail slurm-$SLURM_JOB_ID.out | grep elapsed | cut -d - -f 2 |cut -d s -f 1 | xargs)
vGFLOPS=$(tail -n 4 statics.res | grep GFLOPS| cut -d : -f 2 | xargs)
vinsn=$(tail slurm-$SLURM_JOB_ID.out | grep insn | cut -d '#' -f 2 | cut -d i -f 1| xargs)
echo "icc -O3 -xHost",$vtime,$vtimeerr,$vGFLOPS,$vinsn >> results.plot
