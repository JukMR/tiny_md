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


def edit_make(compiler, flag):
    try:
        with open('Makefile', "r") as f:
            a = list(f.readlines())
            a[0] = compilers[compiler]
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


param = [
        "CFLAGS  = -O0\n",
        "CFLAGS  = -O0 -march=native\n",
        "CFLAGS  = -O1\n",
        "CFLAGS  = -O1 -march=native\n",
        "CFLAGS  = -O2\n",
        "CFLAGS  = -O2 -march=native\n",
        "CFLAGS  = -O3\n",
        "CFLAGS  = -O3\n -floop-block",
        "CFLAGS  = -O3\n -ffast-math",
        "CFLAGS  = -O3\n -funroll-loops",

        "CFLAGS  = -O3 -march=native\n",
        "CFLAGS  = -O3 -DN=512 \n",
        "CFLAGS  = -O3 -march=native -DN=512\n",
        "CFLAGS  = -O3 -DN=1024 \n",
        "CFLAGS  = -O3 -march=native -DN=1024\n",
]

compilers = [
        # "CC      =  gcc\n",
        "CC      =  gcc-10\n",
        # "CC      =  clang\n",
        # "CC      =  icc\n",
]

makecmd = ["make clean && make"]
runcmd = ["./tiny_md"]


def run(compilers, param, makecmd, runcmd):
    for i in range(len(compilers)):
        for j in range(len(param)):
            with open('statics.result', "a") as f:
                f.write(compilers[i])
                f.write(param[j])
            edit_make(i, j)
            run_debug(1, makecmd)
            run_debug(30, runcmd)


run(compilers, param, makecmd, runcmd)
