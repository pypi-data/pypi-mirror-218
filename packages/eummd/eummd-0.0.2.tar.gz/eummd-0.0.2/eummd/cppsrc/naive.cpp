// for std::abs
// #include<cmath>
// #include<math.h>
#include<vector>
#include<random>
#include<math.h>
#include<algorithm>
#include "medianHeuristic.h"


/* Naive MMD with Laplacian kernel
 *
 * Compute the MMD for two matrices
 *
 * @param X First matrix, double*
 *
 * @param Y Second matrix, double*
 *
 * @param beta Parameter for Laplacian kernel.
 *
 * @return A scalar, the kernel value of the two vectors.
 */

std::vector<double> cpp_mmd_lap(double* X, double* Y, 
                                int nX, int dX,
                                int nY, int dY,
                                double beta){

    // return vector is first pval, then statistic
    std::vector<double> returnvec;

    if (dX != dY){
        //error, dimensions incorrect
        returnvec.push_back(-2.0); 
        returnvec.push_back(-2.0);
        return returnvec;
    }

    // if beta <= 0, find using medianHeuristic
    if ( !(beta > 0) ){
        //int should really be size_t
        size_t Xsize = nX*dX;
        size_t Ysize = nY*dY;
        size_t Zsize = Xsize + Ysize;

        // create vector
        std::vector<double> Z;
        Z.reserve(Zsize);
        //insert X then Y
        Z.insert(Z.end(), &X[0], &X[0]+Xsize);
        Z.insert(Z.end(), &Y[0], &Y[0]+Ysize);
        // multivariate, so need to use naive method; kmethod 2 for Laplacian
        beta = 1.0 / naive_multiv_medianHeuristic(Z, dX, nX+nY, 1);
    }


    double arg=0;
    //terms used in computing MMD
    double T1 = 0;
    for (int i = 0; i < nX; ++i){
        for (int j = 0; j < nX; ++j){
            if (i != j){
                arg = 0;
                for (int alpha=0; alpha < dX; ++alpha){
                    arg += std::abs( X[i*dX+alpha] - X[j*dX+alpha] ); 
                }
                T1 += std::exp( -beta * arg );
            }
        }
    }

    double T2 = 0;
    for (int p = 0; p < nY; ++p){
        for (int q = 0; q < nY; ++q){
            if (p != q){
                arg = 0;
                for (int alpha=0; alpha < dY; ++alpha){
                    arg += std::abs( Y[p*dY+alpha] - Y[q*dY+alpha] ); 
                }
                T2 += std::exp( -beta * arg );
            }
        }
    }

    double T3 = 0;
    for (int i = 0; i < nX; ++i){
        for (int p = 0; p < nY; ++p){
            arg = 0;
            for (int alpha=0; alpha < dY; ++alpha){
                arg += std::abs( X[i*dX+alpha] - Y[p*dY+alpha] );
            }
            T3 += std::exp(  -beta * arg  );
        }
    }

    double c1 = 0;
    if (nX > 1){
        c1 = 1.0 / (nX * (nX-1) );
    }
    double c2 = 0;
    if (nY > 1){
        c2 = 1.0 / (nY * (nY-1) );
    }
    double c3 = -2.0 / (nX * nY);

    double MMD_u = c1*T1 + c2*T2 + c3*T3 ;

    returnvec.push_back(MMD_u);
    returnvec.push_back(beta);
    return returnvec;
} // end of cpp_mmd_lap



/* MMD with Gaussian kernel
 *
 * Compute the MMD for two matrices
 *
 * @param X First matrix, double*
 *
 * @param Y Second matrix, double*
 *
 * @param beta Parameter for Laplacian kernel.
 *
 * @return A scalar, the kernel value of the two vectors.
 */

