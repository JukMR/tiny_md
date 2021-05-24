# Esta funcion toma 2 parametros, primero el numero de veces a correr para
# conseguir la muestra y segundo las banderas para pasarle a make

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


def run(makecmd, runcmd, niterations=10):
    run_debug(1, makecmd)
    run_debug(niterations, runcmd)


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

        # Calcular los promedios y las desviaciones
        average_list, sigma_list = [] , []

        for i in newtest_list:
            if len(i) > 1: # Sample has many tests
                j = Average(i)
                s = stdev(i)
                average_list.append(j)
                sigma_list.append(s)
            elif len(i) == 1: # Sample has only one test
                average_list.append(i[0])
                sigma_list.append(-1)


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

if len(sys.argv) > 2:
    flags = sys.argv[2]
makecmd = [f"make clean && make {flags}"]
runcmd = ["./tiny_md"]

# Pasar el numero de corridas a hacer como argumento
if len(sys.argv) > 1:
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Por favor ingresar un numero para el argumento")
        sys.exit()


run(makecmd, runcmd, niterations=n)

# Imprimir y plotear los resultados
result = []
result = avg_maker('statics.res')
print(f"Los promedios son: \n{result[0]}\n")
print(f"Las desviaciones son: \n{result[1]}\n")


# Guardar los resultados en un archivo
try:
    file_object = open('results.res', 'a')
    file_object.write('\nDump result values\n')
    file_object.write('\n')
    file_object.write(str(result))
    file_object.close()
except IOError:
    print("Cannot open file")
    sys.exit(1)

plot(result[0])
