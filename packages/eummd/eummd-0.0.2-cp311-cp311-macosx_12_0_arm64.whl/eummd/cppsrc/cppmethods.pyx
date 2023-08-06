# distutils: language = c++

import cython

import numpy as np
cimport numpy as np

from libcpp.vector cimport vector

##=========================================================================##
## Headers for C++ functions
##=========================================================================##

cdef extern from "eummd.h":
    vector[double] cpp_eummd_pval_faster(vector[double], vector[double], double, int, int);
    vector[double] cpp_eummd(vector[double], vector[double], double);


cdef extern from "medianHeuristic.h":
    double medianHeuristic(vector[double]);
    double cpp_naive_multiv_medianHeuristic(double*, int, int, int);


cdef extern from "naive.h":
    vector[double] cpp_mmd_lap(double*, double*, int, int, int, int, double);
    vector[double] cpp_mmd_gau(double*, double*, int, int, int, int, double);
    vector[double] cpp_mmd_lap_pval(double*, double*, int, int, int, int, int, int, double);
    vector[double] cpp_mmd_gau_pval(double*, double*, int, int, int, int, int, int, double);


cdef extern from "meammd.h":
    double cpp_meammd_proj_stat(double*, double*, int, int, int, int, int, int, double);
    vector[double] cpp_meammd_proj_pval_faster(double*, double*, int, int, int, int, int, int, int, double);
    double cpp_meammd_dist_pval(double*, double*, int, int, int, int, int,int, double, int, int);


##=========================================================================##
## Implementations; Python calling C++ functions
##=========================================================================##


def eummd(x, y, beta=-0.1, pval=True, numperm=200, seednum=0):
    '''Efficiently computes MMD and possibly the p-value.

       Args:
         - x: numpy array, sample 1.
         - y: numpy array, sample 2.
         - beta: kernel parameter for Laplacian kernel; default value is -0.1, 
                 which means that the median heuristic will be computed.
         - pval: boolean flag, if True (default), then computes p-value. 
                 If False, returns statistic and None as pval. 
         - numperm: number of permutations, default value is 200.
         - seednum: number of permutations, default value is 0, which will 
                    mean a random seed will be used. For values greater than 0, 
                    results will be reproducible.

       Details:
         - for n samples and l permutations, complexity is O(n log n + Ln).
         - if beta <= 0, computes beta = 1/mh where mh is the median heuristic,
           in O(n log n). if beta > 0, then this value is used as the kernel 
           parameter value.
         - main method implemented in C++.

       Returns:
         A dictionary consisting of:
           - pval, the p-value of the test, if it is computed 
                   (argument pval=True). Otherwise,  it is set to None.
           - stat, the statisitc used in the test, which is always computed.
           - beta, the kernel parameter used in the test. If beta was not 
                   initialised or negative, this will be the median heuristic
                   value.
    '''
    # if list, convert to numpy arrays
    if isinstance(x, list):
        x = np.array(x).astype(np.float64)
    if isinstance(y, list):
        y = np.array(y).astype(np.float64)

    # check x and y are numeric
    if isinstance(x, (np.array, np.ndarray)):
        if not is_numeric_numpy_arr(x):
            raise ValueError("x needs to be a numeric list or numpy array/matrix.")
    if isinstance(y, (np.array, np.ndarray)):
        if not is_numeric_numpy_arr(y):
            raise ValueError("y needs to be a numeric list or numpy array/matrix.")


    # if not numpy array or matrix, error
    if not isinstance(x, np.ndarray):
        raise ValueError("x needs to be a numeric numpy array/matrix, or a list.")
    if not isinstance(y, np.ndarray):
        raise ValueError("y needs to be a numeric numpy array/matrix, or a list.")

    # make sure vectors are doubles; if not, cast to float64
    if not np.issubdtype(x.dtype, np.float64):
        x = x.astype(np.float64)
    if not np.issubdtype(y.dtype, np.float64):
        y = y.astype(np.float64)

    # initialise values
    pval_val = 0
    stat_val = 0
    if pval:
        returnvec = cpp_eummd_pval_faster(x, y, beta, numperm, seednum)
        pval_val = returnvec[0]
        stat_val = returnvec[1]
        beta = returnvec[2]
    else:
        returnvec = cpp_eummd(x, y, beta)
        pval_val = None
        stat_val = returnvec[0]
        beta = returnvec[1]

    # create return dictionary
    returndict = {"pval": pval_val, "stat": stat_val, "beta":  beta}
    return returndict



