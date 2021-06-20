#ifndef FORCES_GPU_H
#define FORCES_GPU_H

// #ifdef __cplusplus
// extern "C"{
// #endif

void launch_forces(const double *rx, const double *ry, const double *rz,
              double *fx, double *fy, double *fz,
              double *epot, double *pres, const double *temp,
              const double rho, const double V, const double L,
              const int row);

// #ifdef __cplusplus
// }
// #endif

#endif