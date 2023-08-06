import unittest
import numpy as np

from eummd import eummd
from eummd import mediandiff
from eummd import medianheuristic
from eummd import is_numeric_numpy_arr
from eummd import mmd 
from eummd import meammd 


# for generating numbers from pi
def getndfrompi(n, d):
    # pi to 100 digits, apparently
    pidigits = [3,1,4,1,5,9,2,6,5,3,5,8,9,7,9,3,2,3,8,4,6,2,6,4,3,3,8,3,2,7,9,5,0,2,8,8,4,1,9,7,1,6,9,3,9,9,3,7,5,1,0,5,8,2,0,9,7,4,9,4,4,5,9,2,3,0,7,8,1,6,4,0,6,2,8,6,2,0,8,9,9,8,6,2,8,0,3,4,8,2,5,3,4,2,1,1,7,0,6,7,9,8]
    x = np.zeros(n)
    # location
    loc = 0
    for i in range(n):
        xi = 0
        for j in range(d):
            xi = xi + pidigits[loc] * (0.1**j)
            loc += 1
        x[i] = xi
    return x


class BasicTests(unittest.TestCase):

    def test_basic1(self):
        '''Testing if two numbers are equal, just to get started
        '''
        x = 0
        y = 0
        self.assertEqual(x, y)

    def test_basic2(self):
        '''Testing if two numbers are equal, just to get started
        '''
        x = 1
        self.assertEqual(x, 1)

    def test_is_numeric_numpy_arr1(self):
        '''Testing if numpy array only contains numeric values, True
        '''
        X = np.array([7.1, 1.2, 4.3, 0.4]).astype(np.float64)
        self.assertTrue(is_numeric_numpy_arr(X))

    def test_is_numeric_numpy_arr2(self):
        '''Testing if 2D numpy array only contains numeric values, True
        '''
        X = np.array([[7.1, 1.2, 4.3, 0.4], [5, 6, 7, 0.8]]).astype(np.float64)
        self.assertTrue(is_numeric_numpy_arr(X))


    def test_is_numeric_numpy_arr3(self):
        '''Testing if 2D numpy array only contains numeric values, False
        '''
        xlist = [7.1, 1.2, 'a', 0.4]
        X = np.array(xlist)
        self.assertFalse(is_numeric_numpy_arr(X))


    def test_is_numeric_numpy_arr4(self):
        '''Testing if 2D numpy array only contains numeric values, False
        '''
        X = np.array([[7.1, 1.2, 4.3, 0.4], [5, 6, 'a', 0.8]])
        self.assertFalse(is_numeric_numpy_arr(X))

class Getndfrompi_Tests(unittest.TestCase):

    def test_1_1_singledigit(self):
        """Single digit
        """
        ans1 = getndfrompi(4, 1)
        soln1 = np.array([3, 1, 4, 1])
        #self.assertFalse(False)
        np.testing.assert_allclose(ans1, soln1, rtol=1e-5, atol=0)


    def test_1_2_onedecimal(self):
        """One decimal place
        """
        ans2 = getndfrompi(5, 2)
        soln2 = np.array([3.1, 4.1, 5.9, 2.6, 5.3])
        np.testing.assert_allclose(ans2, soln2, rtol=1e-5, atol=0)


    def test_1_3_twodecimals(self):
        """Two decimal places
        """
        ans3 = getndfrompi(6, 3)
        soln3 = np.array([3.14, 1.59, 2.65, 3.58, 9.79, 3.23])
        np.testing.assert_allclose(ans3, soln3, rtol=1e-5, atol=0)


    def test_1_4_threedecimals(self):
        """Three decimal places
        """
        ans4 = getndfrompi(7, 4)
        soln4 = np.array([3.141, 5.926, 5.358, 9.793, 2.384, 6.264, 3.383])
        np.testing.assert_allclose(ans4, soln4, rtol=1e-5, atol=0)