def cy_naive_medianHeuristicMult(np.ndarray[double, ndim=2, mode="c"] X not None, 
                                 np.ndarray[double, ndim=2, mode="c"] Y=None,
                                 kmethod=1): 
    '''Median heuristic

    Args:
      - X np.ndarray, sample 1
      - Y np.ndarray, sample 2, could be None
      - kmethod: scalar, if 1 (default), uses Laplacian kernel. For other values, 
                 uses Gaussian kernel.

    Returns:
      Median heuristic

    Details:
      - For n samples, complexity is O(n^2).
      - Calls cpp_naive_multiv_medianHeuristic, C++ code
      - If Y is not None, concatenates with X.
    '''

    #print("in naive medianHeuristicMult")

    # get the dimensions
    nX = X.shape[0] 
    dX = X.shape[1] 
    nY = Y.shape[0] 
    dY = Y.shape[1]

    #print("X shape: ", X.shape[0], X.shape[1])
    #print("Y shape: ", Y.shape[0], Y.shape[1])

    if Y is None:
        #print("Y is None  X.shape: ")
        #print(X.shape[0], ", ", X.shape[1])
        return cpp_naive_multiv_medianHeuristic(&X[0,0], nX, dX, kmethod)

    if (dX != dY):
        raise ValueError("naive_medianheuristic: Invalid dimensions of matrices; X and Y different dimensions.")

    # concatenate X and Y
    X = np.concatenate([X, Y])

    # get the dimensions again!
    nX = X.shape[0] 
    dX = X.shape[1] 

    return cpp_naive_multiv_medianHeuristic(&X[0,0], nX, dX, kmethod)

def is_numeric_numpy_arr(x):
    '''Checks if a numpy array contains only numeric values
    '''
    isnum =  np.issubdtype(x.dtype, np.number) 
    return isnum



def mediandiff(X, Y=None, kernel="Laplacian", fast=False):
    '''Compute the median difference between the elements in the samples X 
       and Y.

       Args:
         - X: list, or numpy array, sample 1.
         - Y: list, numpy array, sample 2. Default is None, in which case
              only values in X will be used.
         - kernel: string, either "Laplacian" or "Gaussian".
         - fast: boolean; if True will run O(N log N)} algorithm, 
                 where N = n + m, but if False will run naive O(N^2 log(N)) 
                 algorithm.

       Details:
          The median difference is defined as follows:

          Z is the combined X and Y values into a single array or matrix.
          Number of columns is the dimension, and these need to be equal 
          for X and Y. Then if $N=n+m$,

          $m = median { ||z_i - z_j||_1; i=1, 2, ..., N, and j=1, 2,..., i }$ 

          where $||z_i - z_j||_1$ is the 1-norm, and so if the data 
          are $d$-dimensional then
         
          $||z_i - z_j||_1 = \sum_{k=1}^{d} |z_{i,k} - z_{j,k}|$,
         
          The median heuristic is defined as beta = 1/$m$.
         
          Naive method will compute all distinct pairs, of which there are 
          $N(N+1)/2$ differences. These are then sorted using a $O(N log(N))$ 
          algorithm, so overall $O(N^2 log(N))$. 

          The fast method is $O(N log N)$ is from Croux and Rousseeuw (1992), 
          which is based on Johnson and Mizoguchi (1978). 


       References:
          Croux, C. and Rousseeuw, P. J. (1992), 
          "Time-Efficient Algorithms for Two Highly Robust Estimators of Scale"
          In Computational Statistics: Volume 1: Proceedings of the 10th 
          Symposium on Computational Statistics (pp. 411-428).

          Johnson, D.B., and Mizoguchi, T. (1978), 
          "Selecting the Kth Element in X + Y and X_1 + X_2 + ... + X_m", 
          SIAM Journal of Computing, 7, 147-153.


       Returns:
          a scalar, the median of all pairwise differences.
    '''

    # if list, convert to numpy arrays
    if isinstance(X, list):
        X = np.array(X).astype(np.float64)
    if not (Y is None):
        if isinstance(Y, list):
            Y = np.array(Y).astype(np.float64)

    # check X and Y (if not None) are numeric
    if isinstance(X, (np.array, np.ndarray)):
        if not is_numeric_numpy_arr(X):
            raise ValueError("X needs to be a numeric list or numpy array/matrix.")
    if not (Y is None):
        if not is_numeric_numpy_arr(Y):
            raise ValueError("Y needs to be a numeric list or numpy array/matrix.")


    # if not numpy array or matrix, error
    if not isinstance(X, np.ndarray):
        raise ValueError("X needs to be a numeric numpy array/matrix, or a list.")
    if not (Y is None):
        if not isinstance(Y, np.ndarray):
            raise ValueError("Y needs to be a numeric numpy array/matrix, or a list.")
    

    # get dimensions and check
    if not (Y is None):
        if (X.ndim == 2) and (Y.ndim == 2):
            if (X.shape[1] != Y.shape[1]):
                raise ValueError("X and Y need to be vectors or have the same number of columns.")
            if fast:
                raise ValueError("Can only compute fast version when X and Y are vectors.")
        else:
            if not ((X.ndim == 1) and (Y.ndim == 1)):
                raise ValueError("X and Y need be 1- or 2-dimensional numpy arrays, or lists.")


    # check kernel
    if ((kernel != "Laplacian") and (kernel != "Gaussian") ):
        raise ValueError("kernel needs to be either 'Laplacian' or 'Gaussian'.")

    # check fast boolean flag
    if not isinstance(fast, bool):
        raise ValueError("fast needs to be a Boolean.")

    # if fast, must be univariate
    if fast and (X.ndim != 1):
        raise ValueError("fast method can only bet selected for 1-dimensional data.")


    # finally, if Y is not None, concatenate and work with X
    if Y is None:
        Z = X
    else:
        Z = np.concatenate([X, Y])

    # make sure vectors are doubles; if not, cast to float64
    if not np.issubdtype(Z.dtype, np.float64):
        Z = Z.astype(np.float64)

    # median differences
    md = 0
    if fast:
        md = medianHeuristic(Z)
        # if Gaussian kernel, square it
        if (kernel=="Gaussian"):
            md =  md**2
    else:
        # using naive method; make sure correct dimensions; make 2d array
        if (Z.ndim==1):
            Z = Z.reshape(Z.shape[0], 1)
        nZ = Z.shape[0] 
        dZ = Z.shape[1] 

        # sort out kernel
        kmethod=1
        if (kernel=="Gaussian"):
            kmethod=2

        # call internal function
        md = cy_naive_medianHeuristicMult(Z, kmethod=kmethod)
        #md = cpp_naive_multiv_medianHeuristic(&Z[0,0], nZ, dZ, kmethod)

    return md


