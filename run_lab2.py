import subprocess
import sys
from statistics import stdev, mean
from functools import reduce

import matplotlib.pyplot as plt

# Generate sub-process that execute tiny_md
def run_debug(number, bash_cmd_list):
    for i in range(number):
        bashCmd = bash_cmd_list
        process = subprocess.Popen(bashCmd, shell=True,)
        output, error = process.communicate()
        if (error is not None):
            print(f"The output is:{output}. The errors are:{error}")
            sys.exit("An error has ocurred")


def run(makecmd, runcmd):
    run_debug(1, makecmd)
    run_debug(10, runcmd)


def Average(lst):
    return reduce(lambda a, b: a + b, lst) / len(lst)


# Abrir archivo .res para procesarlo
def avg_maker(path):
    app_arr = []
    try:
        with open(path, 'r') as f:
            newtest_list, tmp = [], []
            for line in f:
                if "Begin new test" in line:
                    if len(tmp) != 0:
                        newtest_list.append(tmp)
                        tmp = []
                if "GFLOPS" in line:
                    a = line.split(':')
                    a = float(a[1][1:])
                    tmp.append(a)
            newtest_list.append(tmp)


        average_list, sigma_list = [] , []

        for i in newtest_list:
            j = Average(i)
            s = stdev(i)
            average_list.append(j)
            sigma_list.append(s)


        average_dict, sigma_dict = [], []
        for i in average_list:
            average_dict.append((round(i, 6)))
        app_arr.append(average_dict)

        for i in sigma_list:
            sigma_dict.append((round(i, 6)))
        app_arr.append(sigma_dict)

        return app_arr

    except IOError:
        print("Cannot open file")
        sys.exit(1)
    return app_arr


def plot(arr):
    x = [i for i in range(len(arr))]
    plt.scatter(x, arr, label= "stars", color= "green",
                marker= "*", s=30)

    # Eje x - Iteracion
    plt.xlabel('Iteraciones')
    plt.xticks(range(len(arr)))

    # Eje y - GFLOPS
    plt.ylabel('GFLOPS')
    plt.yscale('log')

    plt.title('Comparacion GFLOPS')
    plt.show()



# Empezar nueva simulacion en statics.res
try:
    file_object = open('statics.res', 'a')
    file_object.write('Begin new test\n')
    file_object.close()
except IOError:
    print("Cannot open file")
    sys.exit(1)


# Ejecutar el programa
makecmd = ["make clean && make"]
runcmd = ["./tiny_md"]
run(makecmd, runcmd)

# Imprimir y plotear los resultados
result = []
result = avg_maker('statics.res')
print(result)

plot(result[0])