class eummd_stat_Tests(unittest.TestCase):

    def test_2_1_eummd_pval_1(self):
        """ eummd, univariate, no pval, positive beta
        """
        X = np.array([7.1, 1.2, 4.3, 0.4]).astype(np.float64)
        Y = np.array([5.5, 2.6, 8.7]).astype(np.float64)
        beta = 0.1

        # get cython emmd with MH
        ans = eummd(X, Y, beta, pval=False)
        soln_pval = None
        soln_stat = -0.0594780368951533
        soln_beta = 0.1

        self.assertTrue(ans['pval'] is None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['beta'], soln_beta, places=11, msg=None, delta=None)

    def test_2_2_eummd_pval_1(self):
        """ eummd, univariate, no pval, negative beta
        """
        X = np.array([7.1, 1.2, 4.3, 0.4]).astype(np.float64)
        Y = np.array([5.5, 2.6, 8.7]).astype(np.float64)
        beta = -0.1

        # get cython emmd with MH
        ans = eummd(X, Y, beta, pval=False)
        soln_pval = None
        soln_stat = -0.129327129453085
        soln_beta = 1.0/3.2

        self.assertTrue(ans['pval'] is None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['beta'], soln_beta, places=11, msg=None, delta=None)



class eummd_pval_Tests(unittest.TestCase):

    def test_3_1_eummd_pval_1(self):
        """ eummd, univariate, pval, negative beta
        """
        X = np.array([7.1, 1.2, 4.3, 0.4]).astype(np.float64)
        Y = np.array([5.5, 2.6, 8.7]).astype(np.float64)
        beta = -0.1
        seednum = 1
        numperm = 200


        # get cython emmd with MH
        ans = eummd(X, Y, beta=beta, numperm=numperm, seednum=seednum)
        soln_pval = 0.5472636815920398
        soln_stat = -0.129327129453085
        soln_beta = 1.0/3.2

        self.assertAlmostEqual(ans['pval'], soln_pval, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['beta'], soln_beta, places=11, msg=None, delta=None)

    def test_3_2_eummd_pval_2(self):
        """ eummd, univariate, pval, negative beta, uses lists
        """
        X = [7.1, 1.2, 4.3, 0.4]
        Y = [5.5, 2.6, 8.7]
        beta = -0.1
        seednum = 1
        numperm = 200

        # get cython emmd with MH
        ans = eummd(X, Y, beta=beta, numperm=numperm, seednum=seednum)
        soln_pval = 0.5472636815920398
        soln_stat = -0.129327129453085
        soln_beta = 1.0/3.2

        self.assertAlmostEqual(ans['pval'], soln_pval, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['beta'], soln_beta, places=11, msg=None, delta=None)


