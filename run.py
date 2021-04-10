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
        with open('Makefile', "r") as mr:
            a = list(mr.readlines())
            a[0] = compilers_list[compiler]
            a[1] = param[flag]
            try:
                with open('Makefile', "w") as mw:
                    mw.writelines(a)
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
            with open('statics.res', "a") as sa:
                sa.write(compilers[i])
                sa.write(param[j])
            edit_make(compilers, param, i, j)
            run_debug(1, makecmd)
            run_debug(2, runcmd)


# Import parameters from settings/params.py

tmp = sys.path
sys.path.append("settings")
compiler, param = [], []
if (sys.argv[1] == 'gcc'):
    from params import param_gcc as p_gcc
    from params import compilers_gcc as c_gcc
    compiler = c_gcc
    param = p_gcc
elif (sys.argv[1] == 'gcc_10'):
    from params import param_gcc_10 as p_gcc_10
    from params import compilers_gcc_10 as c_gcc_10
    compiler = c_gcc_10
    param = p_gcc_10
elif (sys.argv[1] == 'clang'):
    from params import param_clang as p_clang
    from params import compilers_clang as c_clang
    compiler = c_clang
    param = p_clang
elif (sys.argv[1] == 'icc'):
    from params import param_icc as p_icc
    from params import compilers_icc as c_icc
    compiler = c_icc
    param = p_icc
elif (sys.argv[1] == 'sample_size'):
    from params import param_sample_size as p_sample_size
    from params import compilers_gcc_10 as compilers_gcc_10
    compiler = compilers_gcc_10
    param = p_sample_size
elif (sys.argv[1] == 'gcc_10_floop_block'):
    from params import param_gcc_10_floop_block as p_gcc_10_floop_block
    from params import compilers_gcc_10 as compilers_gcc_10
    compiler = compilers_gcc_10
    param = p_gcc_10_floop_block

sys.path = tmp

makecmd = ["make clean && make"]
runcmd = ["./tiny_md"]


run(compiler, param, makecmd, runcmd)
