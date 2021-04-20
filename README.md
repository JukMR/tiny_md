# tiny_md

> _tiny molecular dynamics_

Proyecto inicial para realizar speed-up de un código de Dinámica Molecular con
un potencial interatómico de Lennard-Jones. Inicialmente se dan las posiciones
en un cristal FCC y velocidades aleatorias distribuidas uniformemente según la
temperatura inicial. Las fuerzas se obtienen de un potencial de LJ (12-6) y la
evolución temporal viene dada por el algoritmo Velocity Verlet. Se consideran
condiciones periódicas de contorno para reproducir un sistema infinito. La
temperatura es controlada a través de un reescaleo en las velocidades. Cada
cierta cantidad de pasos de dinámica molecular se cambia la densidad del sistema
y se reescalean las posiciones para obtener la ecuación de estado. Para más
información se puede ver `doc/informe.pdf`.


### Requisitos

Para compilar es necesario tener instalado `gcc` y `OpenGL`.


### Compilación

Para compilar se utiliza `Makefile`:
```bash
make clean
make
```

donde `make clean` elimina los objetos compilados anteriormente y `make` compila
dos ejecutables: `tiny_md` y `viz`, ambos realizan la misma simulación pero el
segundo posee una visualización en tiempo real.

> Nota:
>
> _Si se desean cambiar parámetros de entrada de la simulación, puede modificarse
> el archivo _`parameters.h`_ o pasar los valores deseados como parámetros al
> preprocesador C; por ejemplo, _`make CPPFLAGS="-DN=1372"`_ cambia la cantidad de
> partículas que se simulan._


### Contacto
Por errores, preguntas o sugerencias contactarse con:
+ Francisco Fernandez (<fernandezfrancisco2195@gmail.com>)



### Comentarios y Resultados con 1 único core (Versión 0 del código por defecto)
+ profiling con perf --> forces:53,86% | minimum_image:44,13%
+ En forces se hacen (N * (N - 1 ) * 0.5 ) * 41 + 5  operaciones con punto
  flotante(es decir del orden O(N)=N^2)
+ Con un procesador AMD, el uso del compilador de intel icc dio más lento que gcc
+ Al agrandar de un tamaño 256 a 512 mejoró los GFlops, pero con 1024 empeoró.
  Pensamos que esto pasa porque la caché se queda sin espacio y se necesita
  consultar a memoria cuando el tamaño aumenta.
 
 ### Algunas pruebas para empezar a optimizar el código
+ Probamos de modificar las expresiones en forces para multiplicar todo y en el paso final
  dividir (ganamos menos de 1% de tiempo, no valió la pena)
+ Probamos de utilizar una función de potencia supuestamente más optimizada pero no pudimos sacar
  más velocidad
+ Probamos de cambiar los double por float y corre en la mitad de tiempo, pero hay que revisar
  porque cambiaron los valores
