#ifndef _XOPEN_SOURCE
#define _XOPEN_SOURCE 500 // M_PI
#endif

#include "core.h"
#include "parameters.h"

#include <GL/glut.h> // OpenGL
#include <math.h>
#include <stdio.h>
#include <stdlib.h>


#include <cuda_runtime.h>
#include "forces_gpu.h"
#include "helper_cuda.h"

// variables globales
static double Ekin, Epot, Temp, Pres; // variables macroscopicas
static double Rho, V, box_size, tail, Etail, Ptail;
static double *rx, *ry, *rz, *vx, *vy, *vz, *fx, *fy, *fz; // variables microscopicas
static double Rhob, sf, epotm, presm;
static int switcher = 0, frames = 0, mes;


// OpenGL specific drawing routines
static int win_id;
static int win_x = 900, win_y = 900;


static void pre_display(void)
{ // 3D
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    gluPerspective(45.0, (float)win_x / win_y, 1.0, 0.0);
    gluLookAt(1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 1.0, 0.0, 0.0);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);
}


static void post_display(void)
{
    glutSwapBuffers();
}


static void draw_atoms(void)
{
    double glL = cbrt((double)N / (RHOI - 0.8));

    double resize = 0.5;

    // grafico las lineas que delimitan la caja de simulación
    glBegin(GL_LINES);

    double box_line = resize * (box_size / glL);
    glColor3d(0.0, 0.0, 1.0);

    glVertex3d(0.0, 0.0, 0.0);
    glVertex3d(0.0, 0.0, box_line);

    glVertex3d(0.0, 0.0, 0.0);
    glVertex3d(0.0, box_line, 0.0);

    glVertex3d(0.0, 0.0, 0.0);
    glVertex3d(box_line, 0.0, 0.0);

    glVertex3d(box_line, box_line, box_line);
    glVertex3d(box_line, box_line, 0.0);

    glVertex3d(box_line, box_line, box_line);
    glVertex3d(box_line, 0.0, box_line);

    glVertex3d(box_line, box_line, box_line);
    glVertex3d(0.0, box_line, box_line);

    glVertex3d(0.0, box_line, 0.0);
    glVertex3d(box_line, box_line, 0.0);

    glVertex3d(0.0, box_line, box_line);
    glVertex3d(0.0, 0.0, box_line);

    glVertex3d(box_line, 0.0, box_line);
    glVertex3d(box_line, 0.0, 0.0);

    glVertex3d(box_line, 0.0, box_line);
    glVertex3d(0.0, 0.0, box_line);

    glVertex3d(0.0, box_line, box_line);
    glVertex3d(0.0, box_line, 0.0);

    glVertex3d(box_line, box_line, 0.0);
    glVertex3d(box_line, 0.0, 0.0);

    glEnd();

    // grafico las particulas (x, y, z) en el punto (dx, dy, dx), son reescaleadas
    // a [0, 1] y luego multiplicadas con un factor que las achica para poder
    // apreciar mejor el cambio en el volumen
    glBegin(GL_POINTS);

    int di;

    double dx;
    double dy;
    double dz;

    for (di = 0; di < N; di++) {
        dx = (rx[di] / glL) * resize;
        dy = (ry[di] / glL) * resize;
        dz = (rz[di] / glL) * resize;

        glColor3d(0.0, 1.0, 0.0);
        glVertex3d(dx, dy, dz);
    }

    glEnd();
}


/*static void reshape_func ( int width, int height )
{
	glutSetWindow ( win_id );
	glutReshapeWindow ( width, height );

	win_x = width;
	win_y = height;
}*/


