import typing as _tp


def add1(fraction: _tp.Tuple[int, int]):
	a, b = fraction
	a += b
	return a, b


def exp(fraction: _tp.Tuple[int, int], r: int, e: int):
	a, b = fraction
	k = r ** abs(e)
	if e < 0:
		b *= k
	else:
		a *= k
	return a, b


def exp_base2(fraction: _tp.Tuple[int, int], exponent: int):
	a, b = fraction
	# faster way to do
	#  2 ** abs(exponent)
	k = 1 << abs(exponent)
	#
	if exponent < 0:
		b *= k
	else:
		a *= k
	return a, b
