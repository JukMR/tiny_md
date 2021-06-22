#ifndef _XOPEN_SOURCE
#define _XOPEN_SOURCE 500 // M_PI
#endif
#include "core.h"
#include "parameters.h"
#include "wtime.h"

#include <cmath>
#include <cstdio>
#include <cstdlib>

#include <cuda_runtime.h>
#include "forces_gpu.h"
#include "helper_cuda.h"

int main()
{
    FILE *file_xyz, *file_thermo;
    file_xyz = fopen("trajectory.xyz", "w");
    file_thermo = fopen("thermo.log", "w");
    float Ekin, Epot, Temp, Pres; // variables macroscopicas
    float Rho, cell_V, cell_L, tail, Etail, Ptail;
    float *rx, *ry, *rz, *vx, *vy, *vz, *fx, *fy, *fz; // variables microscopicas

    checkCudaError(cudaMallocManaged(&rx, N * sizeof(float *)));
    checkCudaError(cudaMallocManaged(&ry, N * sizeof(float *)));
    checkCudaError(cudaMallocManaged(&rz, N * sizeof(float *)));
    checkCudaError(cudaMallocManaged(&vx, N * sizeof(float *)));
    checkCudaError(cudaMallocManaged(&vy, N * sizeof(float *)));
    checkCudaError(cudaMallocManaged(&vz, N * sizeof(float *)));
    checkCudaError(cudaMallocManaged(&fx, N * sizeof(float *)));
    checkCudaError(cudaMallocManaged(&fy, N * sizeof(float *)));
    checkCudaError(cudaMallocManaged(&fz, N * sizeof(float *)));


    checkCudaError(cudaMemset(rx, 0, N * sizeof(float *)));
    checkCudaError(cudaMemset(ry, 0, N * sizeof(float *)));
    checkCudaError(cudaMemset(rz, 0, N * sizeof(float *)));
    checkCudaError(cudaMemset(vx, 0, N * sizeof(float *)));
    checkCudaError(cudaMemset(vy, 0, N * sizeof(float *)));
    checkCudaError(cudaMemset(vz, 0, N * sizeof(float *)));
    checkCudaError(cudaMemset(fx, 0, N * sizeof(float *)));
    checkCudaError(cudaMemset(fy, 0, N * sizeof(float *)));
    checkCudaError(cudaMemset(fz, 0, N * sizeof(float *)));

    // rx = (float*)malloc(N * sizeof(float));
    // ry = (float*)malloc(N * sizeof(float));
    // rz = (float*)malloc(N * sizeof(float));
    // vx = (float*)malloc(N * sizeof(float));
    // vy = (float*)malloc(N * sizeof(float));
    // vz = (float*)malloc(N * sizeof(float));
    // fx = (float*)malloc(N * sizeof(float));
    // fy = (float*)malloc(N * sizeof(float));
    // fz = (float*)malloc(N * sizeof(float));

    //    rxyz = (float*)malloc(3 * N * sizeof(float));
    //    vxyz = (float*)malloc(3 * N * sizeof(float));
    //    fxyz = (float*)malloc(3 * N * sizeof(float));

    printf("# Número de partículas:      %d\n", N);
    printf("# Temperatura de referencia: %.2f\n", T0);
    printf("# Pasos de equilibración:    %d\n", TEQ);
    printf("# Pasos de medición:         %d\n", TRUN - TEQ);
    printf("# (mediciones cada %d pasos)\n", TMES);
    printf("# densidad, volumen, energía potencial media, presión media\n");
    fprintf(file_thermo, "# t Temp Pres Epot Etot\n");

    srand(SEED);
    float t = 0.0, sf;
    float Rhob;
    Rho = RHOI;
    init_pos(rx, ry, rz, Rho);
    float start = wtime();

    // float ecut = (4.0 * (pow(RCUT, -12) - pow(RCUT, -6)));
    for (int m = 0; m < 9; m++) {
        Rhob = Rho;
        Rho = RHOI - 0.1 * (float)m;
        cell_V = (float)N / Rho;
        cell_L = cbrt(cell_V);
        tail = 16.0 * M_PI * Rho * ((2.0 / 3.0) * pow(RCUT, -9) - pow(RCUT, -3)) / 3.0;
        Etail = tail * (float)N;
        Ptail = tail * Rho;

        int i = 0;
        sf = cbrt(Rhob / Rho);

            for (int k = 0; k < N; k++) { // reescaleo posiciones a nueva densidad
                rx[k] *= sf;
                ry[k] *= sf;
                rz[k] *= sf;
            }

            init_vel(vx, vy, vz, &Temp, &Ekin);

	    for (int j = 0; j <  N; j++) {
              fx[j] = 0.0;
              fy[j] = 0.0;
              fz[j] = 0.0;
            }
            Epot=0;
            Pres=Temp* Rho ;


            float *epot_aux;
            float *pres_aux;
            float *ptr_Temp;


            checkCudaError(cudaMallocManaged(&epot_aux, sizeof(float *)));
            checkCudaError(cudaMallocManaged(&pres_aux, sizeof(float *)));
            checkCudaError(cudaMallocManaged(&ptr_Temp, sizeof(float *)));

            *epot_aux=0;
            *pres_aux=0;
            *ptr_Temp = Temp;

            // for (int i = 0; i < N-1; i+=1){
                launch_forces(rx, ry, rz, fx, fy, fz, epot_aux, pres_aux, ptr_Temp, Rho, cell_V, cell_L); // actualizo fuerzas

                Temp = *ptr_Temp;
            // }

             Epot+=*epot_aux;
             Pres+=*pres_aux;

            checkCudaError(cudaFree(epot_aux));
            checkCudaError(cudaFree(pres_aux));
            checkCudaError(cudaFree(ptr_Temp));


        for (i = 1; i < TEQ; i++) { // loop de equilibracion

            velocity_verlet(rx, ry, rz, vx, vy, vz, fx, fy, fz, &Epot, &Ekin, &Pres, &Temp, Rho, cell_V, cell_L);

            sf = sqrt(T0 / Temp);
            for (int k = 0; k < N; k++) { // reescaleo de velocidades
                vx[k] *= sf;
                vy[k] *= sf;
                vz[k] *= sf;
            }
        }

        int mes = 0;
        float epotm = 0.0, presm = 0.0;
        for (i = TEQ; i < TRUN; i++) { // loop de medicion

            velocity_verlet(rx, ry, rz, vx, vy, vz, fx, fy, fz, &Epot, &Ekin, &Pres, &Temp, Rho, cell_V, cell_L);

            sf = sqrt(T0 / Temp);
            for (int k = 0; k < N; k++) { // reescaleo de velocidades
                vx[k] *= sf;
                vy[k] *= sf;
                vz[k] *= sf;
            }

            if (i % TMES == 0) {
                Epot += Etail;
                Pres += Ptail;

                epotm += Epot;
                presm += Pres;
                mes++;

                fprintf(file_thermo, "%f %f %f %f %f\n", t, Temp, Pres, Epot, Epot + Ekin);
                fprintf(file_xyz, "%d\n\n", N);
                for (int k = 0; k < N; k++) {
                    fprintf(file_xyz, "Ar %e %e %e\n", rx[k], ry[k], rz[k]);
                }
            }

            t += DT;
        }
        printf("%f\t%f\t%f\t%f\n", Rho, cell_V, epotm / (float)mes, presm / (float)mes);
    }

    float elapsed = wtime() - start;
    FILE* logs;
    logs = fopen("statics.res", "a");
    if (logs == NULL) {
        printf("Cannot open statics log file");
        exit(EXIT_FAILURE);
    }

    fprintf(logs, "# Tiempo total de simulación = %f segundos\n", elapsed);
    float foperations = (N * (N - 1) * 0.5 * 41.0 + 5.0) * TRUN;
    fprintf(logs, "%s %f \n", "Floating point operation done:", foperations);
    float flops = foperations / elapsed;
    fprintf(logs, "%s %f\n", "FLOPS:", flops);
    fprintf(logs, "%s %f\n", "GFLOPS:", flops / (1000.0 * 1000.0 * 1000.0));
    fprintf(logs, "# Tiempo simulado = %f [fs]\n", t * 1.6);
    fprintf(logs, "# ns/day = %f\n", (1.6e-6 * t) / elapsed * 86400);
    //                       ^1.6 fs -> ns       ^sec -> day


    checkCudaError(cudaFree(rx));
    checkCudaError(cudaFree(ry));
    checkCudaError(cudaFree(rz));
    checkCudaError(cudaFree(vx));
    checkCudaError(cudaFree(vy));
    checkCudaError(cudaFree(vz));
    checkCudaError(cudaFree(fx));
    checkCudaError(cudaFree(fy));
    checkCudaError(cudaFree(fz));

    return 0;
}
