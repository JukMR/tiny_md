#ifndef FORCES_GPU_H
#define FORCES_GPU_H

// #ifdef __cplusplus
// extern "C"{
// #endif

void launch_forces(const float *rx, const float *ry, const float *rz,
              float *fx, float *fy, float *fz,
              float *epot, float *pres, const float *temp,
              const float rho, const float V, const float L);

// #ifdef __cplusplus
// }
// #endif

#endif