class medianHeuristic_Tests(unittest.TestCase):

    def test_4_1_medianHeuristic(self):
        """ mediandiff, univariate, fast
        """

        X = np.array([7.1, 1.2, 4.3, 0.4]).astype(np.float64)
        Y = np.array([5.5, 2.6, 8.7]).astype(np.float64)

        ans = mediandiff(X, Y, kernel="Laplacian", fast=True)
        soln = 3.2
        self.assertAlmostEqual(ans, soln, places=11, msg=None, delta=None)


    def test_4_2_medianHeuristic(self):
        """ mediandiff, univariate, NOT fast
        """

        X = np.array([7.1, 1.2, 4.3, 0.4]).astype(np.float64)
        Y = np.array([5.5, 2.6, 8.7]).astype(np.float64)

        ans = mediandiff(X, Y, kernel="Laplacian", fast=False)
        soln = 3.2
        self.assertAlmostEqual(ans, soln, places=11, msg=None, delta=None)


    def test_4_3_medianHeuristic(self):
        """ mediandiff, univariate, NOT fast
        """

        X = np.array([7.1, 1.2, 4.3, 0.4]).astype(np.float64)
        Y = np.array([5.5, 2.6, 8.7]).astype(np.float64)

        ans = mediandiff(X, Y, fast=False)
        soln = 3.2
        self.assertAlmostEqual(ans, soln, places=11, msg=None, delta=None)


    def test_4_4_medianHeuristic(self):
        """ mediandiff, univariate, defaults
        """

        X = np.array([7.1, 1.2, 4.3, 0.4]).astype(np.float64)
        Y = np.array([5.5, 2.6, 8.7]).astype(np.float64)

        ans = mediandiff(X, Y)
        soln = 3.2
        self.assertAlmostEqual(ans, soln, places=11, msg=None, delta=None)


    def test_4_5_medianHeuristic(self):
        """ mediandiff, univariate, Y is None
        """

        X = np.array([7.1, 1.2, 4.3, 0.4]).astype(np.float64)
        Y = np.array([5.5, 2.6, 8.7]).astype(np.float64)
        Z = np.concatenate([X, Y])

        ans = mediandiff(Z)
        soln = 3.2
        self.assertAlmostEqual(ans, soln, places=11, msg=None, delta=None)


    def test_4_6_medianHeuristic(self):
        """ mediandiff, univariate, Gaussian kernel, fast
        """

        X = np.array([7.1, 1.2, 4.3, 0.4]).astype(np.float64)
        Y = np.array([5.5, 2.6, 8.7]).astype(np.float64)

        ans = mediandiff(X, Y, kernel="Gaussian", fast=True)
        soln = 10.24
        self.assertAlmostEqual(ans, soln, places=11, msg=None, delta=None)


    def test_4_7_medianHeuristic(self):
        """ mediandiff, univariate, Gaussian kernel, NOT fast
        """

        X = np.array([7.1, 1.2, 4.3, 0.4]).astype(np.float64)
        Y = np.array([5.5, 2.6, 8.7]).astype(np.float64)

        ans = mediandiff(X, Y, kernel="Gaussian", fast=False)
        soln = 10.24
        self.assertAlmostEqual(ans, soln, places=11, msg=None, delta=None)


    def test_4_8_medianHeuristic(self):
        """ mediandiff, univariate, wrong kernel, throws error
        """

        X = np.array([7.1, 1.2, 4.3, 0.4]).astype(np.float64)
        Y = np.array([5.5, 2.6, 8.7]).astype(np.float64)

        with self.assertRaises(ValueError):
            ans = mediandiff(X, Y, kernel="Blah", fast=False) 


    def test_4_9_medianHeuristic(self):
        """ medianheuristic, univariate, Gaussian kernel, fast
        """

        X = np.array([7.1, 1.2, 4.3, 0.4]).astype(np.float64)
        Y = np.array([5.5, 2.6, 8.7]).astype(np.float64)

        ans = medianheuristic(X, Y, kernel="Gaussian", fast=True)
        soln = 1.0/10.24
        self.assertAlmostEqual(ans, soln, places=11, msg=None, delta=None)


    def test_4_10_medianHeuristic(self):
        """ medianheuristic, univariate, Laplacian kernel (default), fast
        """

        X = np.array([7.1, 1.2, 4.3, 0.4]).astype(np.float64)
        Y = np.array([5.5, 2.6, 8.7]).astype(np.float64)

        ans = medianheuristic(X, Y, fast=True)
        soln = 1.0/3.2
        self.assertAlmostEqual(ans, soln, places=11, msg=None, delta=None)


    def test_4_11_medianHeuristic(self):
        """ mediandiff, multivariate, Laplacian kernel 
        """

        X = np.array(range(1, 13)).astype(np.float64).reshape((6,2))
        Y = np.array(range(13, 21)).astype(np.float64).reshape((4,2))

        # X = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]).astype(np.float64)
        # Y = np.array([[13, 14, 15, 16], [17, 18, 19, 20]]).astype(np.float64)
        ans = mediandiff(X, Y, fast=False)
        soln = 12.0
        self.assertAlmostEqual(ans, soln, places=11, msg=None, delta=None)


    def test_4_12_medianHeuristic(self):
        """ mediandiff, multivariate, Gaussian kernel 
        """

        X = np.array(range(1, 13)).astype(np.float64).reshape((6,2))
        Y = np.array(range(13, 21)).astype(np.float64).reshape((4,2))
        ans = mediandiff(X, Y, kernel="Gaussian", fast=False)
        soln = 72.0
        self.assertAlmostEqual(ans, soln, places=11, msg=None, delta=None)

    def test_4_13_medianHeuristic(self):
        """ medianheuristic, multivariate, Laplacian kernel 
        """

        X = np.array(range(1, 13)).astype(np.float64).reshape((6,2))
        Y = np.array(range(13, 21)).astype(np.float64).reshape((4,2))
        ans = medianheuristic(X, Y, fast=False)
        soln = 1.0/12.0
        self.assertAlmostEqual(ans, soln, places=11, msg=None, delta=None)


    def test_4_14_medianHeuristic(self):
        """ medianheuristic, multivariate, Gaussian kernel 
        """

        X = np.array(range(1, 13)).astype(np.float64).reshape((6,2))
        Y = np.array(range(13, 21)).astype(np.float64).reshape((4,2))
        ans = medianheuristic(X, Y, kernel="Gaussian", fast=False)
        soln = 1.0/72.0
        self.assertAlmostEqual(ans, soln, places=11, msg=None, delta=None)


    def test_4_15_medianHeuristic(self):
        """ mediandiff, multivariate, error
        """

        X = np.array(range(1, 13)).astype(np.float64).reshape((12,1))
        Y = np.array(range(13, 21)).astype(np.float64).reshape((4,2))
        with self.assertRaises(ValueError):
            ans = medianheuristic(X, Y)

    def test_4_16_medianHeuristic(self):
        """ mediandiff, multivariate, error
        """
        X = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 'a', 12]])
        Y = np.array([[13, 14, 15, 16], [17, 18, 19, 20]])
        with self.assertRaises(ValueError):
            ans = medianheuristic(X, Y)
        

