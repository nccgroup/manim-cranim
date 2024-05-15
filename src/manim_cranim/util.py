from random import Random
from sys import argv
from .types import *


__all__ = ['_enc', '_dec', '_pad', '_flatten', 'blk', 'bytes_xor', 'chunk_bytes']


_rng = Random()
_rng.seed(str(argv).encode("UTF-8") + bytes(range(256))*17)


def _enc(msg, mode=None, pad=None, key=bytes(32), iv=None):  # convenience function for (by default) evaluating AES-256 in ECB mode with a null key
    from Crypto.Cipher import AES
    from .buffers import Block
    mode = mode or AES.MODE_ECB
    args = {"key": key, "mode": mode}
    if mode is AES.MODE_CBC or mode is AES.MODE_CTR:
        if iv is None: iv = blk()
        args["iv"] = iv
    if isinstance(msg, Block):
        msg = msg._bytes
    if pad is None:
        pad = len(msg) % 16 != 0 or msg == b''  # if pad is None, apply pkcs7 padding *only* when necessary (not unconditionally)
    if pad:
        msg = _pad(msg)
    cipher = AES.new(**args)
    return cipher.encrypt(msg)


def _dec(msg, mode=None, unpad=False, key=bytes(32), iv=None):  # convenidece function for (by default) evaluating AES-256 in ECB mode with a null key
    from Crypto.Cipher import AES
    from .buffers import Block
    mode = mode or AES.MODE_ECB
    args = {"key": key, "mode": mode}
    if mode is AES.MODE_CBC or mode is AES.MODE_CTR:
        if iv is None: iv = blk()
        args["iv"] = iv
    if isinstance(msg, Block):
        msg = msg._bytes
    cipher = AES.new(**args)
    pt = cipher.decrypt(msg)
    if unpad:
        pt = pt[:-pt[-1]]
    return pt


def _pad(msg: bytes, block_size=16):
    """pkcs7"""
    pad_len = block_size - (len(msg) % block_size)
    return msg + bytes([pad_len]) * pad_len


def _flatten(*iters):
    return [y for x in iters for y in x]


def blk(seed=None, size=16):  # convenience function for getting dummy blocks
    if seed is None:
        return _rng.randbytes(size)
    else:
        seed = repr(seed).encode()
        from Crypto.Hash import BLAKE2b
        return BLAKE2b.new(data=seed, digest_bytes=size).digest()


def _bytes_xor(a: bytes, b: bytes, quiet=True, check_lens=False) -> bytes:
    if not quiet:
        print(a, "⊕", b)
    if check_lens and len(a) != len(b):
        raise ValueError("bytestring lengths aren't equal")
    return bytes(byte_1 ^ byte_2 for byte_1, byte_2 in zip(a, b)) 


def bytes_xor(*args, quiet=True, check_lens=False):
    assert len(args) > 0 
    from .buffers import Block
    args = [(
        arg.bytes if isinstance(arg, Block) else
        arg.encode('ascii') if isinstance(arg, str) else arg
    ) for arg in args]
    result = args[0]
    for arg in args[1:]:
        result = _bytes_xor(result, arg, quiet=quiet, check_lens=check_lens)
    return result


def chunk_bytes(b: bytes, chunk_size: int = 16, quiet=True) -> list[bytes]:  # TODO relax b's type annotation
    """
    "Chunks" a bytestring, breaking it up into equally-sized chunks.
    These could be blocks (usually they will be), but of course they don't have to be.
    Technically they don't even have to be bytes - anything that supports slicing and len() will do.
    """
    chunks = [b[ind:ind+chunk_size] for ind in range(0, len(b), chunk_size)]
    if not quiet:
        print("Chunked input with size {chunk_size}: {chunks}")
    return chunks
