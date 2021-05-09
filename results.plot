CFLAG	time	stdevtime	GFLOPS	insn
clang -O3 -march=native,12.8176,0.0611,0.802110,1.31
(intel)clang -O3 -march=native,13.1423,0.0986,0.784552,1.31
gcc-5 -O3 -march=native,13.2468,0.0454,0.775187,1.32
icc -O2 -xHost,13.229,0.111,0.767117,1.29
icc -O3 -xHost,13.054,0.172,0.794437,1.29
