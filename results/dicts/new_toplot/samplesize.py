import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


def gaussian(x, mu, sig):
    return np.exp(-np.power((x - mu)/sig, 2.)/2)


with open('samplesize.plot') as f:
    header = next(f)
    print(header)
    numlines = 0
    gflops = []
    cflags = []
    times = []
    timeserr = []
    gflopserr = []
    for line in f:
        # spliteo con ',' y borro espacios en blanco
        v = [x.strip() for x in line.split(',')]
        # v = line.split(',') # old 
        print(v[0], v[1], v[2], v[3],v[4])
        cflags.append(v[0])
        times.append(float(v[1]))
        timeserr.append(float(v[2]))
        gflops.append(float(v[3]))
        gflopserr.append(float(v[4]))
        numlines = numlines + 1



# AHORA VAMOS A GRAFICAR LOS TIEMPOS
fig, (ax1,ax2) = plt.subplots(2,1,sharex='col')   # creamos nueva fig
y_pos = np.arange(numlines)
ax1.bar(y_pos, times, yerr=timeserr, align='center',
        alpha=1.0, ecolor='orange',
        error_kw=dict(lw=5, capsize=14.7, capthick=3))
plt.subplots_adjust(bottom=0.5, top=0.9)
# Create names on the x-axis
plt.xticks(y_pos, cflags, rotation=90)
# Show graphic
ax1.set_title('Tiempos y GFLOPS para diferentes tamaños de muestra')
ax1.set_ylabel('tiempo (seg)')

# AHORA VAMOS A GRAFICAR LOS GFLOPS
#plt.figure(2)   # creamos nueva fig
#y_pos = np.arange(numlines)
plt.bar(y_pos, gflops, yerr=gflopserr, align='center',
        alpha=1.0, ecolor='orange',
        error_kw=dict(lw=5, capsize=14.7, capthick=3))
plt.subplots_adjust(bottom=0.5, top=0.9)
# Create names on the x-axis
plt.xticks(y_pos, cflags, rotation=90)
# Show graphic
#plt.title('Comparación de GFLOPS para diferentes CFLAGS. Compilador gcc 9.4')
ax2.set_xlabel('CFLAGS')
ax2.set_ylabel('GFLOPS')
plt.show()



