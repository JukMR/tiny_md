import matplotlib.pyplot as plt

# zx81

## Arch_75
# N_zx81 = [32, 108, 256, 500, 864, 1372, 2048, 2916, 4000, 5324, 6912, 8788, 10976]

# Gflops_zx81 = [0.002823, 0.018777, 0.087077, 0.313706, 0.973503, 2.698487, 5.814254, 7.507554, 8.569062, 9.770986, 10.714135, 11.432618, 11.815259]

# Tiempos_zx81 = [ 14.655765056610107,  25.47667121887207,  30.98280954360962,  32.93618631362915,  31.744341135025024,  28.917893171310425,  29.903117656707764,  46.76183843612671,  76.85533380508423,  119.218576669693,  183.15490579605103,  277.2466459274292,  418.27004861831665,  ]


## Arch_86


Gflops_zx81 = [0.019224, 0.088958, 0.304559, 1.0375, 2.63799, 5.764343, 7.495146, 8.540188, 9.765438, 10.721222, 11.482019, 11.802614]

Tiempos_zx81 = [24.90880846977234, 30.339534282684326, 33.845720291137695, 29.716455459594727, 29.490129232406616, 30.080939292907715, 46.7613959312439, 77.0528609752655, 119.2474889755249, 182.92022109031677, 275.97991919517517, 418.69894528388977,]

N_zx81 = [108, 256, 500, 864, 1372, 2048, 2916, 4000, 5324, 6912, 8788, 10976,]



# Jupiterace

N_Jupiterace = [ 32, 108, 256, 500, 864, 1372, 2048, 2916, 4000, 5324, 6912, 8788, 10976, ]

Gflops_Jupiterace = [0.002784, 0.017792, 0.091187, 0.383666, 1.557027, 3.779965, 6.094679, 8.551947, 10.12269, 11.684155, 13.310257, 14.542133, 14.986285,]


Tiempos_Jupiterace = [ 14.872766733169556,  26.881709814071655,  29.606247663497925,  26.938557147979736,  19.87917709350586,  20.638734817504883,  28.451138019561768,  41.0087149143219,  65.06395983695984,  99.69810080528259,  147.39672684669495,  217.95303082466125,  329.8254141807556,]


### Comparacion con jupiterace grandes

jupiterace_bigN_gflops = [15.730743, 15.865341, 16.524264, 17.053843, 17.178416]

jupiterace_bigN_time = [475.2423584461212, 693.9497056007385, 958.4626290798187, 1308.554118156433, 1796.789901971817,]

jupiterace_bigN = [13500,16384,19652,23328,27436]


## New values
N_Jupiterace.extend(jupiterace_bigN)

Gflops_Jupiterace.extend(jupiterace_bigN_gflops)

Tiempos_Jupiterace.extend(jupiterace_bigN_time)


def clean(arr):
    new = []
    for i in arr:
        new.append(round(i,4))
    return new

"""
print(clean(Gflops_Jupiterace))
print(clean(Tiempos_Jupiterace))


[0.0028, 0.0178, 0.0912, 0.3837, 1.557, 3.78, 6.0947, 8.5519, 10.1227, 11.6842, 13.3103, 14.5421, 14.9863,]
[14.8728, 26.8817, 29.6062, 26.9386, 19.8792, 20.6387, 28.4511, 41.0087, 65.064, 99.6981, 147.3967, 217.953, 329.8254,]

print(clean(Gflops_zx81))
print(clean(Tiempos_zx81))

[0.0192, 0.089, 0.3046, 1.0375, 2.638, 5.7643, 7.4951, 8.5402, 9.7654, 10.7212, 11.482, 11.8026,]
[24.9088, 30.3395, 33.8457, 29.7165, 29.4901, 30.0809, 46.7614, 77.0529, 119.2475, 182.9202, 275.9799, 418.6989,]


print(clean(Gflops_Jupiterace))
print(clean(Tiempos_Jupiterace))


[0.0028, 0.0178, 0.0912, 0.3837, 1.557, 3.78, 6.0947, 8.5519, 10.1227, 11.6842, 13.3103, 14.5421, 14.9863, 15.7307, 15.8653, 16.5243, 17.0538, 17.1784,]
[14.8728, 26.8817, 29.6062, 26.9386, 19.8792, 20.6387, 28.4511, 41.0087, 65.064, 99.6981, 147.3967, 217.953, 329.8254, 475.2424, 693.9497, 958.4626, 1308.5541, 1796.7899,]

"""


