from ..ctypeslib import core as _core
import ctypes as _ct
import numbers as _numbers


def bisect(f, a, b, tol=1E-5, maxiter=100, method="bf", modified=False):
	assert callable(f), "f must be function"
	assert isinstance(a, _numbers.Real), "a must be real number"
	assert isinstance(b, _numbers.Real), "b must be real number"

	return _core.c_root_bisect(f, _ct.c_double(a), _ct.c_double(b), 
			_ct.c_double(tol), 
			_ct.c_int(maxiter), 
			_ct.c_char_p(method.encode('utf-8')),
			_ct.c_bool(modified))


def brentq(f, a, b, tol=1E-5, maxiter=100):
	assert callable(f), "f must be function"
	assert isinstance(a, _numbers.Real), "a must be real number"
	assert isinstance(b, _numbers.Real), "b must be real number"

	return _core.c_root_brentq(f, _ct.c_double(a), _ct.c_double(b), _ct.c_double(tol), _ct.c_int(maxiter))


def muller(f, x0, h=None, x1=None, x2=None, tol=1E-5, maxiter=100):
	assert callable(f), "f must be function"
	assert isinstance(x0, _numbers.Complex), "x0 must be a Complex/Real number"
	
	return _core.c_root_muller(f, x0, h, x1, x2, _ct.c_double(tol), _ct.c_int(maxiter))


def newton(f, x0, x1=None, fprime=None, tol=1E-5, maxiter=100):
	assert callable(f), "f must be function"
	if(fprime == None):
		assert isinstance(x1, _numbers.Real), "If fprime not provided, x1 must be a real number"
	else:
		assert callable(fprime), "If fprime is provided, it must be of type function."

	return _core.c_root_newton(f, _ct.c_double(x0), x1, fprime, _ct.c_double(tol), _ct.c_int(maxiter))


def ridder(f, a, b, tol=1E-5, maxiter=100):
	assert callable(f), "f must be function"
	assert isinstance(a, _numbers.Real), "a must be real number"
	assert isinstance(b, _numbers.Real), "b must be real number"
	
	return _core.c_root_ridder(f, _ct.c_double(a), _ct.c_double(b), _ct.c_double(tol), _ct.c_int(maxiter))



from .fsolve import fsolve


