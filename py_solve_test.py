# https://aleksandarhaber.com/solve-systems-of-nonlinear-equations-in-python-by-using-fsolve/

import numpy as np
from scipy.optimize import fsolve

# https://realpython.com/python-pretty-print/
from pprint import pprint


# for a given variable w, this function returns F(w)
# if w is the solution of the nonlinear system, then
# F(w)=0
# F can be interpreted as the residual

i=0
def nonlinearEquation(w):

    global i

    F=np.zeros(3)
    F[0]=2*w[0]**2+w[1]**2+w[2]**2-15
    F[1]=w[0]+w[1]+2*w[2]-9
    F[2]=w[0]*w[1]*w[2]-6

    # https://pythonguides.com/python-numpy-sum/
    sum_of_squares = np.dot(F, F)

    print(f"{i}:\tw: {w} \n\tF: {F}\n\tsum_of_squares: {sum_of_squares}")
    i += 1
    return F

# generate an initial guess
initialGuess=np.random.rand(3)

# solve the problem
solutionInfo=fsolve(nonlinearEquation,initialGuess,full_output=1)

pprint(solutionInfo)



