"""
Functions for prime sieves and primality tests
"""

import random

import bitarray
import numpy as np


def _primes(N: int) -> list:
    """
    Returns list of primes < N.
    Memory usage ~8*N bytes.
    Defunct: Slower and more memory intensive than Numpy version.
    """
    is_prime = [1] * N
    is_prime[0] = 0
    is_prime[1] = 0
    for j in range(4, N, 2):
        is_prime[j] = 0
    for i in range(3, int(N ** 0.5) + 1, 2):
        if is_prime[i]:
            for j in range(i * i, N, 2 * i):
                is_prime[j] = 0
    return [p for p, b in enumerate(is_prime) if b]


def primes(N: int) -> np.ndarray:
    """
    Returns array of primes < N using Numpy.
    Numba improves speed for N > ~10**8.
    Memory usage ~N bytes.
    """
    is_prime = np.ones(N, dtype=np.uint8)
    is_prime[:2] = 0
    is_prime[4::2] = 0
    for i in range(3, int(N ** 0.5) + 1, 2):
        if is_prime[i]:
            is_prime[i * i :: 2 * i] = 0
    return is_prime.nonzero()[0]


def primes_iter(N: int) -> iter:
    """
    Returns iterable of primes < N using Bitarray.
    Memory usage ~N bits.
    """
    is_prime = bitarray.bitarray(N)
    is_prime.setall(True)
    is_prime[:2] = False
    is_prime[4::2] = False
    for i in range(3, int(N ** 0.5) + 1, 2):
        if is_prime[i]:
            is_prime[i * i :: 2 * i] = False
    return is_prime.itersearch(bitarray.bitarray("1"))


def prime_factors(N: int) -> np.ndarray:
    """
    Returns array of unique prime factors for each number < N.
    Designed to work for N < 2^31.
    """
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
    prod = 1
    for max_count, i in enumerate(small_primes):
        prod *= i
        if prod > N:
            break
    factor_counts = np.zeros(N, np.uint8)
    prime_factors = np.zeros((N, max_count), np.int32)
    for i in range(2, N):
        if factor_counts[i]:
            continue
        for j in range(i, N, i):
            prime_factors[j, factor_counts[j]] = i
            factor_counts[j] += 1
    return prime_factors


def _is_prime_basic(n: int) -> bool:
    """
    Basic primality test using 6k+-1 optimization.
    Called in is_prime for small n.
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def is_prime(n: int) -> bool:
    """
    Returns True if n is prime, else returns False.
    Utilises Miller-Rabin primality test for n > 1,000,000.
    Result is deterministic for n < 3317044064679887385961981.
    For larger n, False means n defintely composite and True means n is very likely prime.
    https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    """

    if n != int(n):
        return False

    if n < 1_000_000:
        # Faster for small n
        return _is_prime_basic(n)

    s = 0
    d = n - 1
    while d % 2 == 0:
        d >>= 1
        s += 1
    assert 2 ** s * d == n - 1

    def trial_composite(a: int) -> bool:
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True  # n definitely composite

    """
    The following test cases are sufficient
    https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    """
    if n < 1373653:
        testCases = [2, 3]
    elif n < 25326001:
        testCases = [2, 3, 5]
    elif n < 3215031751:
        testCases = [2, 3, 5, 7]
    elif n < 2152302898747:
        testCases = [2, 3, 5, 7, 11]
    elif n < 3474749660383:
        testCases = [2, 3, 5, 7, 11, 13]
    elif n < 341550071728321:
        testCases = [2, 3, 5, 7, 11, 13, 17]
    elif n < 3825123056546413051:
        testCases = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    elif n < 318665857834031151167461:
        testCases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    elif n < 3317044064679887385961981:
        testCases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    else:
        testCases = [random.randrange(2, n) for i in range(8)]  # probablistic version

    for a in testCases:
        if trial_composite(a):
            return False

    return True
