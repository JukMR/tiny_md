#define _XOPEN_SOURCE 500 // M_PI
#include "core.h"
#include "parameters.h"
#include "wtime.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>

//#include <omp.h>
int main()
{
    FILE *file_xyz, *file_thermo;
    file_xyz = fopen("trajectory.xyz", "w");
    file_thermo = fopen("thermo.log", "w");
    double Ekin, Epot, Temp, Pres; // variables macroscopicas
    double Rho, cell_V, cell_L, tail, Etail, Ptail;
    double *rx, *ry, *rz, *vx, *vy, *vz, *fx, *fy, *fz; // variables microscopicas
    rx = (double*)malloc(N * sizeof(double));
    ry = (double*)malloc(N * sizeof(double));
    rz = (double*)malloc(N * sizeof(double));
    vx = (double*)malloc(N * sizeof(double));
    vy = (double*)malloc(N * sizeof(double));
    vz = (double*)malloc(N * sizeof(double));
    fx = (double*)malloc(N * sizeof(double));
    fy = (double*)malloc(N * sizeof(double));
    fz = (double*)malloc(N * sizeof(double));

    //    rxyz = (double*)malloc(3 * N * sizeof(double));
    //    vxyz = (double*)malloc(3 * N * sizeof(double));
    //    fxyz = (double*)malloc(3 * N * sizeof(double));

    printf("# Número de partículas:      %d\n", N);
    printf("# Temperatura de referencia: %.2f\n", T0);
    printf("# Pasos de equilibración:    %d\n", TEQ);
    printf("# Pasos de medición:         %d\n", TRUN - TEQ);
    printf("# (mediciones cada %d pasos)\n", TMES);
    printf("# densidad, volumen, energía potencial media, presión media\n");
    fprintf(file_thermo, "# t Temp Pres Epot Etot\n");

    srand(SEED);
    double t = 0.0, sf;
    double Rhob;
    Rho = RHOI;
    init_pos(rx, ry, rz, Rho);
    double start = wtime();

    // double ecut = (4.0 * (pow(RCUT, -12) - pow(RCUT, -6)));
    for (int m = 0; m < 9; m++) {
        Rhob = Rho;
        Rho = RHOI - 0.1 * (double)m;
        cell_V = (double)N / Rho;
        cell_L = cbrt(cell_V);
        tail = 16.0 * M_PI * Rho * ((2.0 / 3.0) * pow(RCUT, -9) - pow(RCUT, -3)) / 3.0;
        Etail = tail * (double)N;
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
	    #pragma omp parallel num_threads(6)
   	    {
            double epot_aux=0;
            double pres_aux=0;
     	     #pragma omp for
             for (int i = 0; i < N-1; i+=1){
                forces(rx, ry, rz, fx, fy, fz, &epot_aux, &pres_aux, &Temp, Rho, cell_V, cell_L, i); // actualizo fuerzas
              }
             #pragma omp critical
             Epot+=epot_aux;
             Pres+=pres_aux;
            }

         //   for(int row = 0 ; row < N-1 ; row++) {
         //       forces(rx, ry, rz, fx, fy, fz, &Epot, &Pres, &Temp, Rho,
         //              cell_V, cell_L, row );
         //   }
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
        double epotm = 0.0, presm = 0.0;
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
        printf("%f\t%f\t%f\t%f\n", Rho, cell_V, epotm / (double)mes, presm / (double)mes);
    }

    double elapsed = wtime() - start;
    FILE* logs;
    logs = fopen("statics.res", "a");
    if (logs == NULL) {
        printf("Cannot open statics log file");
        exit(EXIT_FAILURE);
    }

    fprintf(logs, "# Tiempo total de simulación = %f segundos\n", elapsed);
    double foperations = (N * (N - 1) * 0.5 * 41.0 + 5.0) * TRUN;
    fprintf(logs, "%s %f \n", "Floating point operation done:", foperations);
    double flops = foperations / elapsed;
    fprintf(logs, "%s %f\n", "FLOPS:", flops);
    fprintf(logs, "%s %f\n", "GFLOPS:", flops / (1000.0 * 1000.0 * 1000.0));
    fprintf(logs, "# Tiempo simulado = %f [fs]\n", t * 1.6);
    fprintf(logs, "# ns/day = %f\n", (1.6e-6 * t) / elapsed * 86400);
    //                       ^1.6 fs -> ns       ^sec -> day
    return 0;
}
