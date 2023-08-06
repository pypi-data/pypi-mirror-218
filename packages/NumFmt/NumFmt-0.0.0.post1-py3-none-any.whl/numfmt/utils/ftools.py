# import typing as _tp


class Pass:
	def __new__(cls, f):
		return f


class Not:
	def __new__(cls, f):
		def _not(*x, **y):
			return not f(*x, **y)

		return _not


class Neg:
	def __new__(cls, f):
		def _neg(*x, **y):
			return -f(*x, **y)

		return _neg


class Inv:
	def __new__(cls, f):
		def _inv(*x, **y):
			return ~f(*x, **y)

		return _inv


def fork(f):
	"""
	e.g.
		it = map(fork(print), it)
	"""

	def g(x):
		f(x)
		return x

	return g


def apply(fns):
	def f(it):
		return (g(x) for g, x in zip(fns, it))
	return f