static void idle_func(void)
{

    if (switcher == 3) {

        Rho = RHOI;
        V = (double)N / Rho;
        box_size = cbrt(V);
        tail = 16.0 * M_PI * Rho * ((2.0 / 3.0) * pow(RCUT, -9) - pow(RCUT, -3)) / 3.0;
        Etail = tail * (double)N;
        Ptail = tail * Rho;

        init_pos(rx, ry, rz, Rho);
        init_vel(vx, vy, vz, &Temp, &Ekin);

        for (int j = 0; j < N; j++) {
            fx[j] = 0.0;
            fy[j] = 0.0;
            fz[j] = 0.0;
        }
        Epot = 0;
        Pres = Temp * Rho;
        // #pragma omp parallel
        {
            double *epot_aux;
            double *pres_aux;
            double *ptr_Temp;


            checkCudaError(cudaMallocManaged(&epot_aux, sizeof(double *)));
            checkCudaError(cudaMallocManaged(&pres_aux, sizeof(double *)));
            checkCudaError(cudaMallocManaged(&ptr_Temp, sizeof(double *)));

            *epot_aux=0;
            *pres_aux=0;
            *ptr_Temp = Temp;

            // for (int i = 0; i < N - 1; i += 1) {
                launch_forces(rx, ry, rz, fx, fy, fz, epot_aux, pres_aux, ptr_Temp, Rho, V, box_size);
            // }
            Epot += *epot_aux;
            Pres += *pres_aux;

            checkCudaError(cudaFree(epot_aux));
            checkCudaError(cudaFree(pres_aux));
            checkCudaError(cudaFree(ptr_Temp));
        }

        switcher = 0;

    } else if (switcher == 2) { // imprimo propiedades en la terminal y cambio la densidad

        printf("%f\t%f\t%f\t%f\n", Rho, V, epotm / (double)mes,
               presm / (double)mes);

        Rhob = Rho;
        Rho = Rho - 0.1;

        V = (double)N / Rho;
        box_size = cbrt(V);
        tail = 16.0 * M_PI * Rho * ((2.0 / 3.0) * pow(RCUT, -9) - pow(RCUT, -3)) / 3.0;
        Etail = tail * (double)N;
        Ptail = tail * Rho;

        sf = cbrt(Rhob / Rho);
        for (int k = 0; k < N; k++) { // reescaleo posiciones a nueva densidad
            rx[k] *= sf;
            ry[k] *= sf;
            rz[k] *= sf;
        }
        init_vel(vx, vy, vz, &Temp, &Ekin);

        for (int j = 0; j < N; j++) {
            fx[j] = 0.0;
            fy[j] = 0.0;
            fz[j] = 0.0;
        }
        Epot = 0;
        Pres = Temp * Rho;
        // #pragma omp parallel
        {
            double *epot_aux;
            double *pres_aux;
            double *ptr_Temp;


            checkCudaError(cudaMallocManaged(&epot_aux, sizeof(double *)));
            checkCudaError(cudaMallocManaged(&pres_aux, sizeof(double *)));
            checkCudaError(cudaMallocManaged(&ptr_Temp, sizeof(double *)));

            *epot_aux=0;
            *pres_aux=0;
            *ptr_Temp = Temp;

            // #pragma omp for
            // for (int i = 0; i < N - 1; i += 1) {
                launch_forces(rx, ry, rz, fx, fy, fz, epot_aux, pres_aux, ptr_Temp, Rho, V, box_size);
            // }
            // #pragma omp critical
            Epot += *epot_aux;
            Pres += *pres_aux;

            checkCudaError(cudaFree(epot_aux));
            checkCudaError(cudaFree(pres_aux));
            checkCudaError(cudaFree(ptr_Temp));
        }

        switcher = 0;
        if (fabs(Rho - (RHOI - 0.9f)) < 1e-6) {
            printf("\n");
            switcher = 3;
        }

    } else if (switcher == 1) { // loop de medición


        for (int i = frames; i < frames + TMES; i++) {

            velocity_verlet(rx, ry, rz, vx, vy, vz, fx, fy, fz, &Epot, &Ekin, &Pres, &Temp, Rho, V, box_size);

            sf = sqrt(T0 / Temp);
            for (int k = 0; k < N; k++) { // reescaleo de velocidades
                vx[k] *= sf;
                vy[k] *= sf;
                vz[k] *= sf;
            }
        }

        Epot += Etail;
        Pres += Ptail;

        epotm += Epot;
        presm += Pres;
        mes++;

        frames += TMES;
        if (frames % TRUN == 0) {
            switcher = 2;
        }

    } else if (switcher == 0) { // loop de equilibración


        while (frames % TEQ != 0) {

            velocity_verlet(rx, ry, rz, vx, vy, vz, fx, fy, fz, &Epot, &Ekin, &Pres, &Temp, Rho, V, box_size);

            sf = sqrt(T0 / Temp);
            for (int k = 0; k < N; k++) { // reescaleo de velocidades
                vx[k] *= sf;
                vy[k] *= sf;
                vz[k] *= sf;
            }

            frames++;
        }

        mes = 0;
        epotm = 0.0;
        presm = 0.0;

        switcher = 1;
    }
    glutSetWindow(win_id);
    glutPostRedisplay();
}


static void display_func(void)
{
    pre_display();
    draw_atoms();
    post_display();
}


static void open_glut_window(void)
{
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE);

    glutInitWindowPosition(0, 0);
    glutInitWindowSize(win_x, win_y);
    win_id = glutCreateWindow("tiny molecular dynamics | visualization");

    glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);
    glutSwapBuffers();
    glClear(GL_COLOR_BUFFER_BIT);
    glutSwapBuffers();

    pre_display();

    // glutKeyboardFunc ( key_func );
    // glutMouseFunc ( mouse_func );
    // glutMotionFunc ( motion_func );
    //glutReshapeFunc ( reshape_func );

    glutIdleFunc(idle_func);
    glutDisplayFunc(display_func);
}


