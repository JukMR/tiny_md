#!/usr/bin/env python
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
        # "gcc-10 CFLAGS  = -O0",
        # "gcc-10 CFLAGS  = -O1",
        # "gcc-10 CFLAGS  = -O2",
        # "gcc-10 CFLAGS  = -O2 -march=native",
        # "gcc-10 CFLAGS  = -O3",
        # "gcc-10 CFLAGS  = -O3 -march=native",
        # "gcc-10 CFLAGS  = -O3 -ffast-math",
        # "gcc-10 CFLAGS  = -O3 -funroll-loops",
        # "gcc-10 CFLAGS  = -O3 -funswitch-loops",
        # "gcc-10 CFLAGS  = -O3 -floop-block\n",
        # "gcc-10 CFLAGS  = -O3 -floop-block -DN=512\n",
        # "gcc-10 CFLAGS  = -O3 -floop-block -DN=1024\n",
        # "gcc-10 CFLAGS  = -O3 -march=native -DN=512",
        # "gcc-10 CFLAGS  = -O3 -march=native -DN=1024",
        "CFLAGS  = -O3 -march=native -DN=300\n",
        "CFLAGS  = -O3 -march=native -DN=356\n",
        "CFLAGS  = -O3 -march=native -DN=400\n",
        "CFLAGS  = -O3 -march=native -DN=500\n",
        "CFLAGS  = -O3 -march=native -DN=600\n",
        "CFLAGS  = -O3 -march=native -DN=700\n",
        "CFLAGS  = -O3 -march=native -DN=800\n",
        "CFLAGS  = -O3 -march=native -DN=900\n",
        "CFLAGS  = -O3 -march=native -DN=1000\n",
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
def avg_maker(path, param_arr, app_arr):
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

        output_lst = []
        empty_lst = []
        for i in avg_list:
            i = Average(i)
            empty_lst.append(i)

        dict = {}
        for i in range(len(empty_lst)):
            dict["GFLOPS: " + param_arr[i][:-1]] = round(empty_lst[i], 6)
        app_arr.append(dict)

    except IOError:
        print("Cannot open file")
        sys.exit(1)
    return app_arr


def time_maker(path, param_arr, app_arr):
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
            mean_dict["mean exec time: " + param_arr[i][:-1]] = (
                                                    round(empty_lst[i], 6))
        app_arr.append(mean_dict)

        for i in range(len(sigma_list)):
            sigma_dict["stdev exec time: " + param_arr[i][:-1]] = (
                                                    round(sigma_list[i], 6))
        app_arr.append(sigma_dict)

    except IOError:
        print("Cannot open file")
        sys.exit(1)
    return app_arr


# Elegir el path para el archivo .res de entrada
file_name = input("Agregar el nombre del archivo .res a procesar\n")
path = "../results/" + file_name
path = path + '.res'

# Agregar el nombre del arreglo a generar para salida
# Ejemplo: icc, clang, gcc-10, gcc, sample_test
out_file_name = input("Enter output file name\n")
out_file_name = out_file_name + '.py'

result = []
result = avg_maker(path, param, result)
result = time_maker(path, param, result)
print(f"{out_file_name[:-3]} = {result}")
