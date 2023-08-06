typedef struct {
    int coeff1, coeff2;
} hash_coeff;

unsigned long long minhash(int n, int tokenMaxValue, int coeff1, int coeff2, int tokenCnt, int *tokens) {
    unsigned long long hash = 0, prevHashFactor = 1;
    for (int i = 0; i < n && i < tokenCnt; i++) {
        hash *= tokenMaxValue;
        hash += (unsigned long long)coeff1 * tokens[i] + coeff2;
        prevHashFactor *= tokenMaxValue;
    }
    unsigned long long result = hash;
    for (int i = n; i < tokenCnt; i++) {
        hash *= tokenMaxValue;
        hash -= ((unsigned long long)coeff1 * tokens[i-n] + coeff2) * prevHashFactor;
        hash += (unsigned long long)coeff1 * tokens[i] + coeff2;
        result = hash < result ? hash : result;
    }
    return result;
}

void minhash_all(int n, int tokenMaxValue, int coeffCnt, hash_coeff *coeffs, int tokenCnt, int *tokens, unsigned long long *result) {
    for(int i = 0; i < coeffCnt; i++){
        result[i] = minhash(n, tokenMaxValue, coeffs[i].coeff1, coeffs[i].coeff2, tokenCnt, tokens);
    }
}