// Variables necesarias

#ifndef RCUT // radio de corte
#define RCUT 2.5
#endif
#ifndef N // número de particulas (debe ser un 4m^3 para el cristal inicial)
#define N 500
#endif

//#define ECUT (4.0 * (pow(RCUT, -12) - pow(RCUT, -6)))

double minimum_image(double cordi, const double cell_length)
{
    // imagen más cercana
    if (cordi <= -0.5 * cell_length) {
        cordi += cell_length;
    } else if (cordi > 0.5* cell_length) {
        cordi -= cell_length;
    }
//    cordi -= nearbyint(cordi*(1/cell_length))*cell_length;
    return cordi;
}


export void forces(const double uniform rx[],
                   const double uniform ry[],
                   const double uniform rz[],
                   double uniform fx[],
                   double uniform fy[],
                   double uniform fz[],
                   uniform double epot[],
                   uniform double pres[],
                   uniform const double uniform temp[],
                   uniform const double rho,
                   uniform const double V,
                   uniform const double L,
                   uniform const int32 row)
{

//        fx[row] = 0.0d;
//        fy[row] = 0.0d;
//        fz[row] = 0.0d;

    uniform double pres_vir = 0.0;
//    *epot = 0.0;
    uniform double rcut2 = RCUT * RCUT;
    uniform const double RCUT12 = RCUT * RCUT * RCUT * RCUT * RCUT * RCUT * RCUT *
                                RCUT * RCUT * RCUT * RCUT * RCUT;

    uniform const double RCUT6  = RCUT * RCUT * RCUT * RCUT * RCUT * RCUT;
    uniform const double ECUT = 4.0 * (1/(RCUT12) - 1/(RCUT6));
    //#define ECUT (4.0 * (pow(RCUT, -12) - pow(RCUT, -6)))
    uniform double L2 = 0.5 * L;
///////////////////////////////////////////////
// for (uniform int i = 0; i < (N - 1); i++) {

    double fxi = 0.0;
    double fyi = 0.0;
    double fzi = 0.0;
    double epot_partial = 0.0d;
    double pres_vir_partial = 0.0d ;

	foreach (j = row+1 ... (N-1)){

            double xi = rx[row];
            double yi = ry[row];
            double zi = rz[row];

            double xj = rx[j];
            double yj = ry[j];
            double zj = rz[j];

            double rxd = xi - xj;
            double ryd = yi - yj;
            double rzd = zi - zj;

            rxd = minimum_image(rxd, L);
            ryd = minimum_image(ryd, L);
            rzd = minimum_image(rzd, L);

            double rij2 = rxd * rxd + ryd * ryd + rzd * rzd;

            if (rij2 <= rcut2) {
                double r2inv = 1.0d / rij2;
                double r6inv = r2inv*r2inv*r2inv;

                double fr = 24.0d * r2inv * r6inv * (2.0d * r6inv - 1.0d);

                fxi += fr * rxd;
                fyi += fr * ryd;
                fzi += fr * rzd;
                fx[j] -= fr * rxd;
                fy[j] -= fr * ryd;
                fz[j] -= fr * rzd;


                epot_partial +=  4.0d * r6inv * (r6inv - 1.0) - ECUT;
                pres_vir_partial += fr * rij2 ;
            }
        }
        fx[row] += reduce_add(fxi);
        fy[row] += reduce_add(fyi);
        fz[row] += reduce_add(fzi);
        *epot +=reduce_add(epot_partial);
        pres_vir += reduce_add(pres_vir_partial);
  //}
   pres_vir /= (V * 3.0d);
   //*pres = *temp * rho + pres_vir; // revisar
   *pres += pres_vir; // revisar


}



