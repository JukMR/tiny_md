#include "core.h"
#include "parameters.h"

#include <math.h>
#include <stdlib.h> // rand()

#define ECUT (4.0 * (pow(RCUT, -12) - pow(RCUT, -6)))


void init_pos(double* rxyz, const double rho)
{
    // inicialización de las posiciones de los átomos en un cristal FCC

    double a = cbrt(4.0 / rho); // cbrt=cube root
    int nucells = ceil(cbrt((double)N / 4.0));
    int idx = 0;

    for (int i = 0; i < nucells; i++) {
        for (int j = 0; j < nucells; j++) {
            for (int k = 0; k < nucells; k++) {
                rxyz[idx + 0] = i * a; // x
                rxyz[idx + 1] = j * a; // y
                rxyz[idx + 2] = k * a; // z
                    // del mismo átomo
                rxyz[idx + 3] = (i + 0.5) * a;
                rxyz[idx + 4] = (j + 0.5) * a;
                rxyz[idx + 5] = k * a;

                rxyz[idx + 6] = (i + 0.5) * a;
                rxyz[idx + 7] = j * a;
                rxyz[idx + 8] = (k + 0.5) * a;

                rxyz[idx + 9] = i * a;
                rxyz[idx + 10] = (j + 0.5) * a;
                rxyz[idx + 11] = (k + 0.5) * a;

                idx += 12;
            }
        }
    }
}


void init_vel(double* vxyz, double* temp, double* ekin)
{
    // inicialización de velocidades aleatorias

    double sf, sumvx = 0.0, sumvy = 0.0, sumvz = 0.0, sumv2 = 0.0;

    for (int i = 0; i < 3 * N; i += 3) {
        vxyz[i + 0] = rand() / (double)RAND_MAX - 0.5;
        vxyz[i + 1] = rand() / (double)RAND_MAX - 0.5;
        vxyz[i + 2] = rand() / (double)RAND_MAX - 0.5;

        sumvx += vxyz[i + 0];
        sumvy += vxyz[i + 1];
        sumvz += vxyz[i + 2];
        sumv2 += vxyz[i + 0] * vxyz[i + 0] + vxyz[i + 1] * vxyz[i + 1]
               + vxyz[i + 2] * vxyz[i + 2];
    }

    sumvx /= (double)N;
    sumvy /= (double)N;
    sumvz /= (double)N;
    *temp = sumv2 / (3.0 * N);
    *ekin = 0.5 * sumv2;
    sf = sqrt(T0 / *temp);

    for (int i = 0; i < 3 * N; i += 3) { // elimina la velocidad del centro de masa
        // y ajusta la temperatura
        vxyz[i + 0] = (vxyz[i + 0] - sumvx) * sf;
        vxyz[i + 1] = (vxyz[i + 1] - sumvy) * sf;
        vxyz[i + 2] = (vxyz[i + 2] - sumvz) * sf;
    }
}



static struct Coord minimum_image(struct Coord fix,  const double cell_length)
{
    // imagen más cercana

    if (fix.rx <= -0.5 * cell_length) {
        fix.rx += cell_length;
    } else if (fix.rx > 0.5 * cell_length) {
        fix.rx -= cell_length;
    }
    if (fix.ry <= -0.5 * cell_length) {
        fix.ry += cell_length;
    } else if (fix.ry > 0.5 * cell_length) {
        fix.ry -= cell_length;
    }
    if (fix.rz <= -0.5 * cell_length) {
        fix.rz += cell_length;
    } else if (fix.rz > 0.5 * cell_length) {
        fix.rz -= cell_length;
    }

    return fix;
}


