import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import pandas as pd
from matplotlib.font_manager import FontProperties

fontP = FontProperties()
fontP.set_size('xx-small')

def gaussian(x, mu, sig):
    return np.exp(-np.power((x - mu)/sig, 2.)/2)


with open('tp2original.data') as f:
    header = next(f)
    print(header)
    numlines = 0
    gflopsoriginal = []
    cflagsoriginal = []
    timesoriginal = []
    timeserroriginal = []
    #gflopserroriginal = []
    insnoriginal = []
    for line in f:
        # spliteo con ',' y borro espacios en blanco
        voriginal = [x.strip() for x in line.split(',')]
        # v = line.split(',') # old 
        print(voriginal[0], voriginal[1], voriginal[2], voriginal[3],voriginal[4])
        cflagsoriginal.append(voriginal[0])
        timesoriginal.append(float(voriginal[1]))
        timeserroriginal.append(float(voriginal[2]))
        gflopsoriginal.append(float(voriginal[3]))
        insnoriginal.append(float(voriginal[4]))
        numlines = numlines + 1

with open('tp2SoA.data') as f:
    header = next(f)
    print(header)
    numlines = 0
    gflopsSoA = []
    cflagsSoA = []
    timesSoA = []
    timeserrSoA = []
    #gflopserrSoA = []
    insnSoA = []
    for line in f:
        # spliteo con ',' y borro espacios en blanco
        vSoA = [x.strip() for x in line.split(',')]
        # v = line.split(',') # old 
        #print(v[0], v[1], v[2], v[3],v[4])
        cflagsSoA.append(vSoA[0])
        timesSoA.append(float(vSoA[1]))
        timeserrSoA.append(float(vSoA[2]))
        gflopsSoA.append(float(vSoA[3]))
        insnSoA.append(float(vSoA[4]))
        numlines = numlines + 1

with open('tp2ispc.data') as f:
    header = next(f)
    print(header)
    numlines = 0
    gflopsispc = []
    cflagsispc = []
    timesispc = []
    timeserrispc = []
    #gflopserrispc = []
    insnispc = []
    for line in f:
        # spliteo con ',' y borro espacios en blanco
        vispc = [x.strip() for x in line.split(',')]
        # v = line.split(',') # old 
        #print(v[0], v[1], v[2], v[3],v[4])
        cflagsispc.append(vispc[0])
        timesispc.append(float(vispc[1]))
        timeserrispc.append(float(vispc[2]))
        gflopsispc.append(float(vispc[3]))
        insnispc.append(float(vispc[4]))
        numlines = numlines + 1


# AHORA VAMOS A GRAFICAR LOS TIEMPOS
fig, (ax1,ax2,ax3) = plt.subplots(3,1,sharex='col')   # creamos nueva fig
y_pos = np.arange(numlines)
ax1.bar(y_pos, timesoriginal, yerr=timeserroriginal, align='center',
        alpha=1.0, ecolor='orange',
        error_kw=dict(lw=5, capsize=14.7, capthick=3))
plt.subplots_adjust(bottom=0.5, top=0.9)
# Create names on the x-axis
plt.xticks(y_pos, cflagsoriginal, rotation=90)
# Show graphic
ax1.set_title('Tiempos y GFLOPS para diferentes CFLAGS y compiladores')
ax1.set_ylabel('tiempo (seg)')

# AHORA VAMOS A GRAFICAR LOS GFLOPS
#plt.figure(2)   # creamos nueva fig
#y_pos = np.arange(numlines)
ax2.bar(y_pos, gflopsoriginal, align='center',
        alpha=1.0)
#plt.subplots_adjust(bottom=0.5, top=0.9)
# Create names on the x-axis
#plt.xticks(y_pos, cflagsoriginal, rotation=90)
# Show graphic
#plt.title('Comparación de GFLOPS para diferentes CFLAGS. Compilador gcc 9.4')
#ax2.set_xlabel('CFLAGS')
ax2.set_ylabel('GFLOPS')


# AHORA VAMOS A GRAFICAR EL insn
#plt.figure(2)   # creamos nueva fig
#y_pos = np.arange(numlines)
ax3.bar(y_pos, insnoriginal, align='center',
        alpha=1.0)
#plt.subplots_adjust(bottom=0.5, top=0.9)
# Create names on the x-axis
plt.xticks(y_pos, cflagsoriginal, rotation=90)
# Show graphic
#plt.title('Comparación de GFLOPS para diferentes CFLAGS. Compilador gcc 9.4')
ax3.set_xlabel('CFLAGS')
ax3.set_ylabel('insn')
plt.show()


#plt.figure()
fig, (eje1,eje2,eje3) = plt.subplots(3,1,sharex='col')
plt.subplots_adjust(wspace=0, hspace=0)
df1 = pd.DataFrame([['original',timesoriginal[0],timesoriginal[1],timesoriginal[2],timesoriginal[3]],
                   ['SoA',timesSoA[0],timesSoA[1],timesSoA[2],timesSoA[3]],
                   ['ispc',timesispc[0],timesispc[1],timesispc[2],timesispc[3]]],
                  columns=['cflags',cflagsoriginal[0], cflagsoriginal[1], cflagsoriginal[2],cflagsoriginal[3]])
# view data
ejes1 = df1.plot(x='cflags', ax=eje1, 
        kind='bar',
        stacked=False)#,
       # title='Comparación diferentes')
ejes1.set_ylabel('elapsed time (s)')
ejes1.legend(loc='upper right',prop=fontP)

df2 = pd.DataFrame([['original',gflopsoriginal[0],gflopsoriginal[1],gflopsoriginal[2],gflopsoriginal[3]],
                   ['SoA',gflopsSoA[0],gflopsSoA[1],gflopsSoA[2],gflopsSoA[3]],
                   ['ispc',gflopsispc[0],gflopsispc[1],gflopsispc[2],gflopsispc[3]]],
                  columns=['cflags',cflagsoriginal[0], cflagsoriginal[1], cflagsoriginal[2],cflagsoriginal[3]])
# view data
ejes2 = df2.plot(x='cflags',ax=eje2, legend=False,
        kind='bar',
        stacked=False)
ejes2.set_ylabel('GFLOPs')



df2 = pd.DataFrame([['orig',gflopsoriginal[0],gflopsoriginal[1],gflopsoriginal[2],gflopsoriginal[3]],
                   ['SoA',gflopsSoA[0],gflopsSoA[1],gflopsSoA[2],gflopsSoA[3]],
                   ['ispc',gflopsispc[0],gflopsispc[1],gflopsispc[2],gflopsispc[3]]],
                  columns=['',cflagsoriginal[0], cflagsoriginal[1], cflagsoriginal[2],cflagsoriginal[3]])
# view data
ejes3 = df2.plot(x='',ax=eje3, legend=False,
        kind='bar',
        stacked=False)
ejes3.set_ylabel('insn')
#plt.savefig('foo.png')
#plt.savefig('foo.pdf')