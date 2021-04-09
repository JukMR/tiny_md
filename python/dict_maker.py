import sys
from functools import reduce
import json
from statistics import stdev, mean
import os


def Average(lst):
    return reduce(lambda a, b: a + b, lst) / len(lst)


# Abrir archivo .res para procesarlo
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
        sigma_list = []

        for i in avg_list:
            j = Average(i)
            s = stdev(i)
            empty_lst.append(j)
            sigma_list.append(s)

        mean_dict, sigma_dict = {}, {}
        for i in range(len(empty_lst)):
            mean_dict["GFLOPS: " + param_arr[i][:-1]] = (
                                                    round(empty_lst[i], 6))
        app_arr.append(mean_dict)

        for i in range(len(sigma_list)):
            sigma_dict["stdev GFLOPS: " + param_arr[i][:-1]] = (
                                                    round(sigma_list[i], 6))
        app_arr.append(sigma_dict)

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


# Elegir el path para el archivo .res de entrada dentro de la carpeta results/
file_name = sys.argv[1]
path = "../results/" + file_name
path = path + '.res'

# Agregar el nombre del arreglo a generar para salida
# Ejemplo: icc, clang, gcc-10, gcc, sample_test
out_file_name = sys.argv[2]
out_file_name = out_file_name + '.py'

# Importar todos los params array de params.py en settings/
param = []
tmp = sys.path
sys.path.append("../settings")
from params import param_gcc as p  # noqa: E402
param = p
sys.path = tmp

result = []
result = avg_maker(path, param, result)
result = time_maker(path, param, result)

# Sacar extension .py de out_file_name
print(f"{out_file_name[:-3]} = {result}")