void forces(const double* rxyz, double* fxyz, double* epot, double* pres,
            const double* temp, const double rho, const double V, const double L)
{
    // calcula las fuerzas LJ (12-6)

    for (int i = 0; i < 3 * N; i++) {
        fxyz[i] = 0.0;
    }
    double pres_vir = 0.0;
    double rcut2 = RCUT * RCUT; // mult
    *epot = 0.0;

    // (N - 1) iteraciones
    for (int i = 0; i < 3 * (N - 1); i += 3) {

        double xi = rxyz[i + 0];
        double yi = rxyz[i + 1];
        double zi = rxyz[i + 2];

        // (N - i - 1)  iteraciones
        for (int j = i + 3; j < 3 * N; j += 3) {

            // Dentro del ciclo
            // 21 mult
            // 10 suma
            // 9 resta
            // 1 div
            // TOTAL 41

            // Fuera del ciclo
            // 3 mult
            // 1 div
            // 1 suma
            // TOTAL 5

            // TOTAL 21 + 10 + 9 + 1 = 41 op. flotantes
            // 41 * (N * (N - 1) / 2) + 5 operaciones por llamada forces

            double xj = rxyz[j + 0];
            double yj = rxyz[j + 1];
            double zj = rxyz[j + 2];

            struct Coord xyz;
            // distancia mínima entre r_i y r_j
            xyz.rx = xi - xj;                    // resta
            xyz.ry = yi - yj;                    // resta
            xyz.rz = zi - zj;                    // resta
            xyz = minimum_image(xyz, L);              // mult suma

            double rij2 = xyz.rx * xyz.rx + xyz.ry * xyz.ry + xyz.rz * xyz.rz; // mult mult mult suma suma

            if (rij2 <= rcut2) {
                double r2inv = 1.0 / rij2;  // div
                double r6inv = r2inv * r2inv * r2inv; // mult mult

                double fr = 24.0 * r2inv * r6inv * (2.0 * r6inv - 1.0); // mult mult mult mult resta

                fxyz[i + 0] += fr * xyz.rx; // mult suma
                fxyz[i + 1] += fr * xyz.ry; // mult suma
                fxyz[i + 2] += fr * xyz.rz; // mult suma

                fxyz[j + 0] -= fr * xyz.rx; // mult resta
                fxyz[j + 1] -= fr * xyz.ry; // mult resta
                fxyz[j + 2] -= fr * xyz.rz; // mult resta

                *epot += 4.0 * r6inv * (r6inv - 1.0) - ECUT; // mult mult resta resta suma
                pres_vir += fr * rij2; // mult suma
            }
        }
    }
    pres_vir /= (V * 3.0); // mult div
    *pres = *temp * rho + pres_vir; // mult suma
}


static double pbc(double cordi, const double cell_length)
{
    // condiciones periodicas de contorno coordenadas entre [0,L)
    if (cordi <= 0) {
        cordi += cell_length;
    } else if (cordi > cell_length) {
        cordi -= cell_length;
    }
    return cordi;
}


void velocity_verlet(double* rxyz, double* vxyz, double* fxyz, double* epot,
                     double* ekin, double* pres, double* temp, const double rho,
                     const double V, const double L)
{

    for (int i = 0; i < 3 * N; i += 3) { // actualizo posiciones
        rxyz[i + 0] += vxyz[i + 0] * DT + 0.5 * fxyz[i + 0] * DT * DT;
        rxyz[i + 1] += vxyz[i + 1] * DT + 0.5 * fxyz[i + 1] * DT * DT;
        rxyz[i + 2] += vxyz[i + 2] * DT + 0.5 * fxyz[i + 2] * DT * DT;

        rxyz[i + 0] = pbc(rxyz[i + 0], L);
        rxyz[i + 1] = pbc(rxyz[i + 1], L);
        rxyz[i + 2] = pbc(rxyz[i + 2], L);

        vxyz[i + 0] += 0.5 * fxyz[i + 0] * DT;
        vxyz[i + 1] += 0.5 * fxyz[i + 1] * DT;
        vxyz[i + 2] += 0.5 * fxyz[i + 2] * DT;
    }

    forces(rxyz, fxyz, epot, pres, temp, rho, V, L); // actualizo fuerzas

    double sumv2 = 0.0;
    for (int i = 0; i < 3 * N; i += 3) { // actualizo velocidades
        vxyz[i + 0] += 0.5 * fxyz[i + 0] * DT;
        vxyz[i + 1] += 0.5 * fxyz[i + 1] * DT;
        vxyz[i + 2] += 0.5 * fxyz[i + 2] * DT;

        sumv2 += vxyz[i + 0] * vxyz[i + 0] + vxyz[i + 1] * vxyz[i + 1]
            + vxyz[i + 2] * vxyz[i + 2];
    }

    *ekin = 0.5 * sumv2;
    *temp = sumv2 / (3.0 * N);
}