std::vector<double> cpp_mmd_gau(double* X, double* Y, 
                                int nX, int dX,
                                int nY, int dY,
                                double beta){

    // return vector is first pval, then statistic
    std::vector<double> returnvec;

    if (dX != dY){
        //error, dimensions incorrect
        returnvec.push_back(-2.0); 
        returnvec.push_back(-2.0);
        return returnvec;
    }

    // if beta <= 0, find using medianHeuristic
    if ( !(beta > 0) ){
        //int should really be size_t
        size_t Xsize = nX*dX;
        size_t Ysize = nY*dY;
        size_t Zsize = Xsize + Ysize;

        // create vector
        std::vector<double> Z;
        Z.reserve(Zsize);
        //insert X then Y
        Z.insert(Z.end(), &X[0], &X[0]+Xsize);
        Z.insert(Z.end(), &Y[0], &Y[0]+Ysize);
        // multivariate, so need to use naive method; kmethod 2 for Laplacian
        beta = 1.0 / naive_multiv_medianHeuristic(Z, dX, nX+nY, 2);
    }


    // temporary variables; only compute difference and exp once
    double arg=0;
    double diff = 0;
    //terms used in computing MMD
    double T1 = 0;
    for (int i = 0; i < nX; ++i){
        for (int j = 0; j < nX; ++j){
            if (i != j){
                arg = 0;
                for (int alpha=0; alpha < dX; ++alpha){
                    diff = X[i*dX+alpha] - X[j*dX+alpha];
                    arg += diff*diff; 
                }
                T1 += std::exp( -beta * arg );
            }
        }
    }

    double T2 = 0;
    for (int p = 0; p < nY; ++p){
        for (int q = 0; q < nY; ++q){
            if (p != q){
                arg = 0;
                for (int alpha=0; alpha < dY; ++alpha){
                    diff = Y[p*dY+alpha] - Y[q*dY+alpha];
                    arg += diff*diff; 
                }
                T2 += std::exp( -beta * arg );
            }
        }
    }

    double T3 = 0;
    for (int i = 0; i < nX; ++i){
        for (int p = 0; p < nY; ++p){
            arg = 0;
            for (int alpha=0; alpha < dY; ++alpha){
                diff = X[i*dX+alpha] - Y[p*dY+alpha];
                arg += diff*diff;
            }
            T3 += std::exp( -beta * arg  );
        }
    }

    double c1 = 0;
    if (nX > 1){
        c1 = 1.0 / (nX * (nX-1) );
    }
    double c2 = 0;
    if (nY > 1){
        c2 = 1.0 / (nY * (nY-1) );
    }
    double c3 = -2.0 / (nX * nY);

    double MMD_u = c1*T1 + c2*T2 + c3*T3 ;

    returnvec.push_back(MMD_u);
    returnvec.push_back(beta);
    return returnvec;
}
// end of cpp_mmd_gau



// using only a single vector of values and a single index vector, 
// and noting the sizes of X and Y, and the dimension d
// uses Zindex to extract rows; used for shuffling
double cpp_mmd_lap_ptr(std::vector<double> &Z, 
                       std::vector<size_t> &Zindex,
                       size_t nX,
                       size_t nY,
                       size_t dZ,
                       double beta){

    double arg=0;
    size_t nZ = nX + nY;

    //terms used in computing MMD
    double T1 = 0;
    for (size_t i = 0; i < nX; ++i){
        for (size_t j = 0; j < nX; ++j){
            if (i != j){
                arg = 0;
                for (size_t alpha=0; alpha < dZ; ++alpha){
                    arg += std::abs( Z.at(Zindex.at(i)*dZ + alpha) - Z.at(Zindex.at(j)*dZ + alpha) ); 
                }
                T1 += std::exp( -beta * arg );
            }
        }
    }

    double T2 = 0;
    for (size_t p = nX; p < nZ; ++p){
        for (size_t q = nX; q < nZ; ++q){
            if (p != q){
                arg = 0;
                for (size_t alpha=0; alpha < dZ; ++alpha){
                    arg += std::abs( Z.at( Zindex.at(p)*dZ+alpha ) - Z.at( Zindex.at(q)*dZ+alpha ) ); 
                }
                T2 += std::exp( -beta * arg );
            }
        }
    }

    double T3 = 0;
    for (size_t i = 0; i < nX; ++i){
        for (size_t p = nX; p < nZ; ++p){
            arg = 0;
            for (size_t alpha=0; alpha < dZ; ++alpha){
                arg += std::abs( Z.at(Zindex.at(i)*dZ+alpha) - Z.at(Zindex.at(p)*dZ+alpha) );
            }
            T3 += std::exp(  -beta * arg  );
        }
    }

    double c1 = 0;
    if (nX > 1){
        c1 = 1.0 / (nX * (nX-1) );
    }
    double c2 = 0;
    if (nY > 1){
        c2 = 1.0 / (nY * (nY-1) );
    }
    double c3 = -2.0 / (nX * nY);

    double MMD_u = c1*T1 + c2*T2 + c3*T3 ;
    return MMD_u;
}
//cpp_mmd_lap_ptr



