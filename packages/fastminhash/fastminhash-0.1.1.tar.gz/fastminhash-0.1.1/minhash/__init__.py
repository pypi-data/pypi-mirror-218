from ._minhash.lib import minhash as minhash_impl, minhash_all as minhash_all_impl
from ._minhash import ffi
from typing import List, Tuple

def minhash(n: int, token_max_value: int, modulo: int, coeff1: int, coeff2: int, tokens: List[int]) -> int:
    tokens_in = ffi.new("int[]", len(tokens))
    for i in range(len(tokens)):
        tokens_in[i] = tokens[i]
    return minhash_impl(n, token_max_value, modulo, coeff1, coeff2, len(tokens), tokens_in)

def minhash_all(n: int, token_max_value: int, modulo: int, coeffs: List[Tuple[int, int]], tokens: List[int]) -> List[int]:
    coeffs_in = ffi.new("hash_coeff[]", len(coeffs))
    for i in range(len(coeffs)):
        coeffs_in[i].coeff1 = coeffs[i][0]
        coeffs_in[i].coeff2 = coeffs[i][1]
    tokens_in = ffi.new("int[]", len(tokens))
    for i in range(len(tokens)):
        tokens_in[i] = tokens[i]
    results_out = ffi.new("unsigned long long[]", len(coeffs_in))
    minhash_all_impl(n, token_max_value, modulo, len(coeffs), coeffs_in, len(tokens), tokens_in, results_out)
    return ffi.unpack(results_out, len(coeffs))
