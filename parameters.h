/*
 * Tiny Molecular Dynamics
 *
 * Unidades: Lennard-Jones
 *
 */

#ifndef PARAMETERS_H
#define PARAMETERS_H

#include <time.h> // time(NULL)


// Esta macro tambien esta definida en forces.ispc
#ifndef N // número de particulas (debe ser un 4m^3 para el cristal inicial)
#define N 256
#endif

#ifndef SEED // rand SEED para las velocidades
#define SEED (time(NULL))
#endif

#ifndef T0 // isoterma
#define T0 2.0
#endif

#ifndef RHOI // densidad inicial
#define RHOI 1.2
#endif

// Esta macro tambien esta definida en forces.ispc
#ifndef RCUT // radio de corte
#define RCUT 2.5
#endif

#ifndef DT // paso temporal ~ 1.6 fs para el Ar
#define DT 0.005
#endif

#ifndef TEQ // pasos de equilibracion
#define TEQ 500
#endif

#ifndef TRUN // TRUN - TEQ: pasos de medicion
#define TRUN 2000
#endif

#ifndef TMES // cada cuantos pasos se mide
#define TMES 10
#endif

#endif