// return both pval and statistic
std::vector<double> cpp_mmd_lap_pval(double* X, double* Y, 
                                     int nX, int dX,
                                     int nY, int dY,
                                     int numperm, int seednum, double beta){

    // return vector is first pval, then statistic
    std::vector<double> returnvec;

    if (dX != dY){
        //error, dimensions incorrect
        returnvec.push_back(-2.0); 
        returnvec.push_back(-2.0);
        returnvec.push_back(-2.0);
        return returnvec;
    }


    //int should really be size_t
    size_t Xsize = nX*dX;
    size_t Ysize = nY*dY;
    size_t Zsize = Xsize + Ysize;

    // create vector
    std::vector<double> Z;
    Z.reserve(Zsize);
    //insert X then Y
    Z.insert(Z.end(), &X[0], &X[0]+Xsize);
    Z.insert(Z.end(), &Y[0], &Y[0]+Ysize);

    //now create indices
    std::vector<size_t> Zindex(nX + nY);
    std::iota(Zindex.begin(), Zindex.end(), 0);

    // if beta <= 0, find using medianHeuristic
    if ( !(beta > 0) ){
        // multivariate, so need to use naive method; kmethod 2 for Laplacian
        beta = 1.0 / naive_multiv_medianHeuristic(Z, dX, nX+nY, 1);
    }

    //compute MMD statistic
    double MMDstar = cpp_mmd_lap_ptr(Z, Zindex, nX, nY, dX, beta);

    // initiate random generator
    std::random_device rd;
    std::mt19937 g;
    // set the seed, if greater than 0
    if (seednum > 0){
        g.seed(seednum);
    } else {
        g.seed(rd());
    }

    double MMDperm = 0.0;
    int MMD_count_below = 1;

    //run the permutations
    for (int i=0; i < numperm; ++i){
        //shuffle
        std::shuffle(Zindex.begin(), Zindex.end(), g);
        MMDperm = cpp_mmd_lap_ptr(Z, Zindex, nX, nY, dX, beta);

        if (MMDperm < MMDstar){
            ++MMD_count_below;
        }
    }

    //now return the threshold
    double pval = MMD_count_below / (numperm + 1.0);

    //make one-sided
    // pval = convertTwoSidedPvalueToOneSided(pval);
    pval =  1 - std::abs(1 - 2*pval) ;

    // quick check for minimum possible p-value; avoids pval=0
    // 1 / 2(numperm+1)
    double pmin = 0.5 / (numperm+1.0);
    if (pval < pmin)
        pval = pmin;

    // return vector is first pval, then statistic
    returnvec.push_back(pval);
    returnvec.push_back(MMDstar);
    returnvec.push_back(beta);
    return returnvec;
}
// cpp_mmd_lap_pval




