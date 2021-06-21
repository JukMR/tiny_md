// Variables necesarias

// #include <cuda.h> // no se porque esto rompe todo

#include <cuda_runtime.h>
#include "helper_cuda.h" // checkCudaCall
#include "parameters.h"
#include <cstdio>
#include <cuda.h>

// #include <cub/cub.cuh>



//#define ECUT (4.0 * (pow(RCUT, -12) - pow(RCUT, -6)))

__device__ void minimum_image(double cordi, const double cell_length, double* result)
{
    // imagen más cercana
    if (cordi <= -0.5 * cell_length) {
        cordi += cell_length;
    } else if (cordi > 0.5 * cell_length) {
        cordi -= cell_length;
    }

    *result = cordi;
}


__global__ void forces(const double* rx,
                       const double* ry,
                       const double* rz,
                       double* fx,
                       double* fy,
                       double* fz,
                       double* epot,
                       double* pres,
                       const double* temp,
                       const double rho,
                       const double V,
                       const double L,
                       const int row)
{

    //        fx[row] = 0.0d;
    //        fy[row] = 0.0d;
    //        fz[row] = 0.0d;

    //    *epot = 0.0;
    double rcut2 = RCUT * RCUT;
    const double RCUT12 = RCUT * RCUT * RCUT * RCUT * RCUT * RCUT * RCUT * RCUT * RCUT * RCUT * RCUT * RCUT;

    const double RCUT6 = RCUT * RCUT * RCUT * RCUT * RCUT * RCUT;
    const double ECUT = 4.0 * (1 / (RCUT12)-1 / (RCUT6));
    // //#define ECUT (4.0 * (pow(RCUT, -12) - pow(RCUT, -6)))

    double fxi = 0.0;
    double fyi = 0.0;
    double fzi = 0.0;
    double epot_partial = 0.0;
    double pres_vir_partial = 0.0;

    for (int j = 0; j < (N - 1); j++) {
        if (j != row) {
            double xi = rx[row];
            double yi = ry[row];
            double zi = rz[row];

            double xj = rx[j];
            double yj = ry[j];
            double zj = rz[j];

            double rxd = xi - xj;
            double ryd = yi - yj;
            double rzd = zi - zj;

            minimum_image(rxd, L, &rxd);
            minimum_image(ryd, L, &ryd);
            minimum_image(rzd, L, &rzd);

            double rij2 = rxd * rxd + ryd * ryd + rzd * rzd;

            if (rij2 <= rcut2) {
                double r2inv = 1.0 / rij2;
                double r6inv = r2inv * r2inv * r2inv;

                double fr = 24.0 * r2inv * r6inv * (2.0 * r6inv - 1.0);

                fxi += fr * rxd;
                fyi += fr * ryd;
                fzi += fr * rzd;


                epot_partial += 4.0 * r6inv * (r6inv - 1.0) - ECUT;
                pres_vir_partial += fr * rij2;
            }
        }
    }


    atomicAdd(&fx[row], fxi);
    atomicAdd(&fy[row], fyi);
    atomicAdd(&fz[row], fzi);

    atomicAdd(&epot, epot_partial / 2);
    atomicAdd(&pres, pres_vir_partial / 2 / (V * 3.0));

    // fx[row] += fxi;

    // fy[row] += fyi;
    // fz[row] += fzi;
    *epot += epot_partial / 2;
    *pres += pres_vir_partial / 2 / (V * 3.0);

}



void launch_forces(const double* rx, const double* ry, const double* rz,
                   double* fx, double* fy, double* fz, double* epot,
                   double* pres, const double* temp, const double rho,
                   const double V, const double L)
{

    // int block_size = N;
    // int num_blocks = N;

    dim3 block(1);
    dim3 grid(1);


    for(size_t i = 0; i < N-1; i++ ) {
    forces <<<grid, block>>> (rx, ry, rz, fx, fy, fz, epot, pres, temp, rho,
                              V, L, i);

    checkCudaCall(cudaGetLastError());
    checkCudaCall(cudaDeviceSynchronize());
    }
}