## Graficos gflops, zx81 vs jupiterace
plt.figure()
plt.title("Gflops, Jupiterace vs zx81")
plt.xlabel("N particulas")
plt.ylabel("GFLOPS")
plt.xticks(N_Jupiterace, rotation=75)
plt.scatter(N_Jupiterace, Gflops_Jupiterace, color='blue', s=20, marker='o', label="Jupiterace, GeForce RTX 2080 Ti")
plt.scatter(N_zx81, Gflops_zx81, color='red', s=20, marker='o', label=" zx81, GeForce RTX 3070")
plt.legend(loc='best')

plt.gcf().subplots_adjust(bottom=0.18)
plt.savefig("figures/jupiterace_zx81_gflops.png")
plt.show()



## Graficos segundos, zx81 vs jupiterace
plt.figure()
plt.title("Segundos, Jupiterace vs zx81")
plt.xlabel("N particulas")
plt.ylabel("Segundos")

plt.xticks(N_Jupiterace, rotation=75)
plt.scatter(N_Jupiterace, Tiempos_Jupiterace, color='blue', s=20, marker='o', label="Jupiterace, GeForce RTX 2080 Ti")
plt.scatter(N_zx81, Tiempos_zx81, color='red', s=20, marker='o', label=" zx81, GeForce RTX 3070")
plt.legend(loc='best')

plt.gcf().subplots_adjust(bottom=0.18)
plt.savefig("figures/jupiterace_zx81_segundos.png")
plt.show()




## Comparacion de labs

## Gflops para distintos N, GeForce RTX 2080 Ti, Jupiterace

lab3 = [4.342344, 6.32942, 7.582048, 8.336292, 9.411485, 10.254995, 10.738638, 11.130083, 11.588606, 11.865144]

N_lab3 = [500, 864, 1372, 2048, 2916, 4000, 5324, 6912, 8788, 10976,]



plt.figure()
plt.title("GFLOPS, distintos N contra Lab3, GeForce RTX 2080 Ti")
plt.xlabel("N particulas")
plt.ylabel("GFLOPS")
plt.xticks(N_Jupiterace, rotation=75)
plt.scatter(N_Jupiterace, Gflops_Jupiterace, color='blue', s=25, marker='o', label="Lab4")
plt.scatter(N_lab3, lab3, color='green', s=25, marker='o', label="Lab3")

plt.legend(loc='best')
plt.gcf().subplots_adjust(bottom=0.18)
plt.savefig("figures/lab3_vs_lab4_many_N_jupiterace.png")
plt.show()


## Gflops para distintos N, GeForce RTX 3070, zx81

lab3 = [4.342344, 6.32942, 7.582048, 8.336292, 9.411485, 10.254995, 10.738638, 11.130083, 11.588606, 11.865144]

N_lab3 = [500, 864, 1372, 2048, 2916, 4000, 5324, 6912, 8788, 10976,]



plt.figure()
plt.title("GFLOPS, distintos N contra Lab3, GeForce RTX 3070")
plt.xlabel("N particulas")
plt.ylabel("GFLOPS")
plt.xticks(N_zx81, rotation=75)
plt.scatter(N_zx81, Gflops_zx81, color='red', s=25, marker='o', label="Lab4")
plt.scatter(N_lab3, lab3, color='green', s=25, marker='o', label="Lab3")

plt.legend(loc='best')
plt.gcf().subplots_adjust(bottom=0.18)
plt.savefig("figures/lab3_vs_lab4_many_N_zx81.png")
plt.show()



## A partir de estos valores, vemos que jupiterace da mejor, tomamos esta mejor metrica

## Comparación lab3 vs lab4, cualquier N


labs = ["Lab3", "Lab4"]
best_gflops = [11.865, 14.986285]
plt.figure()
plt.title("Mejor métrica, Lab3 vs Lab4, mejor tamaño N")
plt.xlabel("Lab")
plt.ylabel("GFLOPS")
# plt.xticks(labs)
plt.yticks(best_gflops)
plt.bar(labs, best_gflops, color='orange', edgecolor='black')