def medianheuristic(X, Y=None, kernel="Laplacian", fast=False):
    '''Compute the median heuristc between the elements in the samples X 
       and Y.

       Args:
         - X: list, or numpy array, sample 1.
         - Y: list, numpy array, sample 2. Default is None, in which case
              only values in X will be used.
         - kernel: string, either "Laplacian" or "Gaussian".
         - fast: boolean; if True will run O(N log N)} algorithm, 
                 where N = n + m, but if False will run naive O(N^2 log(N)) 
                 algorithm.

       Details:
          The median heuristic is defined as the inverse of the median difference.
          If Z is the combined X and Y values into a single array or matrix.
          Number of columns is the dimension, and these need to be equal 
          for X and Y. Then if $N=n+m$, the median difference is defined as

          $m = median { ||z_i - z_j||_1; i=1, 2, ..., N, and j=1, 2,..., i }$ 

          where $||z_i - z_j||_1$ is the 1-norm, and so if the data 
          are $d$-dimensional then
         
          $||z_i - z_j||_1 = \sum_{k=1}^{d} |z_{i,k} - z_{j,k}|$,
         
          The median heuristic is defined as beta = 1/$m$.
         
          Naive method will compute all distinct pairs, of which there are 
          $N(N+1)/2$ differences. These are then sorted using a $O(N log(N))$ 
          algorithm, so overall $O(N^2 log(N))$. 

          The fast method is $O(N log N)$ is from Croux and Rousseeuw (1992), 
          which is based on Johnson and Mizoguchi (1978). 


       References:
          Croux, C. and Rousseeuw, P. J. (1992), 
          "Time-Efficient Algorithms for Two Highly Robust Estimators of Scale"
          In Computational Statistics: Volume 1: Proceedings of the 10th 
          Symposium on Computational Statistics (pp. 411-428).

          Johnson, D.B., and Mizoguchi, T. (1978), 
          "Selecting the Kth Element in X + Y and X_1 + X_2 + ... + X_m", 
          SIAM Journal of Computing, 7, 147-153.


       Returns:
          a scalar, the median of all pairwise differences.
    '''
    return 1.0 / mediandiff(X=X, Y=Y, kernel=kernel, fast=fast)



