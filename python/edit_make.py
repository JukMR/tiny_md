param = [
        "CFLAGS  = -O0\n", "CFLAGS  = -O0 -march=native\n",
        "CFLAGS  = -O1\n", "CFLAGS  = -O1 -march=native\n",
        "CFLAGS  = -O2\n", "CFLAGS  = -O2 -march=native\n",
        "CFLAGS  = -O3\n", "CFLAGS  = -O3 -march=native\n",
        "CFLAGS  = -O3 -DN=512 \n", "CFLAGS  = -O3 -march=native -DN=512\n",
        "CFLAGS  = -O3 -DN=1024 \n", "CFLAGS  = -O3 -march=native -DN=1024\n",
        ]
compilers = [
        "CC      =  gcc\n", "CC      =  clang\n",
]


def edit_make(compiler, flag):
    with open('../Makefile', "r") as f:
        a = list(f.readlines())
    a[0] = compilers[compiler]
    a[1] = param[flag]
    with open('../Makefile', "w") as f:
        f.writelines(a)
        print(f"changed:\n {a[0]} {a[1]}")


edit_make(0, 5)
