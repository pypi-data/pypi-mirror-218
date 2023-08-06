# import typing as _tp
from .calc import sci_digits, frac_sci, sci_str
from . import ieee754


def floatstr(float_setup: ieee754.FloatSetup = ieee754.FLOAT32_SETUP):

	def f(base: int, x: float, figures=6) -> str:
		digs = sci_digits(base, figures)(*frac_sci(base)(*ieee754.float_frac(float_setup)(x)))
		# print(digs)
		s = sci_str()(*digs)
		return s

	return f
