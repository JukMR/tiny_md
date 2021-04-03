#f = open('gcc.plot')
#f.readlines()
#import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
def gaussian(x, mu, sig):
    return np.exp(-np.power((x - mu)/sig, 2.)/2)
plt.figure(1)  
with open('gcc.plot') as f:
    header=next(f)
    print(header)
    numlines=0
    gflops=[]
    cflags=[]
    for line in f:
        #spliteo con ',' y borro espacios en blanco
        v = [x.strip() for x in line.split(',')]
        #v = line.split(',') #old
        print (v[0],v[1],v[2],v[3])
        gflops.append(float(v[3]))
        cflags.append(v[0])
        #fig = plt.figure()
        time=np.linspace(0, 20,10000)
        #rv = norm(loc = float(v[1]), scale = float(v[2]))
        #plt.plot(time, rv.pdf(time)	)  
        plt.plot(time,gaussian(time,float(v[1]),float(v[2])),label=v[0])
        plt.legend(loc=2, prop={'size': 6})
        numlines=numlines+1
        #plt.legend(loc="upper left")
        #, label=v[0])
plt.title('Comparación de tiempos para diferentes CFLAGS')
plt.xlabel('tiempo [s]')
plt.ylabel('distribución gaussiana (normalizada)')
plt.show()

## AHORA VAMOS A GRAFICAR LOS GFLOPS
plt.figure(2)   # creamos nueva fig
#with open('gcc.plot') as f:
#    header=next(f)
#    for line in f:
        #spliteo con ',' y borro espacios en blanco
#        v = [x.strip() for x in line.split(',')]
        #v = line.split(',') #old
        #fig = plt.figure()
        #rv = norm(loc = float(v[1]), scale = float(v[2]))
        #plt.plot(time, rv.pdf(time)	)  
bars = ('A', 'B', 'C', 'D', 'E')
y_pos = np.arange(numlines)
plt.bar(y_pos, gflops)
plt.subplots_adjust(bottom=0.5, top=0.9)
        # Create names on the x-axis
plt.xticks(y_pos, cflags,rotation=90)
        
        # Show graphic
plt.title('Comparación de GFLOPS para diferentes CFLAGS')
plt.xlabel('CFLAGS')
plt.ylabel('GFLOPS')
plt.show()





        #oCFLAG = res[0]
        #otime = res[1]
#	otimedev= res[2]
#	oGFLOPS=res[3]
        #print (oCFLAG, otime)
#        print (oCFLAG, otime,otimedev,oGFLOPS)
