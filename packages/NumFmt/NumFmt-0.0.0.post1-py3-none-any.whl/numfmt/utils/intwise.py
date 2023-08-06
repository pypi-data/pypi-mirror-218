"""
successor to 'utils.int'
"""
import typing as _tp


# generic impl
def bits(n: int) -> int:
	return (1 << n) - 1


# todo test which is faster
# python only impl
def bits2(n: int) -> int:
	return ~(-1 << n)


def conditional_negate(neg, x: int) -> int:
	neg = bool(neg)
	return (x ^ -neg) + neg


def conditional_negate2(neg, x: int) -> int:
	neg = -bool(neg) | 1  # either 1 or -1
	return x * neg


def unsign(n_bits: int = 64) \
		-> _tp.Callable[[int, ], int]:
	"""unsign an integer"""
	mask = bits(n_bits)

	def f(x: int) -> int:
		return mask & x

	return f


def resign(n_bits: int = 64) \
		-> _tp.Callable[[int, ], int]:
	"""resign a previously unsigned integer"""
	shift = n_bits - 1
	sign_bit = 1 << shift

	def f(x: int) -> int:
		is_neg = bool(sign_bit & x)
		return (-is_neg << shift) | x

	return f


def split_little(word_size: int = 8) \
		-> _tp.Callable[[int, ], _tp.Generator[int, None, None]]:
	word_mask = bits(word_size)

	def f(x: int) \
			-> _tp.Generator[int, None, None]:
		stop = -(x < 0)  # 0 or -1
		while x != stop:
			yield word_mask & x
			x >>= word_size

	return f


def split_big(word_size: int = 8) \
		-> _tp.Callable[[int, ], _tp.Iterable[int]]:
	g = split_little(word_size)

	def f(x: int) -> _tp.Iterable[int]:
		return reversed(tuple(g(x)))

	return f


def split(_n_words: int = 8, _word_size: int = 8, _endian=False) \
		-> _tp.Callable[[int, ], _tp.Sequence[int]]:
	"""
	_size: num of words
	_word_size: num of bits in a word
	_endian: False/True (little/big endian)
	"""
	_bits = bits(_word_size)
	g = split_little(_word_size)

	def f(x: int) \
			-> _tp.Generator[int, None, None]:
		sign = _bits & -(x < 0)
		i = _n_words
		for v in g(x):
			if not i:
				return
			yield v
			i -= 1
		while i:
			yield sign
			i -= 1
		return

	def big_end(x: int) \
			-> _tp.Sequence[int]:
		return tuple(reversed(tuple(f(x))))

	def little_end(x: int) \
			-> _tp.Sequence[int]:
		return tuple(f(x))

	return big_end if _endian else little_end


def combine_little(word_size: int = 8) \
		-> _tp.Callable[[_tp.Iterable[int], ], int]:
	def f(it: _tp.Iterable[int]) -> int:
		# _tp.Iterable[int] includes bytes type
		r = 0
		for i, v in enumerate(it):
			v <<= word_size * i
			r |= v
		return r

	return f


def combine_big(word_size: int = 8) \
		-> _tp.Callable[[_tp.Sequence[int], ], int]:
	g = combine_little(word_size)

	def f(it: _tp.Sequence[int]) -> int:
		return g(reversed(it))

	return f


def combine(_signed=True, _n_words: int = 8, _word_size: int = 8, _endian=False) \
		-> _tp.Callable[[_tp.Sequence[int], ], int]:
	"""
	_signed: signed/unsigned (True/False) integer
	_size: num of words
	_word_size: num of bits in a word
	_endian: little/big (False/True) endian
	"""

	_n_bits = _n_words * _word_size
	_combine = combine_big(_word_size) if _endian else combine_little(_word_size)
	_resign = resign(_n_bits)

	def signed(it: _tp.Sequence[int]) -> int:
		# _tp.Sequence[int] includes bytes type
		return _resign(_combine(it[:_n_words]))

	def unsigned(it: _tp.Sequence[int]) -> int:
		# _tp.Sequence[int] includes bytes type
		return _combine(it[:_n_words])

	return signed if _signed else unsigned