def cy_mmd(np.ndarray[double, ndim=2, mode="c"] X not None, 
           np.ndarray[double, ndim=2, mode="c"] Y not None,
           beta=-0.1, pval=True, kernel="Laplacian", numperm=200, seednum=0):

    # get the dimensions
    nX = X.shape[0] 
    dX = X.shape[1] 
    nY = Y.shape[0] 
    dY = Y.shape[1]

    pval_val = 0
    stat_val = 0
    if kernel == "Gaussian":
        # do Gaussian
        if pval:
            pvalstat = cpp_mmd_gau_pval(&X[0,0], &Y[0,0], nX, dX, nY, dY, numperm, seednum, beta)
            pval_val = pvalstat[0]
            stat_val = pvalstat[1]
            beta = pvalstat[2]
        else:
            statbeta = cpp_mmd_gau(&X[0,0], &Y[0,0], nX, dX, nY, dY, beta)
            pval_val = None
            stat_val = statbeta[0]
            beta = statbeta[1]
    else:
        # do Laplacian
        if pval:
            pvalstat = cpp_mmd_lap_pval(&X[0,0], &Y[0,0], nX, dX, nY, dY, numperm, seednum, beta)
            pval_val = pvalstat[0]
            stat_val = pvalstat[1]
            beta = pvalstat[2]
        else:
            statbeta = cpp_mmd_lap(&X[0,0], &Y[0,0], nX, dX, nY, dY, beta)
            pval_val = None
            stat_val = statbeta[0]
            beta = statbeta[1]

    # create return dictionary
    returndict = {"pval": pval_val, "stat": stat_val, "beta": beta}
    return returndict


