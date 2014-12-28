__author__ = 'thienbao'


def gcd(num1, num2):
    max_number = max(num1, num2)
    min_number = min(num1, num2)
    while min_number != 0:
        mod_number = max_number % min_number
        max_number = min_number
        min_number = mod_number

    return max_number

def mod_inverse(a, m):
    """
    :param a: to find the mod inverse.
    :param m: mode integer.
    :return: mod inverse of a in mode m.
    """
    assert gcd(a,m) == 1, "%d and %d is not relative prime. So can not find mod inverse of %d" % (a, m, a)
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = u1 - q*v1, u2 - q*v2, u3 - q*v3, v1, v2, v3

    return u1 % m
