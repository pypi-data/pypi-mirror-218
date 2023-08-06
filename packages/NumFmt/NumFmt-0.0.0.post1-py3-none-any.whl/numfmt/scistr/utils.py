
def bits(n: int) -> int:
	return (1 << n) - 1


def conditional_negate(neg, x: int) -> int:
	neg = bool(neg)
	return (x ^ -neg) + neg


def conditional_negate2(neg, x: int) -> int:
	neg = -bool(neg) | 1  # either 1 or -1
	return x * neg
