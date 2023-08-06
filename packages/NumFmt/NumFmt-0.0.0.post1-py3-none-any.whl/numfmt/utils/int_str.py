import typing as _tp
# todo this belongs in parse
# todo each lib could have a utils folder that doesn't import the whole lib?
# todo finish type hinting
from typing import List, Union, Type
from enum import Enum
# todo rename?
#  intcoding, intcode


def _typing_test_a() -> _tp.Callable[[str, int], _tp.Tuple[int, str]]:
	def f(a: str, b: int) -> _tp.Tuple[int, str]:
		return b, a
	return f


_TTB_F_ARG_TS = (str, int)
_TTB_F_ARG_TS_2: List = [str, int]
_TTB_F_RET_T = _tp.Tuple[int, str]
# _TTB_F_SIG = _tp.Callable[(_TTB_F_ARG_TS[0], _TTB_F_ARG_TS[1], ), _TTB_F_RET_T]  # doesn't work, exceptions
_TTB_F_SIG = _tp.Callable[list(_TTB_F_ARG_TS), _TTB_F_RET_T]  # works with error in editor
_TTB_F_SIG = _tp.Callable[[*_TTB_F_ARG_TS, ], _TTB_F_RET_T]  # doesn't work
_TTB_F_SIG = _tp.Callable[_TTB_F_ARG_TS_2, _TTB_F_RET_T]  # works with error in editor
_TTB_F_SIG = _tp.Callable[[_TTB_F_ARG_TS[0], _TTB_F_ARG_TS[1]], _TTB_F_RET_T]  # works
_C_DF = 4  # this stops value from being displayed by type hinting


def _typing_test_b(c: int = _C_DF) -> _TTB_F_SIG:
	def f(a: _TTB_F_ARG_TS[0], b: _TTB_F_ARG_TS[1]) -> _TTB_F_RET_T:
		return b, a
	return f


_i, _s = _typing_test_a()(5, 5)
_typing_test_a()(_i, _i)

_i, __s = _typing_test_b()(5, 5)
_typing_test_b()(_i, _i)

_i, ___s = _typing_test_b()(5, 5)
_typing_test_b()(_i, _i)
_typing_test_b()


def to_int(iterable, index, default=0):
	class RType:
		@property
		def value(self):
			return self._value

		@value.setter
		def value(self, x):
			self._value = x

		@property
		def index(self):
			return self._index

		@index.setter
		def index(self, x):
			self._index = int(x)

		def __init__(self, value, _index):
			super().__init__()
			self.value = value
			self.index = _index

	if index == len(iterable):  #
		return RType(default, index)

	# skip until integer chars
	is_negative = False
	while True:
		c = (iterable[index])
		if '0' <= c <= '9':
			break
		index += 1
		if index == len(iterable):
			return RType(default, index)
		if c == '-':
			is_negative = True
			break

	# main loop
	r = 0
	while True:
		c = (iterable[index])
		if not ('0' <= c <= '9'):
			break
		index += 1
		if index == len(iterable):
			return RType(default, index)
		r *= 10
		r += (ord(c) if isinstance(c, str) else c) - ord('0')

	return RType(-r if is_negative else r, index)


def chars(start: str, length: int) -> _tp.Sequence[str]:
	start = ord(start)
	return tuple((chr(i) for i in range(start, start + length)))


DEFAULT_SIGNS = (('', '+'), ('-', ))
# ALPHANUM_CHARSET = "".join((*chars('0', 10), *chars('a', 26)))
# BASE58_CHARSET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


class Charsets(Enum):
	DEC = "".join(chars('0', 10))
	HEX_LOWER = "".join((*chars('0', 10), *chars('a', 6)))
	HEX_UPPER = "".join((*chars('0', 10), *chars('A', 6)))
	ALPHA_LOWER = "".join(chars('a', 26))
	ALPHA_UPPER = "".join(chars('A', 26))
	ALPHANUM_LOWER = "".join((*chars('0', 10), *chars('a', 26)))
	ALPHANUM_UPPER = "".join((*chars('0', 10), *chars('A', 26)))
	BASE34 = "123456789abcdefghijkmnopqrstuvwxyz"  # case-insensitive derivative of base58
	BASE58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


