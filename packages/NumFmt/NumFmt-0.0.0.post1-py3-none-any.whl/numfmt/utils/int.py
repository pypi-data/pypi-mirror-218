import typing as _tp

# todo can this be moved into bitwise?


def bits(n: int) -> int:
	return ~(-1 << n)


# todo this could be more logical if it just worked off of bits?
#  eg unsign(0xffff, 16)
def unsign(x: int, n_words: int = 8, word_size: int = 8) -> int:
	"""unsign an integer"""
	return bits(n_words * word_size) & x


def unsign2(n_bits: int = 64) \
		-> _tp.Callable[[int, ], int]:
	"""unsign an integer"""
	mask = bits(n_bits)

	def f(x: int) -> int:
		return mask & x

	return f


def resign(x: int, n_words: int = 8, word_size: int = 8) -> int:
	"""resign a previously unsigned integer"""
	shift = word_size * n_words - 1
	sign_bit = 1 << shift
	sign = bool(sign_bit & x)
	return (-sign << shift) | x


def resign2(n_bits: int = 64) \
		-> _tp.Callable[[int, ], int]:
	"""resign a previously unsigned integer"""
	shift = n_bits - 1
	sign_bit = 1 << shift

	def f(x: int) -> int:
		is_neg = bool(sign_bit & x)
		return (-is_neg << shift) | x

	return f


def little_split(x: int, word_size: int = 8) -> _tp.Generator[int, None, None]:
	word_mask = bits(word_size)
	stop = -(x < 0)  # 0 or -1
	while x != stop:
		yield word_mask & x
		x >>= word_size
	return


def little_combine(it: _tp.Iterable[int], word_size: int = 8) -> int:
	# _tp.Iterable[int] includes bytes type
	r = 0
	for i, v in enumerate(it):
		v <<= word_size * i
		r |= v
	return r


def big_split(x: int, word_size: int = 8) -> _tp.Iterable[int]:
	return reversed(tuple(little_split(x, word_size)))


def big_combine(it: _tp.Sequence[int], word_size: int = 8) -> int:
	return little_combine(reversed(it), word_size)


def split(_n_words: int = 8, _word_size: int = 8, _endian=False) \
		-> _tp.Callable[[int, ], _tp.Sequence[int]]:
	"""
	_size: num of words
	_word_size: num of bits in a word
	_endian: False/True (little/big endian)
	"""
	_bits = bits(_word_size)

	def f(x: int) \
			-> _tp.Generator[int, None, None]:
		sign = _bits & -(x < 0)
		i = _n_words
		for v in little_split(x, _word_size):
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


def combine(_signed=True, _n_words: int = 8, _word_size: int = 8, _endian=False) \
		-> _tp.Callable[[_tp.Sequence[int], ], int]:
	"""
	_signed: signed/unsigned (True/False) integer
	_size: num of words
	_word_size: num of bits in a word
	_endian: little/big (False/True) endian
	"""

	_n_bits = _n_words * _word_size
	_combine = big_combine if _endian else little_combine

	def signed(it: _tp.Sequence[int]) -> int:
		# _tp.Sequence[int] includes bytes type
		return resign2(_n_bits)(_combine(it[:_n_words], _word_size))

	def unsigned(it: _tp.Sequence[int]) -> int:
		# _tp.Sequence[int] includes bytes type
		return _combine(it[:_n_words], _word_size)

	return signed if _signed else unsigned