// viz main

int main(int argc, char** argv)
{
    glutInit(&argc, argv);

    // rx = (double*)malloc(N * sizeof(double));
    // ry = (double*)malloc(N * sizeof(double));
    // rz = (double*)malloc(N * sizeof(double));
    // vx = (double*)malloc(N * sizeof(double));
    // vy = (double*)malloc(N * sizeof(double));
    // vz = (double*)malloc(N * sizeof(double));
    // fx = (double*)malloc(N * sizeof(double));
    // fy = (double*)malloc(N * sizeof(double));
    // fz = (double*)malloc(N * sizeof(double));

    checkCudaError(cudaMallocManaged(&rx, N * sizeof(double *)));
    checkCudaError(cudaMallocManaged(&ry, N * sizeof(double *)));
    checkCudaError(cudaMallocManaged(&rz, N * sizeof(double *)));
    checkCudaError(cudaMallocManaged(&vx, N * sizeof(double *)));
    checkCudaError(cudaMallocManaged(&vy, N * sizeof(double *)));
    checkCudaError(cudaMallocManaged(&vz, N * sizeof(double *)));
    checkCudaError(cudaMallocManaged(&fx, N * sizeof(double *)));
    checkCudaError(cudaMallocManaged(&fy, N * sizeof(double *)));
    checkCudaError(cudaMallocManaged(&fz, N * sizeof(double *)));


    checkCudaError(cudaMemset(rx, 0, N * sizeof(double *)));
    checkCudaError(cudaMemset(ry, 0, N * sizeof(double *)));
    checkCudaError(cudaMemset(rz, 0, N * sizeof(double *)));
    checkCudaError(cudaMemset(vx, 0, N * sizeof(double *)));
    checkCudaError(cudaMemset(vy, 0, N * sizeof(double *)));
    checkCudaError(cudaMemset(vz, 0, N * sizeof(double *)));
    checkCudaError(cudaMemset(fx, 0, N * sizeof(double *)));
    checkCudaError(cudaMemset(fy, 0, N * sizeof(double *)));
    checkCudaError(cudaMemset(fz, 0, N * sizeof(double *)));


    // parametros iniciales para que los pueda usar (antes de modificar)
    // `idle_func`
    srand(SEED);
    Rho = RHOI;
    Rhob = Rho;
    V = (double)N / Rho;
    box_size = cbrt(V);
    tail = 16.0 * M_PI * Rho * ((2.0 / 3.0) * pow(RCUT, -9) - pow(RCUT, -3)) / 3.0;
    Etail = tail * (double)N;
    Ptail = tail * Rho;

    init_pos(rx, ry, rz, Rho);
    init_vel(vx, vy, vz, &Temp, &Ekin);

    for (int j = 0; j < N; j++) {
        fx[j] = 0.0;
        fy[j] = 0.0;
        fz[j] = 0.0;
    }
    Epot = 0;
    Pres = Temp * Rho;
    // #pragma omp parallel
        {
            double *epot_aux;
            double *pres_aux;
            double *ptr_Temp;


            checkCudaError(cudaMallocManaged(&epot_aux, sizeof(double *)));
            checkCudaError(cudaMallocManaged(&pres_aux, sizeof(double *)));
            checkCudaError(cudaMallocManaged(&ptr_Temp, sizeof(double *)));

            *epot_aux=0;
            *pres_aux=0;
            *ptr_Temp = Temp;

            // #pragma omp for
            // for (int i = 0; i < N - 1; i += 1) {
                launch_forces(rx, ry, rz, fx, fy, fz, epot_aux, pres_aux, ptr_Temp, Rho, V, box_size);
            // }
            // #pragma omp critical
            Epot += *epot_aux;
            Pres += *pres_aux;

            checkCudaError(cudaFree(epot_aux));
            checkCudaError(cudaFree(pres_aux));
            checkCudaError(cudaFree(ptr_Temp));
        }


    printf("# Número de partículas:      %d\n", N);
    printf("# Temperatura de referencia: %.2f\n", T0);
    printf("# Pasos de equilibración:    %d\n", TEQ);
    printf("# Pasos de medición:         %d\n", TRUN - TEQ);
    printf("# (mediciones cada %d pasos)\n", TMES);

    open_glut_window();

    glutMainLoop();

    checkCudaError(cudaFree(rx));
    checkCudaError(cudaFree(ry));
    checkCudaError(cudaFree(rz));
    checkCudaError(cudaFree(vx));
    checkCudaError(cudaFree(vy));
    checkCudaError(cudaFree(vz));
    checkCudaError(cudaFree(fx));
    checkCudaError(cudaFree(fy));
    checkCudaError(cudaFree(fz));

    exit(0);
}