// using only a single vector of values and a single index vector, 
// and noting the sizes of X and Y, and the dimension d
double cpp_mmd_gau_ptr(std::vector<double> &Z, 
                       std::vector<size_t> &Zindex,
                       size_t nX,
                       size_t nY,
                       size_t dZ,
                       double beta){

    double arg=0;
    double diff = 0;
    size_t nZ = nX + nY;

    //terms used in computing MMD
    double T1 = 0;
    for (size_t i = 0; i < nX; ++i){
        for (size_t j = 0; j < nX; ++j){
            if (i != j){
                arg = 0;
                for (size_t alpha=0; alpha < dZ; ++alpha){
                    diff = Z.at(Zindex.at(i)*dZ + alpha) - Z.at(Zindex.at(j)*dZ + alpha);
                    arg += diff*diff; 
                }
                T1 += std::exp( -beta * arg );
            }
        }
    }

    double T2 = 0;
    for (size_t p = nX; p < nZ; ++p){
        for (size_t q = nX; q < nZ; ++q){
            if (p != q){
                arg = 0;
                for (size_t alpha=0; alpha < dZ; ++alpha){
                    diff = Z.at( Zindex.at(p)*dZ+alpha ) - Z.at( Zindex.at(q)*dZ+alpha ); 
                    arg += diff * diff;
                }
                T2 += std::exp( -beta * arg );
            }
        }
    }

    double T3 = 0;
    for (size_t i = 0; i < nX; ++i){
        for (size_t p = nX; p < nZ; ++p){
            arg = 0;
            for (size_t alpha=0; alpha < dZ; ++alpha){
                diff = Z.at(Zindex.at(i)*dZ+alpha) - Z.at(Zindex.at(p)*dZ+alpha);
                arg += diff * diff;
            }
            T3 += std::exp(  -beta * arg  );
        }
    }

    double c1 = 0;
    if (nX > 1){
        c1 = 1.0 / (nX * (nX-1) );
    }
    double c2 = 0;
    if (nY > 1){
        c2 = 1.0 / (nY * (nY-1) );
    }
    double c3 = -2.0 / (nX * nY);

    double MMD_u = c1*T1 + c2*T2 + c3*T3 ;
    return MMD_u;
}
//cpp_mmd_gau_ptr



// return both pval and statistic
std::vector<double> cpp_mmd_gau_pval(double* X, double* Y, 
                                     int nX, int dX,
                                     int nY, int dY,
                                     int numperm, int seednum, double beta){

    // return vector is first pval, then statistic
    std::vector<double> returnvec;

    if (dX != dY){
        //error, dimensions incorrect
        returnvec.push_back(-2.0); 
        returnvec.push_back(-2.0);
        returnvec.push_back(-2.0);
        return returnvec;
    }

    //int should really be size_t
    size_t Xsize = nX*dX;
    size_t Ysize = nY*dY;
    size_t Zsize = Xsize + Ysize;

    // create vector
    std::vector<double> Z;
    Z.reserve(Zsize);
    //insert X then Y
    Z.insert(Z.end(), &X[0], &X[0]+Xsize);
    Z.insert(Z.end(), &Y[0], &Y[0]+Ysize);

    //now create indices
    std::vector<size_t> Zindex(nX + nY);
    std::iota(Zindex.begin(), Zindex.end(), 0);

    // if beta <= 0, find using medianHeuristic
    if ( !(beta > 0) ){
        // multivariate, so need to use naive method; kmethod 2 for Gaussian
        beta = 1.0 / naive_multiv_medianHeuristic(Z, dX, nX+nY, 2);
    }

    //compute MMD statistic
    double MMDstar = cpp_mmd_gau_ptr(Z, Zindex, nX, nY, dX, beta);

    // initiate random generator
    std::random_device rd;
    std::mt19937 g;
    // set the seed, if greater than 0
    if (seednum > 0){
        g.seed(seednum);
    } else {
        g.seed(rd());
    }

    double MMDperm = 0.0;
    int MMD_count_below = 1;

    //run the permutations
    for (int i=0; i < numperm; ++i){
        //shuffle
        std::shuffle(Zindex.begin(), Zindex.end(), g);
        MMDperm = cpp_mmd_gau_ptr(Z, Zindex, nX, nY, dX, beta);

        if (MMDperm < MMDstar){
            ++MMD_count_below;
        }
    }

    //now return the threshold
    double pval = MMD_count_below / (numperm + 1.0);

    //make one-sided
    // pval = convertTwoSidedPvalueToOneSided(pval);
    pval =  1 - std::abs(1 - 2*pval) ;

    // quick check for minimum possible p-value; avoids pval=0
    // 1 / 2(numperm+1)
    double pmin = 0.5 / (numperm+1.0);
    if (pval < pmin)
        pval = pmin;

    // return vector is first pval, then statistic
    returnvec.push_back(pval);
    returnvec.push_back(MMDstar);
    returnvec.push_back(beta);
    return returnvec;
}
//cpp_mmd_gau_pval
