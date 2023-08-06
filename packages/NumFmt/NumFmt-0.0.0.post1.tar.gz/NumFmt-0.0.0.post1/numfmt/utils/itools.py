import typing as _tp
from itertools import tee


T = _tp.TypeVar('T')
I = _tp.TypeVar('I')
S = _tp.TypeVar('S')


def concat(*its: _tp.Iterable[T]) -> _tp.Generator[T, None, None]:
	"""joins iterables together"""
	for it in its:
		yield from it


def strcat(it):
	return "".join(it)


def ireversed(it: _tp.Iterable[T]) -> _tp.Iterable[T]:
	"""reverses an iterable that does not implement 'reversed'
	doesn't work on infinite iterables"""
	return reversed(tuple(it))


def ireversed2(it: _tp.Iterable[T]) -> _tp.List[T]:
	"""reverses an iterable that does not implement 'reversed'
	doesn't work on infinite iterables"""
	r = []
	for x in it:
		r.insert(0, x)
	return r


def first(it, default=None):
	return next(iter(it), default)


def last(it, default=None):
	r = default
	for r in it:
		pass
	return r


# try to import from itertools, if this fails, define here
try:
	from itertools import pairwise
except ImportError:
	def pairwise(iterable):
		# pairwise('ABCDEFG') --> AB BC CD DE EF FG
		a, b = tee(iterable)
		next(b, None)
		return zip(a, b)
