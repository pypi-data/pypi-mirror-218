import typing as _tp


T = _tp.TypeVar('T')
I = _tp.TypeVar('I')
S = _tp.TypeVar('S')


def bits(n: int) -> int:
	return (1 << n) - 1


def conditional_negate(neg, x: int) -> int:
	neg = bool(neg)
	return (x ^ -neg) + neg


def conditional_negate2(neg, x: int) -> int:
	neg = -bool(neg) | 1  # either 1 or -1
	return x * neg


def exponential(base, start=1):
	"""
	exponential sequence
	"""
	p = start
	while True:
		yield p
		p *= base


def undivmod(base):
	def f(div, mod):
		return base * div + mod
	return f
