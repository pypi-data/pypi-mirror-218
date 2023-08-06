## fastminhash

`fastminhash` is a fast N-gram MinHash implementation in C.

### Install

```shell
pip3 install fastminhash
```

### Usage

```python3
from minhash import minhash, minhash_all

# `n` means to hash every n-grams, `token_max_value` is the maximum value of each token, `coeff1` and `coeff2` are two constants for hash function construction, `tokens` is the list of tokens
hash = minhash(5, 100276, 12345, 54321, [32352, 33513, 1864, 3626, 12763, 27125, 23981])

# You can calculate multiple minhashes at once by using multiple coeffs
hashes = minhash_all(5, 100276, [(12345, 54321), (23456, 65432)], [32352, 33513, 1864, 3626, 12763, 27125, 23981])
```