class naive_mmd_Tests(unittest.TestCase):

    def test_5_1_mmd_naive_lap1(self):
        """ mmd, univariate, no pval, positive beta
        """
        X = np.array([7.1, 1.2, 4.3, 0.4]).astype(np.float64)
        Y = np.array([5.5, 2.6, 8.7]).astype(np.float64)
        beta = 0.1

        # get cython emmd with MH
        ans = mmd(X=X, Y=Y, beta=beta, pval=False, kernel="Laplacian")
        soln_pval = None
        soln_stat = -0.0594780368951533 
        soln_beta = 0.1 

        self.assertTrue(ans['pval'] is None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['beta'], soln_beta, places=11, msg=None, delta=None)


    def test_5_2_mmd_naive_lap2(self):
        """ mmd, univariate, pval, negative beta
        """
        X = np.array([7.1, 1.2, 4.3, 0.4]).astype(np.float64)
        Y = np.array([5.5, 2.6, 8.7]).astype(np.float64)
        beta = -0.1
        numperm = 200
        seednum = 1

        # get cython emmd with MH
        ans = mmd(X=X, Y=Y, beta=beta, pval=True, kernel="Laplacian", 
                  numperm=numperm, seednum=seednum)
        soln_pval = 0.6169154228855721
        soln_stat = -0.129327129453085
        soln_beta = 0.3125

        self.assertAlmostEqual(ans['pval'], soln_pval, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['beta'], soln_beta, places=11, msg=None, delta=None)
 

    def test_5_3_mmd_naive_gau1(self):
        """ mmd, univariate, no pval, negative beta, Gaussian
        """
        X = np.array([7.1, 1.2, 4.3, 0.4]).astype(np.float64)
        Y = np.array([5.5, 2.6, 8.7]).astype(np.float64)
        beta = -0.1

        # get cython emmd with MH
        ans = mmd(X=X, Y=Y, beta=beta, pval=False, kernel="Gaussian")
        soln_pval = None
        soln_stat = -0.23854934793632165
        soln_beta = 0.09765625

        self.assertTrue(ans['pval'] is None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['beta'], soln_beta, places=11, msg=None, delta=None)


    def test_5_4_mmd_naive_gau2(self):
        """ mmd, univariate, pval, negative beta, Gaussian
        """
        X = np.array([7.1, 1.2, 4.3, 0.4]).astype(np.float64)
        Y = np.array([5.5, 2.6, 8.7]).astype(np.float64)
        beta = -0.1
        numperm = 200
        seednum = 1

        # get cython emmd with MH
        ans = mmd(X=X, Y=Y, beta=beta, pval=True, kernel="Gaussian", 
                  numperm=numperm, seednum=seednum)
        soln_pval = 0.58706467662
        soln_stat = -0.23854934793632165
        soln_beta = 0.09765625

        self.assertAlmostEqual(ans['pval'], soln_pval, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['beta'], soln_beta, places=11, msg=None, delta=None)


    def test_5_5_mmd_naive_lap3(self):
        """ mmd, bivariate, no pval, positive beta
        """
        beta = 0.1
        X = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]).reshape((6, 2))
        Y = np.array([[13, 14, 15, 16], [17, 18, 19, 20]]).reshape((4, 2))

        # get cython emmd with MH
        ans = mmd(X=X, Y=Y, beta=beta, pval=False, kernel="Laplacian")
        soln_pval = None
        soln_stat = 0.6016073536188107
        soln_beta = 0.1 

        self.assertTrue(ans['pval'] is None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['beta'], soln_beta, places=11, msg=None, delta=None)


    def test_5_6_mmd_naive_gau3(self):
        """ mmd, bivariate, no pval, positive beta, Gaussian
        """
        beta = 0.1
        X = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]).reshape((6, 2))
        Y = np.array([[13, 14, 15, 16], [17, 18, 19, 20]]).reshape((4, 2))

        # get cython emmd with MH
        ans = mmd(X=X, Y=Y, beta=beta, pval=False, kernel="Gaussian")
        soln_pval = None
        soln_stat = 0.3547468937852599
        soln_beta = 0.1 

        self.assertTrue(ans['pval'] is None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['beta'], soln_beta, places=11, msg=None, delta=None)


    def test_5_7_mmd_naive_lap4(self):
        """ mmd, bivariate, no pval, negative beta
        """
        beta = -0.1
        X = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]).reshape((6, 2))
        Y = np.array([[13, 14, 15, 16], [17, 18, 19, 20]]).reshape((4, 2))

        # get cython emmd with MH
        ans = mmd(X=X, Y=Y, beta=beta, pval=False, kernel="Laplacian")
        soln_pval = None
        soln_stat = 0.614627996988544
        soln_beta = 1.0 / 12 

        self.assertTrue(ans['pval'] is None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['beta'], soln_beta, places=11, msg=None, delta=None)


    def test_5_8_mmd_naive_gau(self):
        """ mmd, bivariate, no pval, negative beta
        """
        beta = -0.1
        X = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]).reshape((6, 2))
        Y = np.array([[13, 14, 15, 16], [17, 18, 19, 20]]).reshape((4, 2))

        # get cython emmd with MH
        ans = mmd(X=X, Y=Y, beta=beta, pval=False, kernel="Gaussian")
        soln_pval = None
        soln_stat = 0.9341789662923607
        soln_beta = 1.0 / 72 

        self.assertTrue(ans['pval'] is None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['beta'], soln_beta, places=11, msg=None, delta=None)


    def test_5_9_mmd_naive_lap(self):
        """ mmd, bivariate, pval, positive beta
        """
        beta = 0.1
        X = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]).reshape((6, 2))
        Y = np.array([[13, 14, 15, 16], [17, 18, 19, 20]]).reshape((4, 2))

        # get cython emmd with MH
        ans = mmd(X=X, Y=Y, beta=beta, pval=False, kernel="Laplacian")
        soln_pval = 0.00995024875621886
        soln_stat = 0.6016073536188107
        soln_beta = 0.1 

        self.assertTrue(ans['pval'] is None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['beta'], soln_beta, places=11, msg=None, delta=None)


    def test_5_10_mmd_naive_gau(self):
        """ mmd, bivariate, pval, positive beta, Gaussian
        """
        beta = 0.1
        X = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]).reshape((6, 2))
        Y = np.array([[13, 14, 15, 16], [17, 18, 19, 20]]).reshape((4, 2))

        # get cython emmd with MH
        ans = mmd(X=X, Y=Y, beta=beta, pval=False, kernel="Gaussian")
        soln_pval = 0.00995024875621886
        soln_stat = 0.3547468937852599
        soln_beta = 0.1 

        self.assertTrue(ans['pval'] is None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['beta'], soln_beta, places=11, msg=None, delta=None)


    def test_5_11_mmd_naive_lap(self):
        """ mmd, bivariate, pval, negative beta
        """
        beta = -0.1
        X = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]).reshape((6, 2))
        Y = np.array([[13, 14, 15, 16], [17, 18, 19, 20]]).reshape((4, 2))

        # get cython emmd with MH
        ans = mmd(X=X, Y=Y, beta=beta, pval=False, kernel="Laplacian")
        soln_pval = 0.029850746268656803
        soln_stat = 0.614627996988544
        soln_beta = 1.0/12.0 

        self.assertTrue(ans['pval'] is None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['beta'], soln_beta, places=11, msg=None, delta=None)


    def test_5_12_mmd_naive_gau(self):
        """ mmd, bivariate, pval, negative beta, Gaussian
        """
        beta = -0.1
        X = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]).reshape((6, 2))
        Y = np.array([[13, 14, 15, 16], [17, 18, 19, 20]]).reshape((4, 2))

        # get cython emmd with MH
        ans = mmd(X=X, Y=Y, beta=beta, pval=False, kernel="Gaussian")
        soln_pval = 0.03921568627450989
        soln_stat = 0.9341789662923607
        soln_beta = 1.0 / 72.0 

        self.assertTrue(ans['pval'] is None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['beta'], soln_beta, places=11, msg=None, delta=None)



    def test_5_13_mmd_naive_errorcheck1(self):
        """ mmd, bivariate, error checks, not numeric
        """
        beta = -0.1
        X = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]).reshape((6, 2))
        Y = np.array([[13, 14, 15, 'a'], [17, 18, 19, 20]]).reshape((4, 2))

        with self.assertRaises(ValueError):
            ans = mmd(X=X, Y=Y, beta=beta, pval=False, kernel="Gaussian")


    def test_5_14_mmd_naive_errorcheck2(self):
        """ mmd, bivariate, error checks, wrong dimension
        """
        beta = -0.1
        X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]).reshape((12, 1))
        Y = np.array([[13, 14, 15, 16], [17, 18, 19, 20]]).reshape((4, 2))

        with self.assertRaises(ValueError):
            ans = mmd(X=X, Y=Y, beta=beta, pval=False, kernel="Gaussian")



    def test_5_15_mmd_naive_errorcheck2(self):
        """ mmd, bivariate, error checks, lists not numeric
        """
        beta = -0.1
        X = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        Y = ['a', 14, 15, 16, 17, 18, 19, 20]

        with self.assertRaises(ValueError):
            ans = mmd(X=X, Y=Y, beta=beta, pval=False, kernel="Gaussian")


    def test_5_16_mmd_naive_gau2(self):
        """ mmd, univariate, pval, negative beta, Gaussian, with list, works
        """
        X = [7.1, 1.2, 4.3, 0.4]
        Y = [5.5, 2.6, 8.7]
        beta = -0.1
        numperm = 200
        seednum = 1

        # get cython emmd with MH
        ans = mmd(X=X, Y=Y, beta=beta, pval=True, kernel="Gaussian", 
                  numperm=numperm, seednum=seednum)
        soln_pval = 0.58706467662
        soln_stat = -0.23854934793632165
        soln_beta = 0.09765625

        self.assertAlmostEqual(ans['pval'], soln_pval, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['beta'], soln_beta, places=11, msg=None, delta=None)