def mmd(X not None, 
        Y not None,
        beta=-0.1, pval=True, kernel="Laplacian", numperm=200, seednum=0):
    '''Computes maximum mean discrepancy statistics with Laplacian 
       or Gaussian kernel. 
       Suitable for multivariate data. Naive approach, quadratic in number
       of observations.

       Args:
         - X: list, or numpy array, of observations in first sample.
         - Y: list, or numpy array, of observations in second sample.
         - beta: kernel parameter. Must be positive; if not, computes
                 median heuristic in quadratic time. Default value
                 is -0.1, which will force median heuristic to be used.
         - pval: boolean flag, if True (default), then computes p-value. 
                 If False, returns statistic and None as pval. 
         - kernel: String, either "Laplacian" or "Gaussian". 
                   Default is "Laplacian".
         - numperm: Number of permutations. Default is 200.
         - seednum: Seed number for generating permutations. Default is 0, 
                    which means seed is set randomly. For values larger than 
                    0, results will be reproducible.

        Details: 
           First checks number of columns (dimension) are equal. 
           Suppose matrix X has n rows and d columns, 
           and matrix Y has m rows; checks that Y 
           also has d columns (if not, then throws error). 
           Then flattens matrices to vectors (or, if $d=1$, they are
           already vectors.
           Then calls C++ method. If the first sample has $n$ 
           $d$-dimensional samples and the second sample has 
           $m$ $d$-dimensional samples, then the algorithm
           computes the statistic in $O( (n+m)^2 )$ time.
          
           Median difference is as follows:
          
           $m = median{ ||x_i - x_j||_1; i=1, 2, ..., n+m, and j=1, 2,..., i }$,
          
           where $||x_i - x_j||_1$ is the 1-norm, and so if the data 
           are $d$-dimensional then
          
           $||x_i - x_j||_1 = \sum_{k=1}^{d} |x_{i,k} - x_{j,k}|$,

           and finally median heuristic is beta = 1/$m$.
           This can be computed in $O( (n+m)^2 )$ time.
         
           The Laplacian kernel $k$ is defined as 
         
           $k(x,y) = exp( -beta ||x - y||_1  )$.

           Random seed is set for std::mt19937 and std::shuffle in C++.

       Returns:
         A dictionary consisting of:
           - pval, the p-value of the test, if it is computed 
                   (argument pval=True). Otherwise,  it is set to None.
           - stat, the statisitc used in the test, which is always computed.
           - beta, the kernel parameter used in the test. If beta was not 
                   initialised or negative, this will be the median heuristic
                   value.
    '''

    # if list, convert to numpy arrays
    if isinstance(X, list):
        X = np.array(X).astype(np.float64)
    if isinstance(Y, list):
        Y = np.array(Y).astype(np.float64)

    # check X and Y are numeric
    if isinstance(X, (np.array, np.ndarray)):
        if not is_numeric_numpy_arr(X):
            raise ValueError("X needs to be a numeric list or numpy array/matrix.")
    if isinstance(Y, (np.array, np.ndarray)):
        if not is_numeric_numpy_arr(Y):
            raise ValueError("Y needs to be a numeric list or numpy array/matrix.")


    # if not numpy array or matrix, error
    if not isinstance(X, np.ndarray):
        raise ValueError("X needs to be a numeric numpy array/matrix, or a list.")
    if not isinstance(Y, np.ndarray):
        raise ValueError("Y needs to be a numeric numpy array/matrix, or a list.")
    

    # get dimensions and check
    if (X.ndim == 2) and (Y.ndim == 2):
        if (X.shape[1] != Y.shape[1]):
            raise ValueError("X and Y need to be vectors or have the same number of columns.")
    else:
        if not ((X.ndim == 1) and (Y.ndim == 1)):
            raise ValueError("X and Y need be 1- or 2-dimensional numpy arrays, or lists.")

    # check pval boolean flag
    if not isinstance(pval, bool):
        raise ValueError("pval needs to be a Boolean.")

    # check kernel
    if ((kernel != "Laplacian") and (kernel != "Gaussian") ):
        raise ValueError("kernel needs to be either 'Laplacian' or 'Gaussian'.")

    # check numperm is integer
    if not isinstance(numperm, int):
        raise ValueError("numperm needs to be an integer.")

    # check numperm is integer
    if not isinstance(seednum, int):
        raise ValueError("seednum needs to be an integer.")

    # if beta is not positive, use MEDIAN HEURISTIC
    #if not (beta > 0):
    #    beta = medianheuristic(X, Y, kernel)

    # reshape the vectors, if univariate
    if (X.ndim==1):
        X = X.reshape(X.shape[0], 1)
    if (Y.ndim==1):
        Y = Y.reshape(Y.shape[0], 1)

    # make sure vectors are doubles; if not, cast to float64
    if not np.issubdtype(X.dtype, np.float64):
        X = X.astype(np.float64)
    if not np.issubdtype(Y.dtype, np.float64):
        Y = Y.astype(np.float64)


    # compute return dictionary; need second function which expects 2d array
    returndict = cy_mmd(X=X, Y=Y, beta=beta, pval=pval, kernel=kernel, 
                        numperm=numperm, seednum=seednum)
    return returndict



def cy_meammd(np.ndarray[double, ndim=2, mode="c"] X not None, 
              np.ndarray[double, ndim=2, mode="c"] Y not None,
              pval, beta, projtype, numproj, nmethod, pmethod, 
              numperm, seednum):

    #print("seednum: ", seednum)

    # get the dimensions
    nX = X.shape[0] 
    dX = X.shape[1] 
    nY = Y.shape[0] 
    dY = Y.shape[1]

    #statbeta = cpp_mmd_lap(&X[0,0], &Y[0,0], nX, dX, nY, dY, beta)
    pval_val = 0
    stat_val = 0
    if (projtype=="proj"):
        if pval:
            pvalstat = cpp_meammd_proj_pval_faster(&X[0,0], &Y[0,0], 
                                                   nX, dX, nY, dY, 
                                                   numperm, numproj, 
                                                   seednum, beta)
            pval_val = pvalstat[0]
            stat_val = pvalstat[1]
        else:
            pval_val = None
            stat_val = cpp_meammd_proj_stat(&X[0,0], &Y[0,0], nX, dX, nY, dY, 
                                            numproj, seednum, beta)

    else:
        pval_val = cpp_meammd_dist_pval(&X[0,0], &Y[0,0], nX, dX, nY, dY, 
                                        numperm, seednum, beta, pmethod, nmethod)
        stat_val = None


    # create return dictionary
    returndict = {"pval": pval_val, "stat": stat_val}
    return returndict



