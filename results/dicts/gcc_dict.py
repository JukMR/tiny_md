gcc = [
 {
  "GFLOPS: -O0": 0.153156,
  "GFLOPS: -O1": 0.312658,
  "GFLOPS: -O2": 0.390438,
  "GFLOPS: -O2 -march=native": 0.40261,
  "GFLOPS: -O3": 0.38444,
  "GFLOPS: -O3 -march=native": 0.406484,
  "GFLOPS: -O3 -ffast-math": 0.405531,
  "GFLOPS: -O3 -funroll-loops": 0.381612,
  "GFLOPS: -O3 -funswitch-loops": 0.385727,
  "GFLOPS: -O3 -floop-block": 0.384896,
  "GFLOPS: -O3 -march=native -DN=512": 0.553402,
  "GFLOPS: -O3 -march=native -DN=1024": 0.470277
 },
 {
  "mean exec time: -O0": 17.476285,
  "mean exec time: -O1": 8.560833,
  "mean exec time: -O2": 6.855524,
  "mean exec time: -O2 -march=native": 6.648172,
  "mean exec time: -O3": 6.962517,
  "mean exec time: -O3 -march=native": 6.585195,
  "mean exec time: -O3 -ffast-math": 6.600456,
  "mean exec time: -O3 -funroll-loops": 7.014125,
  "mean exec time: -O3 -funswitch-loops": 6.939561,
  "mean exec time: -O3 -floop-block": 6.954407,
  "mean exec time: -O3 -march=native -DN=512": 19.384284,
  "mean exec time: -O3 -march=native -DN=1024": 91.337172
 },
 {
  "stdev exec time: -O0": 0.115926,
  "stdev exec time: -O1": 0.060248,
  "stdev exec time: -O2": 0.054385,
  "stdev exec time: -O2 -march=native": 0.047458,
  "stdev exec time: -O3": 0.057499,
  "stdev exec time: -O3 -march=native": 0.069188,
  "stdev exec time: -O3 -ffast-math": 0.057755,
  "stdev exec time: -O3 -funroll-loops": 0.058835,
  "stdev exec time: -O3 -funswitch-loops": 0.072703,
  "stdev exec time: -O3 -floop-block": 0.066279,
  "stdev exec time: -O3 -march=native -DN=512": 0.11821,
  "stdev exec time: -O3 -march=native -DN=1024": 0.913929
 }
]