class meammd_Tests(unittest.TestCase):

    def test_6_1_meammd_proj_stat(self):
        """ meammd, bivariate, proj, stat, no pval, positive beta
        """
        beta = 0.1
        X = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]).reshape((6, 2))
        Y = np.array([[13, 14, 15, 16], [17, 18, 19, 20]]).reshape((4, 2))
        numperm=200
        numproj=20
        projtype="proj"
        pval=False
        seednum=1


        # get cython emmd with MH
        ans = meammd(X=X, Y=Y, beta=beta, pval=pval, projtype=projtype,
                     numproj=numproj, nmethod=1, distpval="Hommel",
                     numperm=numperm, seednum=seednum)
        soln_pval = None
        soln_stat = 0.6057143245724294
        self.assertTrue(ans['pval'] is None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)


    def test_6_2_meammd_proj_stat(self):
        """ meammd, bivariate, proj, no stat, pval, negative beta
        """
        beta = -0.1
        X = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]).reshape((6, 2))
        Y = np.array([[13, 14, 15, 16], [17, 18, 19, 20]]).reshape((4, 2))
        numperm=200
        numproj=20
        projtype="proj"
        pval=False
        seednum=1


        # get cython emmd with MH
        ans = meammd(X=X, Y=Y, beta=beta, pval=pval, projtype=projtype,
                     numproj=numproj, nmethod=1, distpval="Hommel",
                     numperm=numperm, seednum=seednum)
        soln_pval = None
        soln_stat = 0.6146279969885438
        self.assertTrue(ans['pval'] is None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)


    def test_6_3_meammd_dist_error(self):
        """ meammd, bivariate, dist, error
        """
        beta = 0.1
        X = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]).reshape((6, 2))
        Y = np.array([[13, 14, 15, 16], [17, 18, 19, 20]]).reshape((4, 2))
        numperm=200
        numproj=20
        projtype="dist"
        pval=False
        seednum=1
        with self.assertRaises(ValueError):
            # get cython emmd with MH
            ans = meammd(X=X, Y=Y, beta=beta, pval=pval, projtype=projtype,
                         numproj=numproj, nmethod=1, distpval="Hommel",
                         numperm=numperm, seednum=seednum)



    def test_6_4_meammd_proj_stat_pval(self):
        """ meammd, bivariate, proj, stat, pval, negative beta
        """
        beta = -0.1
        X = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]).reshape((6, 2))
        Y = np.array([[13, 14, 15, 16], [17, 18, 19, 20]]).reshape((4, 2))
        numperm=200
        numproj=20
        projtype="proj"
        pval=True
        nmethod=1
        seednum=0
        X = X.astype(np.float64)
        Y = Y.astype(np.float64)
        ans = meammd(X=X, Y=Y, beta=beta, pval=pval, projtype=projtype,
                     numproj=numproj, nmethod=2, distpval="Hommel",
                     numperm=numperm, seednum=seednum)

        soln_pval = 0
        if soln_pval == 0:
            soln_pval = 0.5/ (numperm+1)
        soln_stat = 0.5838965971391168
        self.assertAlmostEqual(ans['pval'], soln_pval, places=11, msg=None, delta=None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=11, msg=None, delta=None)

        #ans2 = cy_meammd_proj_stat(X, Y, numproj=20, seednum=0, beta=-0.1)
        #ans3 = meammd(X=X, Y=Y, beta=beta, pval=False, projtype=projtype,
        #             numproj=numproj, nmethod=1, distpval="Hommel",
        #             numperm=numperm, seednum=seednum)
        #soln_stat2 = ans3['stat']
        #self.assertAlmostEqual(ans2, soln_stat2, places=11, msg=None, delta=None)



    def test_6_5_meammd_proj_stat_pval(self):
        """ meammd, bivariate, proj, stat, pval, negative beta, pi data, seed 1
        """
        beta = -0.1
        Z = getndfrompi(20, 3)
        X = Z[:12].reshape((6, 2)).astype(np.float64)
        Y = Z[12:].reshape((4,2)).astype(np.float64)
        numperm=200
        numproj=20
        projtype="proj"
        pval=True
        nmethod=1
        seednum=1
        X = X.astype(np.float64)
        Y = Y.astype(np.float64)
        ans = meammd(X=X, Y=Y, beta=beta, pval=pval, projtype=projtype,
                     numproj=numproj, nmethod=2, distpval="Hommel",
                     numperm=numperm, seednum=seednum)

        soln_pval = 0.00995024875621886
        if soln_pval == 0:
            soln_pval = 0.5/ (numperm+1)
        soln_stat = -0.0889076401603383
        self.assertAlmostEqual(ans['pval'], soln_pval, places=9, msg=None, delta=None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=9, msg=None, delta=None)



    def test_6_6_meammd_proj_stat_pval(self):
        """ meammd, bivariate, proj, stat, pval, negative beta, pi data, seed 2
        """
        beta = -0.1
        Z = getndfrompi(20, 3)
        X = Z[:12].reshape((6, 2)).astype(np.float64)
        Y = Z[12:].reshape((4,2)).astype(np.float64)
        numperm=200
        numproj=20
        projtype="proj"
        pval=True
        nmethod=1
        seednum=2
        X = X.astype(np.float64)
        Y = Y.astype(np.float64)
        ans = meammd(X=X, Y=Y, beta=beta, pval=pval, projtype=projtype,
                     numproj=numproj, nmethod=2, distpval="Hommel",
                     numperm=numperm, seednum=seednum)

        soln_pval = 0.00995024875621886
        if soln_pval == 0:
            soln_pval = 0.5/ (numperm+1)
        soln_stat = -0.06682145578647423
        self.assertAlmostEqual(ans['pval'], soln_pval, places=9, msg=None, delta=None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=9, msg=None, delta=None)


    def test_6_7_meammd_proj_stat_pval(self):
        """ meammd, bivariate, proj, stat, pval, negative beta, pi data, seed 3
        """
        beta = -0.1
        Z = getndfrompi(20, 3)
        X = Z[:12].reshape((6, 2)).astype(np.float64)
        Y = Z[12:].reshape((4,2)).astype(np.float64)
        numperm=50
        numproj=20
        projtype="proj"
        pval=True
        nmethod=1
        seednum=3
        X = X.astype(np.float64)
        Y = Y.astype(np.float64)
        ans = meammd(X=X, Y=Y, beta=beta, pval=pval, projtype=projtype,
                     numproj=numproj, nmethod=2, distpval="Hommel",
                     numperm=numperm, seednum=seednum)

        soln_pval = 0.03921568627450989
        if soln_pval == 0:
            soln_pval = 0.5/ (numperm+1)
        soln_stat = -0.05168408059151506
        self.assertAlmostEqual(ans['pval'], soln_pval, places=9, msg=None, delta=None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=9, msg=None, delta=None)



    def test_6_8_meammd_proj_stat_pval_threecols(self):
        """ meammd, bivariate, proj, stat, pval, negative beta, pi data, seed 3, 3 col
        """
        beta = -0.1
        Z = getndfrompi(33, 3)
        X = Z[:21].reshape((7, 3)).astype(np.float64)
        Y = Z[21:].reshape((4, 3)).astype(np.float64)
        numperm=50
        numproj=20
        projtype="proj"
        pval=True
        nmethod=1
        seednum=3
        X = X.astype(np.float64)
        Y = Y.astype(np.float64)
        ans = meammd(X=X, Y=Y, beta=beta, pval=pval, projtype=projtype,
                     numproj=numproj, nmethod=2, distpval="Hommel",
                     numperm=numperm, seednum=seednum)

        soln_pval = 0.03921568627450989
        if soln_pval == 0:
            soln_pval = 0.5/ (numperm+1)
        soln_stat =  -0.026413152602165535
        self.assertAlmostEqual(ans['pval'], soln_pval, places=9, msg=None, delta=None)
        self.assertAlmostEqual(ans['stat'], soln_stat, places=9, msg=None, delta=None)
