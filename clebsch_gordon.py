import numpy as np
from math import factorial

def lorentzian(x, gamma, x_0, offset, a):
    return a * (1 / np.pi) * (0.5 * gamma) / ((x - x_0) ** 2 + (0.5 * gamma) ** 2) + offset


def triangle_coefficient(a, b, c):
    num = factorial(a + b - c) * factorial(a - b + c) * factorial(-a + b + c)
    den = factorial(a + b + c + 1)
    return num / den


def wigner_3j(j1, j2, j3, m1, m2, m3):
    if m1 > abs(j1) or m2 > abs(j2) or m3 > abs(j3):
        print('m value is greater than j')
        return np.nan
    
    if j3 < (j1 - j2) or j3 > (j1 + j2):
        print('Triangle relation not satisfied')
        return np.nan
    
    if int(m1 + m2 + m3) != 0:
        print('m values do not sum to 0')
        return np.nan
    
    if f'{j1 + j2 + j3:.01f}'[-1] != '0':
        print('j values do not sum to 0')
        return np.nan
    
    sign = (-1) ** (j1 - j2 - m3)
    try:
        triangle = np.sqrt(triangle_coefficient(j1, j2, j3))
    except ValueError:
        return np.nan
    factor = np.sqrt(factorial(j1 + m1) * factorial(j1 - m1)
                     * factorial(j2 + m2) * factorial(j2 - m2)
                     * factorial(j3 + m3) * factorial(j3 - m3))
    sum_limit = min([j1 + m1, j1 - m1, j2 + m2, j2 - m2, j3 + m3, j3 - m3,
                     j1 + j2 - j3, j1 - j2 + j3, -j1 + j2 + j3]) + 1
    sum_limit = max(0, sum_limit)
    total = 0
    iterations = 0
    t = 0
    while iterations < sum_limit:
        try:
            x = factorial(t) * factorial(j3 - j2 + t + m1) * factorial(j3 - j1 + t - m2) * factorial(
                j1 + j2 - j3 - t) * factorial(j1 - t - m1) * factorial(j2 - t + m2)
            total += (-1) ** t / x
        except ValueError:
            t += 1
            continue
        
        t += 1
        iterations += 1
    
    return sign * triangle * factor * total


def wigner_6j(a, b, c, d, e, f):
    try:
        t1 = triangle_coefficient(a, b, c)
        t2 = triangle_coefficient(a, e, f)
        t3 = triangle_coefficient(d, b, f)
        t4 = triangle_coefficient(d, e, c)
    except ValueError:
        print('wigner_6j nan')
        return np.nan
    triangle = np.sqrt(t1 * t2 * t3 * t4)
    
    sum_limit = min([a + b - c, -a + b + c, a - b + c,
                     a + e - f, -a + e + f, a - e + f,
                     b + d - f, -b + d + f, b - d + f,
                     c + d - e, -c + d + e, c - d + e]) + 1
    sum_limit = int(max(0, sum_limit))
    total = 0
    iterations = 0
    t = 0
    while iterations < sum_limit:
        try:
            x = factorial(t - a - b - c)
            x *= factorial(t - a - e - f)
            x *= factorial(t - d - b - f)
            x *= factorial(t - d - e - c)
            x *= factorial(a + b + d + e - t)
            x *= factorial(b + c + e + f - t)
            x *= factorial(a + c + d + f - t)
            total += ((-1) ** t * factorial(t + 1)) / x
        except ValueError:
            t += 1
            continue
        
        t += 1
        iterations += 1
    
    return triangle * total


def two_photon_clebsch_gordon(J, Jp, F, Fp, I, mF, mFp):
    q = mF - mFp
    return wigner_3j(Fp, 2, F, mFp, q, -mF) * wigner_6j(J, Jp, 2, Fp, F, I) * ((-1) ** (J + I + mF)) * (
        np.sqrt((2 * Fp + 1) * (2 * F + 1) * (2 * J + 1)))


def field_shift(S, L, J, I, F, mF, Bz):
    gL = 1
    gS = 2
    gJ = (1 / (2 * J * (J + 1))) * (
                gL * (J * (J + 1) - S * (S + 1) + L * (L + 1)) + gS * (J * (J + 1) + S * (S + 1) - L * (L + 1)))
    gF = (1 / (2 * F * (F + 1))) * (gJ * (F * (F + 1) - I * (I + 1) + J * (J + 1)))
    return 1.399624624e6 * gF * mF * Bz