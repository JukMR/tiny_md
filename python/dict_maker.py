import sys
from functools import reduce
import json
from statistics import stdev, mean


# Descomentar los parametros que se hayan probado
param = [
        # "gcc CFLAGS  = -O0",
        # "gcc CFLAGS  = -O1",
        # "gcc CFLAGS  = -O2",
        # "gcc CFLAGS  = -O2 -march=native",
        # "gcc CFLAGS  = -O3",
        # "gcc CFLAGS  = -O3 -march=native",
        # "gcc CFLAGS  = -O3 -ffast-math",
        # "gcc CFLAGS  = -O3 -funroll-loops",
        # "gcc CFLAGS  = -O3 -funswitch-loops",
        # "gcc CFLAGS  = -O3 -floop-block",
        # "gcc CFLAGS  = -O3 -march=native -DN=512",
        # "gcc CFLAGS  = -O3 -march=native -DN=1024",
        "gcc-10 CFLAGS  = -O0",
        "gcc-10 CFLAGS  = -O1",
        "gcc-10 CFLAGS  = -O2",
        "gcc-10 CFLAGS  = -O2 -march=native",
        "gcc-10 CFLAGS  = -O3",
        "gcc-10 CFLAGS  = -O3 -march=native",
        "gcc-10 CFLAGS  = -O3 -ffast-math",
        "gcc-10 CFLAGS  = -O3 -funroll-loops",
        "gcc-10 CFLAGS  = -O3 -funswitch-loops",
        "gcc-10 CFLAGS  = -O3 -floop-block",
        "gcc-10 CFLAGS  = -O3 -march=native -DN=512",
        "gcc-10 CFLAGS  = -O3 -march=native -DN=1024",
        # "clang CFLAGS  = -O0",
        # "clang CFLAGS  = -O1",
        # "clang CFLAGS  = -O2",
        # "clang CFLAGS  = -O2 -march=native",
        # "clang CFLAGS  = -O3",
        # "clang CFLAGS  = -O3 -march=native",
        # "clang CFLAGS  = -O3 -ffast-math",
        # "clang CFLAGS  = -O3 -funroll-loops",
        # "clang CFLAGS  = -O3 -funswitch-loops",
        # # "clang CFLAGS  = -O3 -floop-block",  # doesn't work on clang
        # "clang CFLAGS  = -O3 -march=native -DN=512",
        # "clang CFLAGS  = -O3 -march=native -DN=1024",
        # " -icc CFLAGS  = -O0\n",
        # " -icc CFLAGS  = -O1\n",
        # " -icc CFLAGS  = -O2\n",
        # " -icc CFLAGS  = -O2 -xHost\n",
        # " -icc CFLAGS  = -O3\n",
        # " -icc CFLAGS  = -O3 -xHost\n",
        # " -icc CFLAGS  = -O3 -fp-model fast=2 -no-prec-div\n",
        # " -icc CFLAGS  = -O3 -funroll-loops\n",
        # " -icc CFLAGS  = -O3 -funswitch-loops\n",
        # # -icc CFLAGS  = -O3 -floop-block\n", # doesn't work on icc
        # " -icc CFLAGS  = -O3 -xHost -DN=512\n",
        # " -icc CFLAGS  = -O3 -xHost -DN=1024\n",
]


def Average(lst):
    return reduce(lambda a, b: a + b, lst) / len(lst)


# Abrir archivo de salida de tiny_md para procesarlo
def avg_maker(path, param_arr):
    try:
        with open(path, 'r') as f:
            avg_list = []
            tmp = []
            for line in f:
                if "CC" in line:
                    avg_list.append(tmp)
                    tmp = []
                if "GFLOPS" in line:
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
            dict["GFLOPS: " + param_arr[i]] = round(empty_lst[i], 6)
        print(json.dumps(dict, indent=2))

    except IOError:
        print("Cannot open file")
        sys.exit(1)


def time_maker(path, param_arr):
    try:
        with open(path, 'r') as f:
            avg_list = []
            tmp = []
            for line in f:
                if "CC" in line:
                    avg_list.append(tmp)
                    tmp = []
                if "simulación" in line:
                    a = line.split('=')
                    a = float(a[1][1:10])
                    tmp.append(a)
            avg_list.append(tmp)

        avg_list = avg_list[1:]

        empty_lst = []
        sigma_list = []
        for i in avg_list:
            j = mean(i)
            s = stdev(i)
            empty_lst.append(j)
            sigma_list.append(s)

        mean_dict, sigma_dict = {}, {}
        for i in range(len(empty_lst)):
            mean_dict["mean exec time: " + param_arr[i]] = (
                                                    round(empty_lst[i], 6))
        print(json.dumps(mean_dict, indent=2))

        for i in range(len(sigma_list)):
            sigma_dict["stdev exec time: " + param_arr[i]] = (
                                                    round(sigma_list[i], 6))
        print(json.dumps(sigma_dict, indent=2))

    except IOError:
        print("Cannot open file")
        sys.exit(1)


# Elegir el path correcto para el archivo a resumir
path = "../results/gcc-10_new.res"

avg_maker(path, param)
time_maker(path, param)
