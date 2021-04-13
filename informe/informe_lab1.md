## Introducción

En este laboratorio analizamos diferentes optimizaciones para mejorar la
performance del problema de Dinámica molecular. Hicimos 30 pruebas con cada
parámetro a probar y obtuvimos la media muestral y la desviación estándar
muestral de cada uno. Así, podemos obtener una función normal que nos de mas
certeza que los valores medidos son correctos.

## Optimizaciones

Para el experimento probamos con 4 compiladores diferentes para analizar sus
distintos comportamientos:

* gcc versión 9.3.0-17
* gcc versión 10.2.0-5
* clang versión 10.0.0-4
* icc 2021.1 Beta 20201112

Y comparamos la ejecución del problema con los siguientes parámetros:

```
-O0
-O1
-O2
-O2 -march=native
-O3
-O3 -march=native
-O3 -ffast-math
-O3 -funroll-loops
-O3 -funswitch-loops
-O3 -march=native -DN=512
-O3 -march=native -DN=1024
```

En el caso del compilador de Intel que implementa las mismas funciones pero con
distinto nombre:

```
* -O0
* -O1
* -O2
* -O2 -xHost
* -O3
* -O3 -xHost
* -O3 -fp-model fast=2 -no-prec-div
* -O3 -funroll-loops
* -O3 -funswitch-loops
* -O3 -xHost -DN=512
* -O3 -xHost -DN=1024
```

Además solamente para gcc 9.3 y gcc 10.2 probamos la siguiente bandera:

```
* -O3 -floop-block
```


### Resultados

# Escala de tamaños de muestras

Probamos como se comportaba el problema al incrementar gradualmente el tamaño de
muestra:

```
* -O3 -march=native -DN=300
* -O3 -march=native -DN=356
* -O3 -march=native -DN=400
* -O3 -march=native -DN=500
* -O3 -march=native -DN=600
* -O3 -march=native -DN=700
* -O3 -march=native -DN=800
* -O3 -march=native -DN=900
* -O3 -march=native -DN=1000
```

### Resultados


## Características del hardware y software

### CPU

* Amd Ryzen 5 3500 - 6 núcleos
* Min. veloc. : 2,2 GHz
* Max. veloc. : 4,1 GHz
* Cache L1d : 192 KiB
* Cache L1i : 192 KiB
* Cache L2 : 3 MiB
* Cache L3 : 16 MiB

### Memoria Ram

* Memoria total del sistema: 16 GiB (2x GiB) Dual Channel DDR4 2,666 MHz

### Compiladores

* gcc versión 9.3.0-17
* gcc versión 10.2.0-5
* clang versión 10.0.0-4
* icc 2021.1 Beta 20201112

### Sistema Operativo

* Sistema operativo: Linux Mint 20.1
* Kernel: Linux 5.8.0-48-generic
* Arquitectura: x86_64

## Conclusiones
