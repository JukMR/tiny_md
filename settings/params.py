param_gcc_10 = [
#    "CFLAGS  = -O0\n",
#    "CFLAGS  = -O1\n",
#    "CFLAGS  = -O2\n",
    "CFLAGS  = -O2 -march=native -DN=512\n",
#    "CFLAGS  = -O3\n",
#    "CFLAGS  = -O3 -march=native\n",
#    "CFLAGS  = -O3 -ffast-math\n",
#    "CFLAGS  = -O3 -funroll-loops\n",
#    "CFLAGS  = -O3 -funswitch-loops\n",
#    "CFLAGS  = -O3 -floop-block\n",
#    "CFLAGS  = -O3 -march=native -DN=512\n",
#    "CFLAGS  = -O3 -march=native -DN=1024\n",
]

param_gcc = [
#    "CFLAGS  = -O0\n",
#    "CFLAGS  = -O1\n",
#    "CFLAGS  = -O2\n",
    "CFLAGS  = -O2 -march=native -DN=512\n",
#    "CFLAGS  = -O3\n",
#    "CFLAGS  = -O3 -march=native\n",
#    "CFLAGS  = -O3 -ffast-math\n",
#    "CFLAGS  = -O3 -funroll-loops\n",
#    "CFLAGS  = -O3 -funswitch-loops\n",
#    "CFLAGS  = -O3 -floop-block\n",
#    "CFLAGS  = -O3 -march=native -DN=512\n",
#    "CFLAGS  = -O3 -march=native -DN=1024\n",
]

param_clang = [
#    "CFLAGS  = -O0\n",
#    "CFLAGS  = -O1\n",
#    "CFLAGS  = -O2\n",
    "CFLAGS  = -O2 -march=native -ND=512\n",
#    "CFLAGS  = -O3\n",
#    "CFLAGS  = -O3 -march=native\n",
#    "CFLAGS  = -O3 -ffast-math\n",
#    "CFLAGS  = -O3 -funroll-loops\n",
#    "CFLAGS  = -O3 -funswitch-loops\n",
#    "CFLAGS  = -O3 -march=native -DN=512\n",
#    "CFLAGS  = -O3 -march=native -DN=1024\n",
]

param_sample_size = [
#    "CFLAGS  = -O3 -march=native -DN=300\n",
#    "CFLAGS  = -O3 -march=native -DN=356\n",
#    "CFLAGS  = -O3 -march=native -DN=400\n",
#    "CFLAGS  = -O3 -march=native -DN=500\n",
#    "CFLAGS  = -O3 -march=native -DN=600\n",
#    "CFLAGS  = -O3 -march=native -DN=700\n",
#    "CFLAGS  = -O3 -march=native -DN=800\n",
#    "CFLAGS  = -O3 -march=native -DN=900\n",
#    "CFLAGS  = -O3 -march=native -DN=1000\n",
]

param_icc = [
#    "CFLAGS  = -O0\n",
#    "CFLAGS  = -O1\n",
#    "CFLAGS  = -O2\n",
    "CFLAGS  = -O2 -xHost -DN=512\n",
#    "CFLAGS  = -O3\n",
#    "CFLAGS  = -O3 -xHost\n",
#    "CFLAGS  = -O3 -fp-model fast=2 -no-prec-div\n",
#    "CFLAGS  = -O3 -funroll-loops\n",
#    "CFLAGS  = -O3 -funswitch-loops\n",
#    "CFLAGS  = -O3 -xHost -DN=512\n",
#    "CFLAGS  = -O3 -xHost -DN=1024\n",
]

param_gcc_10_floop_block_dict = [
#    "CFLAGS  = -O3 -floop-block\n",
#    "CFLAGS  = -O3 -floop-block -DN=512\n",
#    "CFLAGS  = -O3 -floop-block -DN=1024\n",
]

compilers_gcc = ["CC      =  gcc\n"]
compilers_gcc_10 = ["CC      =  gcc-10\n"]
compilers_clang = ["CC      =  clang\n"]
compilers_icc = ["CC      =  icc\n"]