ENCODE_ARG_TS = [int, ]
ENCODE_RET_T = str
ENCODE_SIG = _tp.Callable[ENCODE_ARG_TS, ENCODE_RET_T]

DECODE_ARG_TS = [str, ]
DECODE_RET_T = int
DECODE_SIG = _tp.Callable[DECODE_ARG_TS, DECODE_RET_T]

CHARSET_U = _tp.Union[Enum, _tp.Sequence[str]]

CODER_ARG_TS = [int, int, CHARSET_U, _tp.Sequence[str]]


class Coder(_tp.NamedTuple):
	encode: ENCODE_SIG
	decode: DECODE_SIG


def coders(
		base: CODER_ARG_TS[0] = 10,
		padding: CODER_ARG_TS[1] = 1,
		charset: CODER_ARG_TS[3] = Charsets.ALPHANUM_LOWER.value,
		signs: CODER_ARG_TS[2] = DEFAULT_SIGNS,
) -> Coder:
	"""
	returns: encoder, decoder
	"""
	if base is None:
		base = len(charset)
	if base < 2:
		raise ValueError("! base must be >= 2")  # stops forever looping
	if isinstance(charset, Enum):
		charset = charset.value
	charset_indexes = {c: i for i, c in enumerate(charset)}

	pos_signs, neg_signs = signs

	def encode(x: ENCODE_ARG_TS[0]) -> ENCODE_RET_T:
		neg = x < 0
		sign = signs[neg][0]
		if neg:
			x = -x

		r = []
		while x:  # do while in c++ (more efficient)
			index = x % base
			x //= base
			r.insert(0, charset[index])

		r.insert(0, "".join(charset[0] for _ in range(padding - len(r))))
		r.insert(0, sign)
		return "".join(r)

	# todo make tolerant of leading/trailing whitespace
	def decode(sequence: DECODE_ARG_TS) -> DECODE_RET_T:
		# check sign
		# todo better algorithm here
		is_negative = False
		for _neg_signs, _signs in enumerate(signs):
			for sign in _signs:
				if sequence[:len(sign)] == sign:
					is_negative = _neg_signs
					sequence = sequence[len(sign):]

		# main loop
		r = 0
		for c in sequence:
			# if not ('0' <= c <= '9'):
			# 	break
			r *= base
			try:
				r += charset_indexes[c]
			except KeyError:
				break

		return -r if is_negative else r

	return Coder(encode, decode)


def encoder(base: CODER_ARG_TS[0] = 10, padding: CODER_ARG_TS[1] = 1, signs: CODER_ARG_TS[2] = DEFAULT_SIGNS,
		charset: CODER_ARG_TS[3] = Charsets.ALPHANUM_LOWER.value) -> ENCODE_SIG:
	return coders(base, padding, charset, signs)[0]


def decoder(base: CODER_ARG_TS[0] = 10, padding: CODER_ARG_TS[1] = 1, signs: CODER_ARG_TS[2] = DEFAULT_SIGNS,
		charset: CODER_ARG_TS[3] = Charsets.ALPHANUM_LOWER.value) -> DECODE_SIG:
	return coders(base, padding, charset, signs)[1]


if __name__ == '__main__':
	import enum
	print(isinstance(Charsets, enum.Enum))
	print(isinstance(Charsets, enum.EnumMeta))
	print(isinstance(Charsets.ALPHANUM_LOWER, enum.Enum))

	def test():
		print(Charsets.ALPHANUM_LOWER)
		base58 = coders(base=58, charset=Charsets.BASE58)
		base26 = coders(base=26, padding=1, charset=chars('a', 26))
		base16 = coders(base=16)
		base10 = coders(base=10)
		base8 = coders(base=8)
		base4 = coders(base=4)
		base2 = coders(base=2)

		encode, decode = base58

		for i in range(-10000, 10000):
			enc = encode(i)
			dec = decode(enc)
			if i != dec:
				(print(i, dec))

			# print(base26(i), base10(i), base8(i), base4(i), base2(i))

	test()
	# print(int(" -1 "))
	# print("asdf.fdsa".partition("."))
	# print(".fdsa".partition("."))
	# print("fdsa".partition("."))
	# print("asdf.fdsa".rpartition("."))
	# print(".fdsa".rpartition("."))
	# print("fdsa".rpartition("."))
