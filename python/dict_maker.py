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
# Ejemplo: icc, clang, gcc-10, gcc, sample_size
out_file_name = sys.argv[2]
out_file_name = out_file_name + '.py'

# Importar todos los params array de params.py en settings/

tmp = sys.path
sys.path.append("../settings")
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

result = []
result = avg_maker(path, param, result)
result = time_maker(path, param, result)

# Sacar extension .py de out_file_name
print(f"{out_file_name[:-3]} = {result}")
