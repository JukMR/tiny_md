#include "core.h"
#include "parameters.h"

#include <cmath>
#include <cstdlib> // rand()

#include <cuda_runtime.h>
#include "forces_gpu.h"
#include "helper_cuda.h"


void init_pos(double* rx, double* ry, double* rz, const double rho)
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


void init_vel(double* vx, double* vy, double* vz, double* temp, double* ekin)
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


void velocity_verlet(double* rx, double* ry, double* rz, double* vx,
                     double* vy, double* vz, double* fx, double* fy,
                     double* fz, double* epot, double* ekin, double* pres,
                     double* temp, const double rho, const double V,
                     const double L)
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

    for (int j = 0; j < N; j++) {
        fx[j] = 0.0;
        fy[j] = 0.0;
        fz[j] = 0.0;
    }
    *epot = 0;
    *pres = *temp * rho;
    {
            double *epot_aux;
            double *pres_aux;
            double *ptr_Temp;


            checkCudaCall(cudaMallocManaged(&epot_aux, sizeof(double *)));
            checkCudaCall(cudaMallocManaged(&pres_aux, sizeof(double *)));
            checkCudaCall(cudaMallocManaged(&ptr_Temp, sizeof(double *)));

            *epot_aux=0;
            *pres_aux=0;
            *ptr_Temp = *temp;

        // for (int i = 0; i < N - 1; i += 1) {
            launch_forces(rx, ry, rz, fx, fy, fz, epot_aux, pres_aux, ptr_Temp, rho, V, L); // actualizo fuerzas
        // }
        *epot += *epot_aux;
        *pres += *pres_aux;

        checkCudaCall(cudaFree(epot_aux));
        checkCudaCall(cudaFree(pres_aux));
        checkCudaCall(cudaFree(ptr_Temp));
    }


    double sumv2 = 0.0;
    for (int i = 0; i < N; i++) { // actualizo velocidades
        vx[i] += 0.5 * fx[i] * DT;
        vy[i] += 0.5 * fy[i] * DT;
        vz[i] += 0.5 * fz[i] * DT;

        sumv2 += vx[i] * vx[i] + vy[i] * vy[i] + vz[i] * vz[i];
    }
    *ekin = 0.5 * sumv2;
    *temp = sumv2 / (3.0 * N);
}
