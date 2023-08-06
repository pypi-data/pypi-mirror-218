import typing as _tp
from itertools import islice
from ..utils.itools import concat, ireversed
from ..charmaps import Charsets, DEFAULT_SIGNS
from .calc import digits_le


T = _tp.TypeVar('T')
I = _tp.TypeVar('I')
S = _tp.TypeVar('S')


def pad_back(
		padding: int = 1
):
	# def f(seq):
	# 	return tuple(concat(seq, (0 for _ in range(padding - len(seq)))))

	def g(it):
		i = 0
		for i, x in enumerate(it, 1):
			yield x
		yield from (0 for _ in range(padding - i))

	return g


def charmap(
		charset: _tp.Sequence[S] = Charsets.DEC.value,
):
	"""
	standard notation charmap
	"""

	def f(it: _tp.Iterable[I]) -> _tp.Generator[S, None, None]:
		return (charset[i] for i in it)

	return f


def signmap(
		signs: _tp.Sequence[_tp.Sequence[S]] = DEFAULT_SIGNS,
):
	def f(sign):
		return signs[sign][0]

	return f


# encode int to str
def int_to_str(
		base: int = 10,
		padding: int = 1,
		limit: int = None,
		charset: _tp.Sequence = Charsets.ALPHANUM_LOWER.value,
		signs: _tp.Sequence = DEFAULT_SIGNS,
):
	_digits = digits_le(base)
	_pad_back = pad_back(padding)

	def encode(x: int) -> str:
		neg, digs = _digits(x)
		return "".join(
			concat(
				signs[neg][0],
				map(
					charset.__getitem__,
					ireversed(islice(_pad_back(digs), limit)),
				),
			)
		)

	return encode


def str_to_int():
	...