def meammd(X not None, 
           Y not None,
           beta=-0.1, pval=True,
           projtype="proj", numproj=20, nmethod=1, distpval="Hommel", 
           numperm=200, seednum=0):
    '''Computes maximum mean discrepancy statistics with Laplacian 
       or Gaussian kernel. 
       Suitable for multivariate data. Naive approach, quadratic in number
       of observations.

       Args:
         - X: d-dimensional numpy array, d > 1, of observations in first sample.
         - Y: d-dimensional numpy array, d > 1, of observations in second sample.
         - beta: kernel parameter. Must be positive; if not, computes
                 median heuristic in quadratic time. Default value
                 is -0.1, which will force median heuristic to be used.
         - pval: boolean flag, if True (default), then computes p-value. 
                 If False, returns statistic and None as pval. 
         - projtype: string, the type of projection used. Either "proj" for 
                     random projections (default) or \code{"dist"} for interpoint
                     distances.
         - numproj: integer, Number of projections (only used if type="proj").
                    Default is 20.
         - nmethod: Norm used for interpoint distances, if projtype="dist". 
                    Needs to be either 2 (for two-norm, default) or 
                    1 (for one-norm).
         - distpval: string, the p-value combination procedure if type="dist".
                     Options are "Hommel" (default) or "Fisher".
                     The Hommel method is preferred since the Type I error does 
                     not seem to be controlled if the Fisher method is used.
         - numperm: integer, number of permutations. Default is 200.
         - seednum: Seed number for generating permutations. Default is 0, 
                    which means seed is set randomly. For values larger than 
                    0, results will be reproducible.

       Returns:
         A dictionary consisting of:
           - pval, the p-value of the test, if it is computed 
                   (argument pval=True). Otherwise, it is set to None.
           - stat, the statisitc used in the test, which is only returned
                   when type="proj", otherwise it is set to None.
    '''
    # if not numpy array or matrix, error
    if not isinstance(X, np.ndarray):
        raise ValueError("X needs to be a numeric numpy array/matrix.")
    if not isinstance(Y, np.ndarray):
        raise ValueError("Y needs to be a numeric numpy array/matrix.")

    # check X and Y are numeric
    if not is_numeric_numpy_arr(X):
        raise ValueError("X needs to be a numeric numpy array/matrix.")

    if not is_numeric_numpy_arr(Y):
        raise ValueError("Y needs to be a numeric numpy array/matrix.")

    # check pval boolean flag
    if not isinstance(pval, bool):
        raise ValueError("pval needs to be a Boolean.")

    # get dimensions and check
    if (X.ndim != 2) or (Y.ndim != 2):
        raise ValueError("X and Y need to be 2-dimensional arrays (matrices).")
    else:
        if (X.shape[1] != Y.shape[1]):
            raise ValueError("X and Y need to have be matrices/2-dimensional arrays with the same number of columns.")

    # check projtype
    if ((projtype != "proj") and (projtype != "dist") ):
        raise ValueError("projtype needs to be either 'proj' or 'dist'.")

    if ((projtype=="dist") and (pval==False)):
        raise ValueError("if projtype is 'dist', then pval must be 'True', since MEA-MMD-Dist does not return a statistic, only a p-value.")


    # check numproj is integer
    if not isinstance(numproj, int):
        raise ValueError("numproj needs to be an integer.")

    # nmethod needs to be either 1 or 2
    if (nmethod != 1) and (nmethod != 2):
        raise ValueError("nmethod needs to be either 1 for the one-norm or 2 for the two-norm.")

    # actually, if 2, should be 0
    if (nmethod==2):
        nmethod = 0

    # check distpval
    if ((distpval != "Hommel") and (distpval != "Fisher") ):
        raise ValueError("distpval needs to be either 'Hommel' or 'Fisher'.")


    pmethod = 0
    if (distpval != "Hommel"):
        pmethod = 1

    # check numperm is integer
    if not isinstance(numperm, int):
        raise ValueError("numperm needs to be an integer.")


    # check numperm is integer
    if not isinstance(numperm, int):
        raise ValueError("numperm needs to be an integer.")

    # check numperm is integer
    if not isinstance(seednum, int):
        raise ValueError("seednum needs to be an integer.")

    # make sure vectors are doubles; if not, cast to float64
    if not np.issubdtype(X.dtype, np.float64):
        X = X.astype(np.float64)
    if not np.issubdtype(Y.dtype, np.float64):
        Y = Y.astype(np.float64)

    returndict = cy_meammd(X=X, Y=Y, beta=beta, pval=pval, projtype=projtype, 
                           numproj=numproj,
                           nmethod=nmethod, pmethod=pmethod, 
                           numperm=numperm, seednum=seednum)

    return returndict
                     
                     

