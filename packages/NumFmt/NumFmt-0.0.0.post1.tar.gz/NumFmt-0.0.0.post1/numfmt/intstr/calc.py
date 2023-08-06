import typing as _tp
from itertools import accumulate
from ..utils.itools import concat, last  # need this as a utility function for importers
from ..utils import exponential, conditional_negate


T = _tp.TypeVar('T')
I = _tp.TypeVar('I')
S = _tp.TypeVar('S')


DIGITS_1_R = _tp.Tuple[bool, _tp.Iterable[I]]
DIGITS_0_R = _tp.Callable[[I, ], DIGITS_1_R]


# You can extend your answer to include base 1. if b == 1: return n * [1]
def digits_le(
		base: int = 10,
) -> DIGITS_0_R:
	def g(div):
		div, mod = divmod(div, base)
		yield mod  # ensure at least 1 digit
		while div:
			div, mod = divmod(div, base)
			yield mod

	def f(x: I) -> DIGITS_1_R:
		"""digits are returned in little endian order"""
		neg = x < 0
		return neg, (g(abs(x)))

	return f


def digits_le_comp(
		base: int = 10,
) -> DIGITS_0_R:
	"""base complimented"""
	def f(x: I) -> DIGITS_1_R:
		"""digits are returned in little endian order"""
		neg = x < 0
		stop = -neg

		def g(div):
			while div != stop:
				div, mod = divmod(div, base)
				yield mod
			# div, mod = divmod(div, base)
			# yield mod

		return neg, (g(x))

	return f


def digits_be(
		base: int = 10,
) -> DIGITS_0_R:
	g = digits_le(base)

	def f(x: I) -> DIGITS_1_R:
		"""digits are returned in big endian order"""
		neg, it = g(x)
		return neg, (reversed(tuple(it)))

	return f


def digits_be_comp(
		base: int = 10,
) -> DIGITS_0_R:
	"""base complimented"""
	g = digits_le_comp(base)

	def f(x: I) -> DIGITS_1_R:
		"""digits are returned in big endian order"""
		neg, it = g(x)
		return neg, (reversed(tuple(it)))

	return f


NUMBER_1_0 = _tp.Union[bool, I]
NUMBER_1_1 = _tp.Iterable[I]
NUMBER_0_R = _tp.Callable[[NUMBER_1_0, NUMBER_1_1], I]


def number_le(
		base: int = 10,
) -> NUMBER_0_R:
	def f(_sign: NUMBER_1_0, _digits: NUMBER_1_1) -> I:
		"""digits are passed in big endian order"""
		div = 0
		for pos, mod in zip(exponential(base), _digits):
			# div += mod * (base ** i)  # reverse divmod
			div += mod * pos  # reverse divmod
			yield conditional_negate(_sign, div)

	return f


def number_le_comp(
		base: int = 10,
) -> NUMBER_0_R:
	"""base complimented"""
	def f(_sign: NUMBER_1_0, _digits: NUMBER_1_1) -> I:
		"""digits are passed in little endian order"""
		return accumulate(
			mod * pos
			for pos, mod in zip(
				exponential(base),
				concat(_digits, (-bool(_sign), )),
			)
		)

	return f


def number_be(
		base: int = 10,
) -> NUMBER_0_R:
	def f(_sign: NUMBER_1_0, _digits: NUMBER_1_1) -> I:
		"""digits are passed in big endian order"""
		div = 0
		for mod in _digits:
			div = base * div + mod  # reverse divmod
			yield conditional_negate(_sign, div)

	return f


def number_be_comp(
		base: int = 10,
) -> NUMBER_0_R:
	"""base complimented"""
	def f(_sign: NUMBER_1_0, _digits: NUMBER_1_1) -> I:
		"""digits are passed in big endian order"""
		div = -bool(_sign)
		for mod in _digits:
			div = base * div + mod  # reverse divmod
			yield div

	return f


def digits(
		base: int = 10,
		endian: int = False,
		complemented: int = False,
) -> DIGITS_0_R:
	return (
		(digits_le, digits_le_comp), (digits_be, digits_be_comp)
	)[1 & endian][1 & complemented](base)


def number(
		base: int = 10,
		endian: int = False,
		complemented: int = False,
) -> NUMBER_0_R:
	return (
		(number_le, number_le_comp), (number_be, number_be_comp)
	)[1 & endian][1 & complemented](base)
