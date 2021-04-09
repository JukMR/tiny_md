import subprocess
import sys


def run_debug(number, bash_cmd_list):
    for i in range(number):
        bashCmd = bash_cmd_list
        process = subprocess.Popen(bashCmd, shell=True,)
        output, error = process.communicate()
        if (error is not None):
            print(f"The output is:{output}. The errors are:{error}")
            sys.exit("An error has ocurred")


def edit_make(compilers_list, param, compiler, flag):
    try:
        with open('Makefile', "r") as f:
            a = list(f.readlines())
            a[0] = compilers_list[compiler]
            a[1] = param[flag]
            try:
                with open('Makefile', "w") as f:
                    f.writelines(a)
                    print(f"changed:\n {a[0]} {a[1]}")
            except IOError:
                print("Cannot open file")
                sys.exit(1)
    except IOError:
        print("Cannot open file")
        sys.exit(1)


param_gcc = [
        # "CFLAGS  = -O0\n",
        # "CFLAGS  = -O1\n",
        # "CFLAGS  = -O2\n",
        # "CFLAGS  = -O2 -march=native\n",
        # "CFLAGS  = -O3\n",
        # "CFLAGS  = -O3 -march=native\n",
        # "CFLAGS  = -O3 -ffast-math\n",
        # "CFLAGS  = -O3 -funroll-loops\n",
        # "CFLAGS  = -O3 -funswitch-loops\n",
        # "CFLAGS  = -O3 -floop-block\n",
        # "CFLAGS  = -O3 -floop-block -DN=512\n",
        # "CFLAGS  = -O3 -floop-block -DN=1024\n",
        # "CFLAGS  = -O3 -march=native -DN=512\n",
        # "CFLAGS  = -O3 -march=native -DN=512\n",
        "CFLAGS  = -O3 -march=native -DN=300\n",
        "CFLAGS  = -O3 -march=native -DN=356\n",
        "CFLAGS  = -O3 -march=native -DN=400\n",
        "CFLAGS  = -O3 -march=native -DN=500\n",
        "CFLAGS  = -O3 -march=native -DN=600\n",
        "CFLAGS  = -O3 -march=native -DN=700\n",
        "CFLAGS  = -O3 -march=native -DN=800\n",
        "CFLAGS  = -O3 -march=native -DN=900\n",
        "CFLAGS  = -O3 -march=native -DN=1000\n",
        # "CFLAGS  = -O3 -march=native -DN=1024\n",
]
param_icc = [
        "CFLAGS  = -O0\n",
        "CFLAGS  = -O1\n",
        "CFLAGS  = -O2\n",
        "CFLAGS  = -O2 -xHost\n",
        "CFLAGS  = -O3\n",
        "CFLAGS  = -O3 -xHost\n",
        "CFLAGS  = -O3 -fp-model fast=2 -no-prec-div\n",
        "CFLAGS  = -O3 -funroll-loops\n",
        "CFLAGS  = -O3 -funswitch-loops\n",
        "CFLAGS  = -O3 -xHost -DN=512\n",
        "CFLAGS  = -O3 -xHost -DN=1024\n",
]

compilers_gcc = [
        # "CC      =  gcc\n",
        "CC      =  gcc-10\n",
        # "CC      =  clang\n",
]
compilers_icc = [
        "CC      =  icc\n",
]

makecmd = ["make clean && make"]
runcmd = ["./tiny_md"]


def run(compilers, param, makecmd, runcmd):
    for i in range(len(compilers)):
        for j in range(len(param)):
            with open('statics.res', "a") as f:
                f.write(compilers[i])
                f.write(param[j])
            edit_make(compilers, param, i, j)
            run_debug(1, makecmd)
            run_debug(15, runcmd)


run(compilers_gcc, param_gcc, makecmd, runcmd)
