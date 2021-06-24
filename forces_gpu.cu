// Variables necesarias

// #include <cuda.h> // no se porque esto rompe todo

#include <cuda_runtime.h>
#include "helper_cuda.h" // checkCudaError
#include "parameters.h"
#include <cstdio>
// #include <cuda.h>

// #include <cub/cub.cuh>



//#define ECUT (4.0 * (pow(RCUT, -12) - pow(RCUT, -6)))

__device__ void minimum_image(float cordi, const float cell_length, float* result)
{
    // imagen más cercana
    if (cordi <= -0.5 * cell_length) {
        cordi += cell_length;
    } else if (cordi > 0.5 * cell_length) {
        cordi -= cell_length;
    }

    *result = cordi;
}

// Esta función esta sacada de la wiki de Cuda. capaz sirve.


// __device__ double atomicAdd(double* address, double val)
// {
//     unsigned long long int* address_as_ull =
//                              (unsigned long long int*)address;
//     unsigned long long int old = *address_as_ull, assumed;
//     do {
//         assumed = old;
// old = atomicCAS(address_as_ull, assumed,
//                         __double_as_longlong(val +
//                                __longlong_as_double(assumed)));
//     } while (assumed != old);
//     return __longlong_as_double(old);
// }


__device__ double atomicAdd2(double* address, double val) {
unsigned long long int* address_as_ull = (unsigned long long int*)address;
unsigned long long int old = *address_as_ull, assumed;

            do {
                  assumed = old;
                  old = atomicCAS(address_as_ull, assumed, __double_as_longlong(val+__longlong_as_double(assumed)));
           } while (assumed != old);
           return __longlong_as_double(old);
}

// Algo asi capaz si se podria implementar para la reduccion con floats.


// __global__ void sum_shared_atomic(const int *in, int n, int *out)
// {
//     __shared__ int partial_sum;

//     uint i = blockIdx.x * blockDim.x + threadIdx.x;

//     if (threadIdx.x == 0) {
//         partial_sum = 0;
//     }

//     __syncthreads();

//     if (i < n) {
//         atomicAdd(&partial_sum, in[i]);
//     }

//     __syncthreads();

//     if (threadIdx.x == 0) {
//         atomicAdd(out, partial_sum);
//     }
// }



__global__ void forces(const float* rx,
                       const float* ry,
                       const float* rz,
                       float* fx,
                       float* fy,
                       float* fz,
                       float* epot,
                       float* pres,
                       const float* temp,
                       const float rho,
                       const float V,
                       const float L)
{

    for (uint row = 0; row < N-1; row++){

    float rcut2 = RCUT * RCUT;
    const float RCUT12 = RCUT * RCUT * RCUT * RCUT * RCUT * RCUT * RCUT * RCUT * RCUT * RCUT * RCUT * RCUT;

    const float RCUT6 = RCUT * RCUT * RCUT * RCUT * RCUT * RCUT;
    const float ECUT = 4.0 * (1 / (RCUT12)-1 / (RCUT6));
    // //#define ECUT (4.0 * (pow(RCUT, -12) - pow(RCUT, -6)))

    float fxi = 0.0;
    float fyi = 0.0;
    float fzi = 0.0;
    float epot_partial = 0.0;
    float pres_vir_partial = 0.0;

	unsigned int j = blockIdx.x*blockDim.x + threadIdx.x;

        if (j != row) {
            float xi = rx[row];
            float yi = ry[row];
            float zi = rz[row];

            float xj = rx[j];
            float yj = ry[j];
            float zj = rz[j];

            float rxd = xi - xj;
            float ryd = yi - yj;
            float rzd = zi - zj;

            minimum_image(rxd, L, &rxd);
            minimum_image(ryd, L, &ryd);
            minimum_image(rzd, L, &rzd);

            float rij2 = rxd * rxd + ryd * ryd + rzd * rzd;

            if (rij2 <= rcut2) {
                float r2inv = 1.0 / rij2;
                float r6inv = r2inv * r2inv * r2inv;

                float fr = 24.0 * r2inv * r6inv * (2.0 * r6inv - 1.0);

                fxi += fr * rxd;
                fyi += fr * ryd;
                fzi += fr * rzd;


                epot_partial += 4.0 * r6inv * (r6inv - 1.0) - ECUT;
                pres_vir_partial += fr * rij2;
            }
        }


    atomicAdd(&fx[row], fxi);
    atomicAdd(&fy[row], fyi);
    atomicAdd(&fz[row], fzi);

    atomicAdd(epot, epot_partial / 2);
    atomicAdd(pres, pres_vir_partial / 2 / (V * 3.0));

    // fx[row] += fxi;
    // fy[row] += fyi;
    // fz[row] += fzi;
    // *epot += epot_partial / 2;
    // *pres += pres_vir_partial / 2 / (V * 3.0);


    }
}
int div_ceil(int a, int b) {
    return (a + b - 1) / b;
}

void launch_forces(const float* rx, const float* ry, const float* rz,
                   float* fx, float* fy, float* fz, float* epot,
                   float* pres, const float* temp, const float rho,
                   const float V, const float L)
{

    // Todavía no entiendo que número de bloques y grilla nos conviene usar para el problema


    // Por ahora tomo N-1 hilos para tener un hilo por cada elemento de N
    dim3 block(N-1);

    // Por ahora la misma selección de grilla usando los ejemplos de Charly
    dim3 grid(div_ceil(N-1, block.x));


    // Este for probablemente no tendria que ir, deberiamos lanzar un kernel que haga esto según el hilo en el que esta parado



    forces <<<grid, block>>> (rx, ry, rz, fx, fy, fz, epot, pres, temp, rho, V, L);


    checkCudaError(cudaGetLastError());
    checkCudaError(cudaDeviceSynchronize());

}

