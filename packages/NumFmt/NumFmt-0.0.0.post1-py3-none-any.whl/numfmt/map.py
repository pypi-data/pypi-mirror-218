from enum import Enum
from .utils import chars


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
	# BASE34 = "123456789abcdefghijkmnopqrstuvwxyz"  # case-insensitive derivative of base58
	BASE58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
