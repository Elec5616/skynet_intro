from Crypto.Util import strxor

__all__ = ("XOR",)


class XOR:
    __slots__ = ("key", "_keylen", "_last_pos")

    block_size = 1

    def __init__(self, key: bytes) -> None:
        assert 0 < len(key) <= 32, "XOR key must be no longer than 32 bytes"
        self.key = key
        self._last_pos = 0

    @classmethod
    def new(cls, key: bytes) -> "XOR":
        return cls(key)

    def encrypt(self, plaintext: bytes) -> bytes:
        key = rotate(self.key, self._last_pos)
        keylen = len(key)
        pt_len = len(plaintext)
        key *= pt_len // keylen + 1
        key = key[:pt_len]
        self._last_pos = (self._last_pos + pt_len) % keylen
        return strxor.strxor(plaintext, key)

    def decrypt(self, ciphertext: bytes) -> bytes:
        return self.encrypt(ciphertext)


def rotate(s: bytes, n: int) -> bytes:
    return s[n:] + s[:n]
