import struct
import typing as _tp
import enum
from ..utils import bits
from . import fracs


def float_to_bits(f: float) -> int:
	s = struct.pack('>f', f)
	i = struct.unpack('>L', s)[0]
	return i


def bits_to_float(i: int) -> float:
	s = struct.pack('>L', i)
	f = struct.unpack('>f', s)[0]
	return f


def double_to_bits(f: float) -> int:
	s = struct.pack('>d', f)
	i = struct.unpack('>Q', s)[0]
	return i


def bits_to_double(i: int) -> float:
	s = struct.pack('>Q', i)
	f = struct.unpack('>d', s)[0]
	return f


def float32_cat(base, sign, exponent, fraction):
	sign = -bool(sign) | 1  # either 1 or -1
	return sign * (base ** (exponent - 127)) * (1 + fraction)


def float64_cat(base, sign, exponent, fraction):
	sign = -bool(sign) | 1  # either 1 or -1
	return sign * (base ** (exponent - 1023)) * (1 + fraction)


class FloatSize(_tp.NamedTuple):
	sign: int
	exp: int
	frac: int


class FloatSetup(_tp.NamedTuple):
	size: FloatSize
	unpacker: _tp.Callable[[float, ], int]
	exp_offset: int


FLOAT32_SETUP = FloatSetup(FloatSize(1, 8, 23), float_to_bits, -127)
FLOAT64_SETUP = FloatSetup(FloatSize(1, 11, 52), double_to_bits, -1023)


def slice_int(stops):
	masks = tuple(map(bits, stops))

	def f(x: int):
		for mask, stop in zip(masks, stops):
			yield x & mask
			x >>= stop

	return f


def slice_float2(float_size: FloatSize):
	_slice = slice_int(tuple(reversed(float_size)))

	def f(i: int):
		return reversed(tuple(_slice(i)))

	return f


def slice_float(float_size: FloatSize):
	s_len, e_len, f_len = float_size
	s_mask, e_mask, f_mask = map(bits, float_size)

	def f(i: int):
		_f = f_mask & i
		i >>= f_len
		e = e_mask & i
		i >>= e_len
		s = s_mask & i
		return s, e, _f

	return f


def float_unpack(float_setup: FloatSetup):
	size, to_bits, offset = float_setup
	_slice_float = slice_float(size)

	def f(x: float):
		i = to_bits(x)
		sign, exp, frac = _slice_float(i)
		# exp += offset
		return sign, exp, frac

	return f


class FloatEncoding(enum.Enum):
	null = 0
	subnormal = 1
	normal = 2
	inf = 3
	nan = 4


def float_encoding(exp, exp_mask, frac_numerator):
	# special exponents
	#  signed zero (if F = 0) and subnormal numbers (if F ≠ 0)
	if exp == 0:
		if frac_numerator == 0:
			exp_enc = FloatEncoding.null
		else:
			exp_enc = FloatEncoding.subnormal
	# ∞ (if F = 0) and NaNs (if F ≠ 0)
	elif exp == exp_mask:
		if frac_numerator == 0:
			exp_enc = FloatEncoding.inf
		else:
			exp_enc = FloatEncoding.nan
	else:
		exp_enc = FloatEncoding.normal
	return exp_enc


def float_frac(float_setup: FloatSetup = FLOAT32_SETUP):
	_float_unpack = float_unpack(float_setup)
	(_, exp_len, frac_len), _, offset = float_setup
	exp_mask = bits(exp_len)
	frac_max = 1 << frac_len

	def f(x: float) -> tuple:
		# unpack floating point
		sign, exp, frac_numerator = _float_unpack(x)

		# special exponents
		exp_enc = float_encoding(exp, exp_mask, frac_numerator)

		if exp_enc in (FloatEncoding.inf, FloatEncoding.nan, ):
			raise NotImplementedError(str(exp_enc.name))

		exp += offset

		# convert to fraction
		frac = frac_numerator, frac_max
		if exp_enc in (FloatEncoding.normal, ):
			# add 1 to the fraction when in
			#  normal encoding mode
			frac = fracs.add1(frac)
		frac = fracs.exp_base2(frac, exp)

		return sign, frac

	return f
