// Variables necesarias

#ifndef RCUT // radio de corte
#define RCUT 2.5
#endif
#ifndef N // número de particulas (debe ser un 4m^3 para el cristal inicial)
#define N 256
#endif

#define ECUT (4.0 * (pow(RCUT, -12) - pow(RCUT, -6)))

static double minimum_image(double cordi, const double cell_length)
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
                   double epot[],
                   double pres[],
                   uniform const double uniform temp[],
                   uniform const double rho,
                   uniform const double V,
                   uniform const double L)
{

foreach(i = 0 ... N-1)
{
    fx[i] = 0.0;
    fy[i] = 0.0;
    fz[i] = 0.0;
}

double pres_vir = 0.0;
double rcut2 = RCUT * RCUT;
double epot[0] = {0.0};



foreach(i = 0 ... (N-1))
{
    double xi = rx[i];
    double yi = ry[i];
    double zi = rz[i];

    for (int j = i + 1; j <  N; j++)
    {
        double xj = rx[j];
        double yj = ry[j];
        double zj = rz[j];


        double rx = xi - xj;
        rx = minimum_image(rx, L);
        double ry = yi - yj;
        ry = minimum_image(ry, L);
        double rz = zi - zj;
        rz = minimum_image(rz, L);

        double rij2 = rx * rx + ry * ry + rz * rz;

        if (rij2 <= rcut2) {
            double r2inv = 1.0 / rij2;
            double r6inv = r2inv * r2inv * r2inv;

            double fr = 24.0 * r2inv * r6inv * (2.0 * r6inv - 1.0);

            fx[i] += fr * rx;
            fy[i] += fr * ry;
            fz[i] += fr * rz;

            fx[j] -= fr * rx;
            fy[j] -= fr * ry;
            fz[j] -= fr * rz;

            epot[0] =  4.0 * r6inv * (r6inv - 1.0) - ECUT; // revisar

        }

    }
}

pres_vir = pres_vir / (V * 3.0);
pres[0] = *temp * rho + pres_vir; // revisar
}

