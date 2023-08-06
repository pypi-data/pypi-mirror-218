#ifndef GUARD_naive_h
#define GUARD_naive_h

#include<vector>

std::vector<double> cpp_mmd_lap(double* X, double* Y, 
                                int nX, int dX,
                                int nY, int dY,
                                double beta);

std::vector<double> cpp_mmd_gau(double* X, double* Y, 
                                int nX, int dX,
                                int nY, int dY,
                                double beta);

std::vector<double> cpp_mmd_lap_pval(double* X, double* Y, 
                                     int nX, int dX,
                                     int nY, int dY,
                                     int numperm, int seednum,
                                     double beta);

std::vector<double> cpp_mmd_gau_pval(double* X, double* Y, 
                                     int nX, int dX,
                                     int nY, int dY,
                                     int numperm, int seednum,
                                     double beta);


#endif

