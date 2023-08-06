# import typing as _tp
import itertools
import math
from ..intstr.calc import digits_be, number_be
from ..utils.itools import strcat
from ..utils import exponential
from . import fracs


def sci_exp(base: int, x: float):
	x = abs(x)
	if x < 1:
		if x == 0.0:
			e = 0
		else:
			e = math.log(1 / x, base)
			e = -math.ceil(e)
	else:
		e = math.log(x, base)
		e = math.floor(e)
	return e


def sci_exp_frac(base: int, a: int, b: int):
	if not (a or b):
		e = 0
	elif a < b:  # numerator < denominator == n/d < 1
		e = math.log(b / a, base)
		e = -math.ceil(e)
	else:
		e = math.log(a / b, base)
		e = math.floor(e)
	return e


def sci_div(base, mod, b):
	"""
	perform division in base,
		yielding digits in said
		base
	"""
	div, mod = divmod(mod, b)
	yield div
	while mod:
		mod *= base
		div, mod = divmod(mod, b)
		yield div


def number_be2(
		base: int = 10,
):
	def f(_digits):
		"""digits are passed in big endian order"""
		div = 0
		for mod in _digits:
			div = base * div + mod  # reverse divmod
			yield div

	return f


def frac2(base, digits):
	return zip(
		number_be2(base)(digits),
		exponential(base),
	)


def digits_frac(base: int):

	def f(frac_digits, exp_digits) -> tuple:
		sign, frac_digits = frac_digits
		frac_digits = tuple(frac_digits)
		# frac_max = base ** (len(frac_digits) - 1)
		# frac_numerator = intstr.math.number_be(base)(sign, frac_digits)
		exp = number_be(base)(*exp_digits)

		# convert to fraction
		frac = tuple(frac2(base, frac_digits))[-1]
		frac = fracs.exp(frac, base, exp)

		return sign, frac

	return f


def frac_sci(base: int):

	def f(sign, frac):
		# rebase fraction to sci form
		rebase_exp = sci_exp_frac(base, *frac)
		frac = fracs.exp(frac, base, -rebase_exp)
		return sign, frac, rebase_exp

	return f


def sci_digits(base: int, figures: int = 6):

	def f(sign, frac, exp):
		# convert rebased fraction into str
		frac_digits = (itertools.islice(sci_div(base, *frac), figures))
		exp_digits = digits_be(base)(exp)
		return (sign, frac_digits), exp_digits

	return f


def sci_str(base: int = None):
	zero = str(0)
	signs = ('', '-')
	charmap = str

	def f(frac_digits, exp_digits) -> str:
		# convert rebased fraction into str
		f_sign, f_digits = frac_digits
		e_sign, e_digits = exp_digits

		f_digits = iter(f_digits)
		fs = signs[f_sign]
		es = signs[e_sign]
		fd_a = charmap(next(f_digits))
		fd_b = strcat(map(charmap, f_digits))
		ed = strcat(map(charmap, e_digits))
		# e = f"e{exp_digits}"
		# e = f" * {base}**{exp_digits}"
		return f"{fs}{fd_a}.{fd_b if fd_b else zero}e{es}{ed}"

	return f
