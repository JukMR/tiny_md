#include "core.h"
#include "parameters.h"

#include <math.h>
#include <stdlib.h> // rand()

#define ECUT (4.0 * (pow(RCUT, -12) - pow(RCUT, -6)))


void init_pos(double* rx,double* ry,double* rz, const double rho)
{
    // inicialización de las posiciones de los átomos en un cristal FCC

    double a = cbrt(4.0 / rho); // cbrt=cube root
    int nucells = ceil(cbrt((double)N / 4.0));
    int idx = 0;

    for (int i = 0; i < nucells; i++) {
        for (int j = 0; j < nucells; j++) {
            for (int k = 0; k < nucells; k++) {
                rx[idx] = i * a; // x
                ry[idx] = j * a; // y
                rz[idx] = k * a; // z
                    // del mismo átomo
                rx[idx + 1] = (i + 0.5) * a;
                ry[idx + 1] = (j + 0.5) * a;
                rz[idx + 1] = k * a;

                rx[idx + 2] = (i + 0.5) * a;
                ry[idx + 2] = j * a;
                rz[idx + 2] = (k + 0.5) * a;

                rx[idx + 3] = i * a;
                ry[idx + 3] = (j + 0.5) * a;
                rz[idx + 3] = (k + 0.5) * a;

                idx += 4;
            }
        }
    }
}


void init_vel(double* vx,double* vy,double* vz, double* temp, double* ekin)
{
    // inicialización de velocidades aleatorias

    double sf, sumvx = 0.0, sumvy = 0.0, sumvz = 0.0, sumv2 = 0.0;

    for (int i = 0; i < N; i++) {
        vx[i] = rand() / (double)RAND_MAX - 0.5;
        vy[i] = rand() / (double)RAND_MAX - 0.5;
        vz[i] = rand() / (double)RAND_MAX - 0.5;

        sumvx += vx[i];
        sumvy += vy[i];
        sumvz += vz[i];
        sumv2 += vx[i] * vx[i] + vy[i] * vy[i] + vz[i] * vz[i];
    }

    sumvx /= (double)N;
    sumvy /= (double)N;
    sumvz /= (double)N;
    *temp = sumv2 / (3.0 * N);
    *ekin = 0.5 * sumv2;
    sf = sqrt(T0 / *temp);

    for (int i = 0; i < N; i++) { // elimina la velocidad del centro de masa
        // y ajusta la temperatura
        vx[i] = (vx[i] - sumvx) * sf;
        vy[i] = (vy[i] - sumvy) * sf;
        vz[i] = (vz[i] - sumvz) * sf;
    }
}


static double minimum_image(double cordi, const double cell_length)
{
    // imagen más cercana

    if (cordi <= -0.5 * cell_length) {
        cordi += cell_length;
    } else if (cordi > 0.5 * cell_length) {
        cordi -= cell_length;
    }
    return cordi;
}


void forces(const double* rx,const double* ry,const double* rz, double* fx,double* fy,double* fz, double* epot, double* pres,
            const double* temp, const double rho, const double V, const double L)
{
    // calcula las fuerzas LJ (12-6)

    for (int i = 0; i <  N; i++) {
        fx[i] = 0.0;
        fy[i] = 0.0;
        fz[i] = 0.0;
    }
    double pres_vir = 0.0;
    double rcut2 = RCUT * RCUT; // mult
    *epot = 0.0;

    // (N - 1) iteraciones
    for (int i = 0; i < (N - 1); i++) {

        double xi = rx[i];
        double yi = ry[i];
        double zi = rz[i];

        // (N - i - 1)  iteraciones
        for (int j = i + 1; j <  N; j++) {

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

            double xj = rx[j];
            double yj = ry[j];
            double zj = rz[j];

            // distancia mínima entre r_i y r_j
            double rx = xi - xj;                    // resta
            rx = minimum_image(rx, L);              // mult suma
            double ry = yi - yj;                    // resta
            ry = minimum_image(ry, L);              // mult suma
            double rz = zi - zj;                    // resta
            rz = minimum_image(rz, L);              // mult suma

            double rij2 = rx * rx + ry * ry + rz * rz; // mult mult mult suma suma

            if (rij2 <= rcut2) {
                double r2inv = 1.0 / rij2;  // div
                double r6inv = r2inv * r2inv * r2inv; // mult mult

                double fr = 24.0 * r2inv * r6inv * (2.0 * r6inv - 1.0); // mult mult mult mult resta

                fx[i] += fr * rx; // mult suma
                fy[i] += fr * ry; // mult suma
                fz[i] += fr * rz; // mult suma

                fx[j] -= fr * rx; // mult resta
                fy[j] -= fr * ry; // mult resta
                fz[j] -= fr * rz; // mult resta

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


void velocity_verlet(double* rx,double* ry,double* rz,double* vx,double* vy,double* vz, 
                     double* fx,double* fy,double* fz,double* epot,
                     double* ekin, double* pres, double* temp, const double rho,
                     const double V, const double L)
{

    for (int i = 0; i < N; i++) { // actualizo posiciones
        rx[i] += vx[i] * DT + 0.5 * fx[i] * DT * DT;
        ry[i] += vy[i] * DT + 0.5 * fy[i] * DT * DT;
        rz[i] += vz[i] * DT + 0.5 * fz[i] * DT * DT;

        rx[i] = pbc(rx[i], L);
        ry[i] = pbc(ry[i], L);
        rz[i] = pbc(rz[i], L);

        vx[i] += 0.5 * fx[i] * DT;
        vy[i] += 0.5 * fy[i] * DT;
        vz[i] += 0.5 * fz[i] * DT;
    }

    forces(rx,ry,rz, fx,fy,fz, epot, pres, temp, rho, V, L); // actualizo fuerzas

    double sumv2 = 0.0;
    for (int i = 0; i < N; i++) { // actualizo velocidades
        vx[i] += 0.5 * fx[i] * DT;
        vy[i] += 0.5 * fy[i] * DT;
        vz[i] += 0.5 * fz[i] * DT;

        sumv2 += vx[i] * vx[i] + vy[i] * vy[i]+ vz[i] * vz[i];
    }

    *ekin = 0.5 * sumv2;
    *temp = sumv2 / (3.0 * N);
}
