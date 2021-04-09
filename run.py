import subprocess
import sys


# Generate sub-process that execute tiny_md
def run_debug(number, bash_cmd_list):
    for i in range(number):
        bashCmd = bash_cmd_list
        process = subprocess.Popen(bashCmd, shell=True,)
        output, error = process.communicate()
        if (error is not None):
            print(f"The output is:{output}. The errors are:{error}")
            sys.exit("An error has ocurred")


# Modify makefile in order to change flags
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


# Look for params on settings/params.py, modify makefile and run all the
# posibles flags
def run(compilers, param, makecmd, runcmd):
    for i in range(len(compilers)):
        for j in range(len(param)):
            with open('statics.res', "a") as f:
                f.write(compilers[i])
                f.write(param[j])
                edit_make(compilers, param, i, j)
                run_debug(1, makecmd)
                run_debug(15, runcmd)


# Import parameters from settings/params.py

param_gcc, param_icc, compilers_gcc, compilers_icc = [], [], [], []
tmp = sys.path
sys.path.append("settings")
from params import param_gcc as p_gcc  # noqa: E402
from params import param_icc as p_icc  # noqa: E402
from params import compilers_gcc as c_gcc  # noqa: E402
from params import compilers_icc as c_icc  # noqa: E402
param_gcc = p_gcc
param_icc = p_icc
compilers_gcc = c_gcc
compilers_icc = c_icc
sys.path = tmp

makecmd = ["make clean && make"]
runcmd = ["./tiny_md"]


run(compilers_gcc, param_gcc, makecmd, runcmd)
