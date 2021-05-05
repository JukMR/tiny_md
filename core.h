#ifndef CORE_H
#define CORE_H

void init_pos(double* rx, double* ry, double* rz, const double rho);

void init_vel(double* vx, double* vy, double* vz, double* temp, double* ekin);

extern void forces(const double* rx, const double* ry, const double* rz,
                   double* fx, double* fy, double* fz, double* epot, double* pres, const double* temp, const double rho, const double V, const double L);

void velocity_verlet(double* rx, double* ry, double* rz, double* vx,
                     double* vy, double* vz,
                     double* fx, double* fy, double* fz, double* epot,
                     double* ekin, double* pres, double* temp, const double rho,
                     const double V, const double L);

#endif
