
# generic impl
def bits(n: int) -> int:
	return (1 << n) - 1


# generic impl
#  seems to be slightly slower
def bits2(n: int) -> int:
	return ~(-1 << n)


# no overflow impl
def bits3(n: int) -> int:
	x = bool(n)
	return (((1 << (n - x)) - 1) << x) | x


def get(integer: int, index: int) -> int:
	mask = 1 << index
	return bool(integer & mask)


bit = get


# todo test which is faster
def set(integer: int, index: int, value) -> int:
	mask = 1 << index
	# clear then set to value
	return (integer & ~mask) | (mask & -bool(value))


def set2(integer: int, index: int, value) -> int:
	mask = 1 << index
	# use conditional to set or clear
	return integer | mask if value else integer & ~mask


bit_set = set


def main3():
	a = set(0b100, 2, 1)
	print(bin(a))


def left(integer: int, shift: int) -> int:
	return integer >> -shift if shift < 0 else integer << shift


def right(integer: int, shift: int) -> int:
	return integer << -shift if shift < 0 else integer >> shift


def msbi(x: int) -> int:
	"""highest order bit index / most significant bit index"""
	shift = -1
	stop = -(x < 0)
	while x != stop:
		x >>= 1
		shift += 1
	return shift


def msb2(n: int) -> int:
	n |= (n >> 1)
	n |= (n >> 2)
	n |= (n >> 4)
	n |= (n >> 8)
	n |= (n >> 16)
	# return n - (n >> 1)
	return n - (n >> 1)


def msb3(x: int) -> int:
	i = 0
	# if x & 0xFFFF0000:
	# 	i += 16
	# 	x >>= 16
	# if x & 0xFF00:
	# 	i += 8
	# 	x >>= 8
	if x & 0xF0:
		i += 4
		x >>= 4
	if x & 0x0C:
		i += 2
		x >>= 2
	if x & 2:
		i += 1
		x >>= 1
	if x & 1:
		i += 1
	return i


hobi = msbi


def msb(integer: int) -> int:
	"""highest order bit / most significant bit"""
	shift = msbi(integer)
	return 1 << shift if shift != -1 else 0


def main2():
	x = 255
	#print(x.bit_length())
	#print(msbi(x))
	print(x.bit_length(),)
	shift = 1 << 8
	for i in range(9):
		shift >>= 1
		print(shift, msb3(shift), bin(msb3(shift)))
		# print(shift, bin(shift), msbi(shift), ~shift, bin(~shift), msbi(~shift))


hob = msb


def lsbi(integer: int) -> int:
	"""lowest order bit index / the least significant bit index"""
	integer <<= 1
	shift = -1
	while integer and not (1 & integer):
		integer >>= 1
		shift += 1
	return shift


def main():
	print(lsbi(0))
	print(lsbi(1))
	print(lsbi(0b11011001))
	print(lsbi(0b11011000))
	print(lsbi(0b1000))


if __name__ == '__main__':
	main2()


lobi = lsbi


def lsb(integer: int) -> int:
	"""lowest order bit / most significant bit"""
	shift = lsbi(integer)
	return 1 << shift if shift != -1 else 0


lob = lsb


#
# reverse
#

def reverse_8b(x):
	x = ((x & 0x55) << 1) | ((x & 0xAA) >> 1)
	x = ((x & 0x33) << 2) | ((x & 0xCC) >> 2)
	x = ((x & 0x0F) << 4) | ((x & 0xF0) >> 4)
	return x


REVERSE_8B2_LOOKUP = (
	0x0, 0x8, 0x4, 0xc, 0x2, 0xa, 0x6, 0xe,
	0x1, 0x9, 0x5, 0xd, 0x3, 0xb, 0x7, 0xf,
)


# alternative, usually faster
def reverse_8b2(x: int) -> int:
	x &= 0xff
	return (REVERSE_8B2_LOOKUP[x & 0b1111] << 4) | REVERSE_8B2_LOOKUP[x >> 4]


def reverse_16b(x):
	x = ((x & 0x5555) << 1) | ((x & 0xAAAA) >> 1)
	x = ((x & 0x3333) << 2) | ((x & 0xCCCC) >> 2)
	x = ((x & 0x0F0F) << 4) | ((x & 0xF0F0) >> 4)
	x = ((x & 0x00FF) << 8) | ((x & 0xFF00) >> 8)
	return x


def reverse_32b(x):
	x = ((x & 0x55555555) << 1) | ((x & 0xAAAAAAAA) >> 1)
	x = ((x & 0x33333333) << 2) | ((x & 0xCCCCCCCC) >> 2)
	x = ((x & 0x0F0F0F0F) << 4) | ((x & 0xF0F0F0F0) >> 4)
	x = ((x & 0x00FF00FF) << 8) | ((x & 0xFF00FF00) >> 8)
	x = ((x & 0x0000FFFF) << 16) | ((x & 0xFFFF0000) >> 16)
	return x


# slow
def reverse_byte(x: int) -> int:
	r = 0
	for i in range(8):
		r |= ((x >> i) & 1) << (7-i)
	return r


# faster
reverse_byte2 = reverse_8b

# much faster
reverse_byte3 = reverse_8b2


def reverse(x: int, n_bits: int) -> int:
	"""logical reverse: reverse bit order"""
	r = 0
	for i in reversed(range(n_bits)):
		r |= (x & 1) << i
		x >>= 1
	return r


# faster
#  reverses the input in chunks
#  fewer iterations is faster
def reverse2(x: int, n_bits: int, word_size=32, reverse_word=reverse_32b):
	word_mask = bits(word_size)
	n_words = (n_bits + word_size - 1) // word_size  # ceiling div
	correction = n_words * word_size - n_bits

	def g(v):
		for i in range(n_words):
			word = word_mask & v
			v >>= word_size
			yield reverse_word(word)

	def f(v: int, _=None):
		r = 0
		for b in g(v):
			r <<= word_size
			r |= b
		return r >> correction

	return f(x)
