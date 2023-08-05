"""
Speed test for prime sieves using various packages.
1. Standard library only - Ok for small N.
                         - Returns list.
2. Numpy - Faster for larger N and more memory efficient.
         - Returns np.ndarray.
3. Bitarray - Fastest if returning generator and most memory efficent.
            - Converting to list slower.
            - Cannot use Numba.
"""

import math
import os
import sys
import time

import bitarray

import numba
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from euler_maths.prime import _primes, primes, primes_iter


def speed_test(N=10 ** 6, use_njit=False):
    """
    Runs a speed comparison on three prime number sieves from the module.
    Output printed to console.
    """
    print(f"Speed test for prime number sieves for numbers <{N}.")
    print("Standard lib")
    start = time.time()
    if use_njit:
        x = numba.njit(_primes)(N)
    else:
        x = _primes(N)
    end = time.time()
    print(f"Size:{sys.getsizeof(x)/2**20}MB Time:{end - start}")

    print("Numpy")
    start = time.time()
    if use_njit:
        x = numba.njit(primes)(N)
    else:
        x = primes(N)
    end = time.time()
    print(f"Size:{x.nbytes/2**20}MB Time:{end - start}")

    print("Bitarray")
    start = time.time()
    x = primes_iter(N)
    mid = time.time()
    x = [p for p, b in enumerate(x) if b]
    end = time.time()
    print(
        f"Iter size:~{N/(8 * 2**20)}MB Time:{mid - start}\nList size:{sys.getsizeof(x)/2**20}MB List-conversion time:{end - mid}"
    )


if __name__ == "__main__":
    """
    On executing this script, the speed test is run.
    """
    if sys.argv:
        try:
            N = 10 ** int(sys.argv[1])
        except:
            N = 10 ** 6
        if "njit" in sys.argv:
            use_njit = True
        else:
            use_njit = False
    speed_test(N, use_njit)
