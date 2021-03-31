import sys
from functools import reduce
import json


param = [
        # "gcc CFLAGS  = -O0\n",
        # "gcc CFLAGS  = -O0 -march=native\n",
        # "gcc CFLAGS  = -O1\n",
        # "gcc CFLAGS  = -O1 -march=native\n",
        # "gcc CFLAGS  = -O2\n",
        # "gcc CFLAGS  = -O2 -march=native\n",
        # "gcc CFLAGS  = -O3\n",
        # "gcc CFLAGS  = -O3 -march=native\n",
        # "gcc CFLAGS  = -O3 -DN=512 \n",
        # "gcc CFLAGS  = -O3 -march=native -DN=512\n",
        # "gcc CFLAGS  = -O3 -DN=1024 \n",
        # "gcc CFLAGS  = -O3 -march=native -DN=1024\n",
        "gcc-10 CFLAGS  = -O0\n",
        "gcc-10 CFLAGS  = -O0 -march=native\n",
        "gcc-10 CFLAGS  = -O1\n",
        "gcc-10 CFLAGS  = -O1 -march=native\n",
        "gcc-10 CFLAGS  = -O2\n",
        "gcc-10 CFLAGS  = -O2 -march=native\n",
        "gcc-10 CFLAGS  = -O3\n",
        "gcc-10 CFLAGS  = -O3 -march=native\n",
        "gcc-10 CFLAGS  = -O3 -DN=512 \n",
        "gcc-10 CFLAGS  = -O3 -march=native -DN=512\n",
        "gcc-10 CFLAGS  = -O3 -DN=1024 \n",
        "gcc-10 CFLAGS  = -O3 -march=native -DN=1024\n",
        # "clang CFLAGS  = -O0\n",
        # "clang CFLAGS  = -O0 -march=native\n",
        # "clang CFLAGS  = -O1\n",
        # "clang CFLAGS  = -O1 -march=native\n",
        # "clang CFLAGS  = -O2\n",
        # "clang CFLAGS  = -O2 -march=native\n",
        # "clang CFLAGS  = -O3\n",
        # "clang CFLAGS  = -O3 -march=native\n",
        # "clang CFLAGS  = -O3 -DN=512 \n",
        # "clang CFLAGS  = -O3 -march=native -DN=512\n",
        # "clang CFLAGS  = -O3 -DN=1024 \n",
        # "clang CFLAGS  = -O3 -march=native -DN=1024\n",
        # "icc CFLAGS  = -O0\n",
        # "icc CFLAGS  = -O0 -march=native\n",
        # "icc CFLAGS  = -O1\n",
        # "icc CFLAGS  = -O1 -march=native\n",
        # "icc CFLAGS  = -O2\n",
        # "icc CFLAGS  = -O2 -march=native\n",
        # "icc CFLAGS  = -O3\n",
        # "icc CFLAGS  = -O3 -march=native\n",
        # "icc CFLAGS  = -O3 -DN=512 \n",
        # "icc CFLAGS  = -O3 -march=native -DN=512\n",
        # "icc CFLAGS  = -O3 -DN=1024 \n",
        # "icc CFLAGS  = -O3 -march=native -DN=1024\n",
]


def Average(lst):
    return reduce(lambda a, b: a + b, lst) / len(lst)


# Abrir archivo de salida de tiny_md para procesarlo
try:
    with open("../results/gcc_clang_statics.result", 'r') as f:
        avg_list = []
        tmp = []
        for line in f:
            if "CC" in line:
                avg_list.append(tmp)
                tmp = []
            if line[0:5] == "FLOPS":
                a = line.split(':')
                a = float(a[1][1:])
                tmp.append(a)
        avg_list.append(tmp)

    avg_list = avg_list[1:]

    empty_lst = []
    for i in avg_list:
        i = Average(i)
        empty_lst.append(i)

    dict = {}
    for i in range(len(empty_lst)):
        dict[param[i]] = empty_lst[i]
    print(json.dumps(dict, indent=2))

except IOError:
    print("Cannot open file")
    sys.exit(1)
