import typing as _tp


T = _tp.TypeVar('T')
I = _tp.TypeVar('I')
S = _tp.TypeVar('S')


# todo some of these fns can be i[ter]tools2?
def concat(*its: _tp.Iterable[T]) -> _tp.Generator[T, None, None]:
	"""joins iterables together"""
	for it in its:
		yield from it


def ireversed(it: _tp.Iterable[T]) -> _tp.List[T]:
	"""reverses an iterable that does not implement 'reversed'
	doesn't work on infinite iterables"""
	r = []
	for x in it:
		r.insert(0, x)
	return r


def ireversed2(it: _tp.Iterable[T]) -> _tp.Iterable[T]:
	"""reverses an iterable that does not implement 'reversed'
	doesn't work on infinite iterables"""
	return reversed(tuple(it))


def first(it):
	return next(iter(it))


def strcat(it):
	return "".join(it)


def chars(start: str, length: int) -> _tp.Sequence[str]:
	start = ord(start)
	return tuple((chr(i) for i in range(start, start + length)))


def exp(base, start=1):
	p = start
	while True:
		yield p
		p *= base


def undivmod(base):
	def f(div, mod):
		return base * div + mod

	return f