plt.gcf().subplots_adjust(bottom=0.18)
plt.savefig("figures/lab3_vs_lab4_bestN.png")
plt.show()


## Comparación 4 laboratorios, cualquier N


labs = ["Lab1", "Lab2", "Lab3", "Lab4 N=10976", "Lab4 N=27436"]
best_gflops = [0.45, 0.8, 11.865, 14.986285, 17.178416]
plt.figure()
plt.title("Mejor métrica, todos los Labs, mejor tamaño N")
plt.xlabel("Lab")
plt.ylabel("GFLOPS")
plt.xticks(rotation=30)
plt.yticks(best_gflops)
plt.bar(labs, best_gflops, color='orange', edgecolor='black')

plt.gcf().subplots_adjust(bottom=0.2)
plt.savefig("figures/best_everyLab_bestN.png")
plt.show()

# Comparación lab3 vs lab4, N=500

labs = ["Lab3", "Lab4"]
best_gflops = [4.67, 0.383666]
plt.figure()
plt.title("Mejor métrica, Lab 3 vs Lab4, N=500")
plt.xlabel("Lab")
plt.ylabel("GFLOPS")
# plt.xticks()
plt.yticks(best_gflops)
plt.bar(labs, best_gflops, color='cyan', edgecolor='black')

plt.gcf().subplots_adjust(bottom=0.18)
plt.savefig("figures/best_lab3_vs_lab4_N500.png")
plt.show()

# Comparación todos labs, N=500

labs = ["Lab1", "Lab2", "Lab3", "Lab4"]

best_gflops = [0.45, 0.8, 4.67, 0.383666]
plt.figure()
plt.title("Mejor métrica, entre todos los labs, N=500")
plt.xlabel("Lab")
plt.ylabel("GFLOPS")
# plt.xticks(labs)
plt.yticks(best_gflops)
plt.bar(labs, best_gflops, color='cyan', edgecolor='black')

plt.gcf().subplots_adjust(bottom=0.18)
plt.savefig("figures/best_everyLab_N500.png")
plt.show()




### Jupiterace double vs float



Gflops_float = [0.002325, 0.016338, 0.071136, 0.309985, 1.11167, 2.285082, 7.015613, 11.063674, 15.386182, 19.487224, 23.109405, 26.549488, 26.823764, 30.295779, 31.772447, 32.445573, 33.613654, 34.797433, 35.688186, 36.169114]

Tiempos_float = [17.794772386550903, 29.225499629974365, 37.87234401702881, 33.24780607223511, 27.756632804870605, 34.09491539001465, 24.672178745269775, 31.71737766265869, 42.845136880874634, 59.86936616897583, 84.99781537055969, 119.41193199157715, 184.43875241279602, 246.86163663864136, 346.64623737335205, 488.29682445526123, 664.0148515701294, 887.1017236709595, 1176.6020891666412, 1555.8628797531128, ]

N_float = [32, 108, 256, 500, 864, 1372, 2048, 2916, 4000, 5324, 6912, 8788, 10976, 13500, 16384, 19652, 23328, 27436, 32000, 37044]



## Float vs double, gflops
plt.figure()
plt.title("GFLOPS, Precision simple vs Precision doble")

plt.xlabel("N particulas")
plt.ylabel("GFLOPS")
plt.xticks(N_float, rotation=75)
plt.scatter(N_Jupiterace, Gflops_Jupiterace, color='blue', s=20, marker='o', label="Double")
plt.scatter(N_float, Gflops_float, color='purple', s=20, marker='o', label="Float")
plt.legend(loc='best')

plt.gcf().subplots_adjust(bottom=0.18)
plt.savefig("figures/double_vs_float_gflops.png")
plt.show()



## Float vs double, tiempos
plt.figure()
plt.title("Segundos, Precision simple vs Precision doble")
plt.xlabel("N particulas")
plt.ylabel("Segundos")

plt.xticks(N_float, rotation=75)
plt.scatter(N_Jupiterace, Tiempos_Jupiterace, color='blue', s=20, marker='o', label="Double")
plt.scatter(N_float, Tiempos_float, color='purple', s=20, marker='o', label="Float")
plt.legend(loc='upper left')

plt.gcf().subplots_adjust(bottom=0.18)
plt.savefig("figures/double_vs_float_time.png")
plt.show()

