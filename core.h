#ifndef CORE_H
#define CORE_H

void init_pos(float* rx, float* ry, float* rz, const float rho);

void init_vel(float* vx, float* vy, float* vz, float* temp, float* ekin);

void velocity_verlet(float* rx, float* ry, float* rz, float* vx,
                     float* vy, float* vz,
                     float* fx, float* fy, float* fz, float* epot,
                     float* ekin, float* pres, float* temp, const float rho,
                     const float V, const float L);

#endif
