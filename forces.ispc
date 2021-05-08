// Variables necesarias

#ifndef RCUT // radio de corte
#define RCUT 2.5
#endif
#ifndef N // número de particulas (debe ser un 4m^3 para el cristal inicial)
#define N 256
#endif

#define ECUT (4.0 * (pow(RCUT, -12) - pow(RCUT, -6)))

double minimum_image(double cordi, const double cell_length)
{
    // imagen más cercana
    if (cordi <= -0.5 * cell_length) {
        cordi += cell_length;
    } else if (cordi > 0.5 * cell_length) {
        cordi -= cell_length;
    }
    return cordi;
}


export void forces(const double uniform rx[],
                   const double uniform ry[],
                   const double uniform rz[],
                   double uniform fx[],
                   double uniform fy[],
                   double uniform fz[],
                   uniform double uniform epot[],
                   uniform double uniform pres[],
                   uniform const double uniform temp[],
                   uniform const double rho,
                   uniform const double V,
                   uniform const double L)
{

foreach(i = 0 ... N)
{
    fx[i] = 0.0d;
    fy[i] = 0.0d;
    fz[i] = 0.0d;
}

uniform double pres_vir;
double pres_vir_partial = 0.0d ;
uniform double rcut2 = RCUT * RCUT;
double epot_partial = 0.0d;


foreach(i = 0 ... N-1)
{
    double xi = rx[i];
    double yi = ry[i];
    double zi = rz[i];

    for (int j = i + 1; j <  N; j++)
    {
        double xj = rx[j];
        double yj = ry[j];
        double zj = rz[j];

        double rxd = xi - xj;
        rxd = minimum_image(rxd, L);
        double ryd = yi - yj;
        ryd = minimum_image(ryd, L);
        double rzd = zi - zj;
        rzd = minimum_image(rzd, L);

        double rij2 = rxd * rxd + ryd * ryd + rzd * rzd;

        cif (rij2 <= rcut2) {
            double r2inv = 1.0d / rij2;
            double r6inv = r2inv * r2inv * r2inv;

            double fr = 24.0d * r2inv * r6inv * (2.0d * r6inv - 1.0d);

            fx[i] += fr * rxd;
            fy[i] += fr * ryd;
            fz[i] += fr * rzd;

            fx[j] -= fr * rxd;
            fy[j] -= fr * ryd;
            fz[j] -= fr * rzd;

            epot_partial +=  4.0d * r6inv * (r6inv - 1.0d) - ECUT;
            pres_vir_partial += fr * rij2 ;
        }
    }
}

*epot=reduce_add(epot_partial);
pres_vir=reduce_add(pres_vir_partial);
pres_vir /= (V * 3.0d);
*pres = *temp * rho + pres_vir;

}

