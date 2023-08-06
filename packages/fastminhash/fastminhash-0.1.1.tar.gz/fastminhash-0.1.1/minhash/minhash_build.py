from cffi import FFI

signature = """
typedef struct {
    int coeff1, coeff2;
} hash_coeff;
unsigned long long minhash(int n, int tokenMaxValue, int modulo, int coeff1, int coeff2, int tokenCnt, int *tokens);
void minhash_all(int n, int tokenMaxValue, int modulo, int coeffCnt, hash_coeff *coeffs, int tokenCnt, int *tokens, unsigned long long *result);
"""

ffibuilder = FFI()
ffibuilder.cdef(signature)
ffibuilder.set_source("minhash._minhash", signature,
    sources=['minhash/minhash.c'],
    libraries=[])

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)