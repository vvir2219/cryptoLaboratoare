#!/bin/python2
import argparse
import math

g_verbose = False
g_verbose_indent = ''
g_indent_tab = [4]

def print_verbose(message, end = "\n"):
    global g_verbose
    if g_verbose:
        print g_verbose_indent + message + end,

def indent_verbose(amount):
    global g_verbose_indent
    g_verbose_indent += ' '*amount

def dedent_verbose(amount):
    global g_verbose_indent
    g_verbose_indent = g_verbose_indent[:-amount]

def indented(amount):
    def _indented_decorator(func):
        def wrapper(*args, **kwargs):
            indent_verbose(amount[0])
            ret_value = func(*args, **kwargs)
            dedent_verbose(amount[0])
            return ret_value
        return wrapper
    return _indented_decorator

@indented(g_indent_tab)
def factor_sqrtn(number, bound):
    n = int(math.sqrt(number))
    for i in xrange(bound):
        if number % (n - i) == 0:
            return n - i, number // (n - i)

@indented(g_indent_tab)
def factor_fermat(number, bound):
    from gmpy import is_square
    n = int(math.sqrt(number))
    for t in xrange(n, n+bound):
        s2 = t*t - number
        if is_square(s2):
            s = int(math.sqrt(s2))
            return t+s, t-s

@indented(g_indent_tab)
def prime_factors_limited(n, prime_limit):
    factors = []
    factor = 2
    while n > 1:
        if factor > prime_limit:
            return None

        if n % factor == 0:
            facpow = 0
            while n % factor == 0:
                n //= factor
                facpow += 1
            factors.append((factor, facpow))
        else:
            factor += 1
    return factors

@indented(g_indent_tab)
def prime_factors(n):
    factors = []
    factor = 2
    while n > 1:
        if n % factor == 0:
            facpow = 0
            while n % factor == 0:
                n //= factor
                facpow += 1
            factors.append((factor, facpow))
        else:
            factor += 1
    return factors

@indented(g_indent_tab)
def least_absolute_residue(n, a):
    if a < n // 2:
        return a
    return a - n;

def gen_factor_base(factorizations):
    factor_base = set()
    factor_base.add(-1)
    for i in xrange(len(factorizations)):
        factorization = factorizations[i]
        for prime, power in factorization:
            if power % 2 == 0:
                factor_base.add(prime)
            else:
                for j in xrange(len(factorizations)):
                    if i != j:
                        if prime in map(lambda x: x[0], factorizations[j]):
                            factor_base.add(prime)
                            break
    return sorted(factor_base)

def in_base(base, number):
    based = [0] * len(base)
    if number < 0:
        based[base.index(-1)] = 1
        number *= -1
    factors = prime_factors(number)
    primes = map(lambda x: x[0], factors)
    if len(set(base).intersection(set(primes))) != len(primes):
        return None

    for prime, power in factors:
        based[base.index(prime)] = power

    return based

@indented(g_indent_tab)
def cf2(n, bound, small_primes_bound):
    sqrtn = math.sqrt(n)
    a, b, x = [int(sqrtn)], [1, int(sqrtn)], [sqrtn - int(sqrtn)]
    out = [least_absolute_residue(n, pow(b[1], 2, n))]
    for i in xrange(1, bound):
        a.append(int(1/x[i-1]))
        x.append(1/x[i-1] - a[i])
        b.append(a[i]*b[(i+1)-1] + b[(i+1)-2])
        b[i+1] = b[i+1] % n
        out.append(least_absolute_residue(n, pow(b[i+1], 2, n)))
    out = [ x for x in out if prime_factors_limited(abs(x), small_primes_bound) is not None]
    print out
    factor_base = gen_factor_base([ prime_factors(abs(x)) for x in out])

    return a, b, x, out, factor_base, [x for x in [in_base(factor_base, x) for x in out] if x]


@indented(g_indent_tab)
def factor_continued_fractions(number, bound):
    raise ValueError("Function not yet implemented")


factorization_methods = {
    'sqrtn' : factor_sqrtn,
    'fermat' : factor_fermat,
    'continued-fractions' : factor_continued_fractions
}

def factor(args):
    global factorization_methods
    method = args.method
    number = args.number
    bound = args.bound

    if number <= 1:
        raise ValueError("Number has to be greater than 1")

    if not bound:
        bound = int(math.sqrt(number))

    return factorization_methods[method](number, bound)

def main():
    global g_verbose

    parser = argparse.ArgumentParser(description = 'Factors a number into 2 factors if found')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
            dest='verbose', help='Makes output verbose')
    parser.add_argument('-i', '--indent', action='store', default=4, type=int,
            dest='indent', help='Indentation of verbosity in function call')
    parser.add_argument('method', choices=['sqrtn', 'fermat', 'continued-fractions'])
    parser.add_argument('number', type=int, help='The number which will be factored, has to be greater than 1')
    parser.add_argument('bound', type=int, nargs='?', default=None, help='The bound on which to serch for factors, defaults to sqrt(n)')

    args = parser.parse_args()
    g_verbose = args.verbose
    try:
        factors = factor(args)
        if factors:
            a, b = factors
            print "{} == {}*{}".format(args.number, a, b)
    except ValueError as e:
        print e

if __name__ == "__main__":
    main()
