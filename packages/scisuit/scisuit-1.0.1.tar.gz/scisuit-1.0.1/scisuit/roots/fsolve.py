import numbers
import types
import numpy as np


__all__ = ['fsolve']


def fsolve(F:list, x0:list, tol=1E-5, maxiter=100 ):
	"""
	F: a list of functions <br>
	x0: a list of initial values <br>

	Solves a system of non-linear equations using Newton's approach
	Funcs contains table of equations in the format of f(x1,x2,...)=0
	v initial starting vector

	USAGE EXAMPLE

	def f1(t): return t[0]**2 + t[1]**2 - 5
	def f2(t): return t[0]**2 - t[1]**2 - 1
	roots, iter=fsolve([f1,f2], [1,1])
	print(roots, "  iter:", iter) 1.73205	1.41421	iter:5
	print(f1(roots), " ", f2(roots)) 9.428e-09    9.377e-09 
	
	"""
	assert isinstance(F, list), "F must be a list of functions"
	assert isinstance(x0, list), "a must be a number"

	assert isinstance(tol, numbers.Number) and tol>0, "tol must be a positive number"
	assert isinstance(maxiter, int) and maxiter>0, "maxiter must be a positive integer"

	dim = len(F)

	assert dim>=2, "At least 2 functions are required"
	assert dim == len(x0), "F and x0 must have same length"


	#solution vector as floating point
	v = np.asfarray(x0)
      
	#values of each function	
	Fvals = np.zeros(dim)

	Jacobi = np.zeros((dim, dim)) 

	for iter in range(maxiter):
		maxfuncval = 0 #convergence criteria
	
		for i in range(dim):
			func = F[i]     #function

			assert isinstance(func, types.FunctionType), "Entries of F must be functions of form f(t) = 0"
			
			Fvals[i] = func(v.tolist())
		
			for j in range(dim):
				oldval = v[j]
				
				#Note that vector contains (xi+dx,...)
				v[j] += tol  
				
				#evaluate function with (xi+dx,...)
				f_dxi = func(v.tolist()) 
				
				#restore the old value, vector again contains (xi,...)
				v[j] = oldval
				
				#evaluate function with (xi,...)
				f_xi = func(v.tolist())  
				
				if(abs(maxfuncval) < abs(f_xi)): 
					maxfuncval = abs(f_xi) 
				
				#register the derivative with respect to xi to Jacobian matrix
				Jacobi[i, j] = (f_dxi - f_xi) / tol


		#return solution vector and number of iterations
		if(abs(maxfuncval) < tol): 
			return v.tolist(),  iter

		DetJacobi = abs(np.linalg.det(Jacobi))
            
		if(DetJacobi <= tol):
			raise RuntimeError("At iter="+ str(iter) + " Jacobian Det=" + str(DetJacobi) + ", try different initial values") 
			
		v = v - np.linalg.solve(Jacobi, Fvals)

