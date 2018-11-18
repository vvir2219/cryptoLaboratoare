#!/bin/python2

import random
import argparse
import json

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

random.seed();

##
# @brief Greatest common divisor between two positive integers
#
# @param a integer
# @param b integer
#
# @return gcd between a and b
@indented(g_indent_tab)
def _gcd(a, b):
    if b == 0:
        print_verbose("a = {}".format(a))

        return a
    if g_verbose:
        print_verbose("a = {}\tb = {}".format(a, b))

    return _gcd(b, a % b)

@indented(g_indent_tab)
def _gcd(a, b):
    print_verbose("gcd({}, {}) = ".format(a, b), end="")
    while b != 0:
        print_verbose("gcd({1}, {0} % {1}) =".format(a, b))
        print_verbose("gcd({}, {}) = ".format(b, a%b), end="")

        a, b = b, a % b
    print_verbose("{}".format(a))
    return a

##
# @brief Greatest common divisor between two integer
#
# @param a
# @param b
#
# @return 
def gcd(a, b):
    return _gcd(abs(a), abs(b))

##
# @brief Extended greatest common divisor between two positive integers
#
# @param a integer
# @param b integer
#
# @return A tuple of (d, x, y)
# where d = gcd(a, b), x and y are coefficients of ax + by = d identity
@indented(g_indent_tab)
def _egcd(a, b):
    if b == 0:
        print_verbose("d = {}\tx = 1\ty =0".format(a))

        return (a, 1, 0)
    d, x0, y0 = _egcd(b, a % b)
    print_verbose("d = "+str(d)+"\tx = " +str(y0)+"\ty = "+str(x0-(a//b)*y0));

    return (d, y0, x0 - (a//b)*y0)
@indented(g_indent_tab)
def _egcd(a, b):
    print_verbose("solves the equation: "+str(a)+"*x + "+str(b)+"*y = gcd("+str(a)+", "+str(b)+") ")
    print_verbose("q = cat")
    print_verbose("r = rest")
    print_verbose("x = coeficientul lui a")
    print_verbose("y = coeficientul lui b")
    s, _s = 0, 1
    t, _t = 1, 0
    r, _r = b, a
    print_verbose("q = 0\tr = "+str(_r)+"\tx = "+str(_s)+"\ty = "+str(_t));
    while r != 0:
        q = _r // r
        _r, r = r, _r - q*r
        _s, s = s, _s - q*s
        _t, t = t, _t - q*t
        print_verbose("q = "+str(q)+"\tr = "+str(_r)+"\tx = "+str(_s)+"\ty = "+str(_t));

    return (_r, _s, _t)


##
# @brief Extended greatest common divisor between two positive integers
#
# @param a integer
# @param b integer
#
# @return A tuple of (d, x, y)
# where d = gcd(a, b), x and y are coefficients of ax + by = d identity
def egcd(a, b):
    return _egcd(abs(a), abs(b));

##
# @brief Modular inverse of b in Zn
#
# @param a - integer
# @param n - integer, modulo n
#
# @return modular inverse : a^-1 mod n
@indented(g_indent_tab)
def inv_mod(a, n):
    print_verbose("Modular inverse of "+str(a)+" in Z"+str(n))
    print_verbose("Extended gcd:")
    d, x, y = egcd(a, n);
    if d != 1:
        print_verbose("Gcd is not 1, modular inverse does not exist")
        raise ValueError(str(a) + " does not have modular inverse in Z(" + str(n)+")");

    print_verbose("Modular inverse: "+str((x%n+n)%n))
    return (x % n + n) % n

##
# @brief computes b^e mod n
#
# @param b
# @param e
# @param n
#
# @return 
@indented(g_indent_tab)
def exp_mod(b, e, n):
    print_verbose(str(b)+"^"+str(e)+"\t( mod "+str(n)+") = ")
    if e < 0:
        print_verbose("("+str(b)+"^(-1))^"+str(-e)+"\t( mod "+str(n)+") = ")

        b = inv_mod(b, n)
        e = -e
        print_verbose(str(b)+"^"+str(e)+"\t( mod "+str(n)+") = ")
    y = 1
    while e > 1:
        if e % 2 == 1:
            y = b * y
            y %= n
        print_verbose(str(y)+" * "+str(b)+"^"+str(e//2)+" * "+str(b)+"^"+str(e//2)+"\t( mod "+str(n)+") = ");
        b *= b
        print_verbose(str(y)+" * "+str(b)+"^"+str(e//2)+"\t( mod "+str(n)+") = ");
        b %= n
        e //= 2
        print_verbose(str(y)+" * "+str(b)+"^"+str(e)+"\t( mod "+str(n)+") = ");
    print_verbose(str((b * y) % n))
    return (b * y) % n

##
# @brief incearca daca numaru ii compus relativ cu withness-u a
#
# @param a - whitness
# @param d - 
# @param n - (n-1) = (2^s)*d
# @param s - 
#
# @return 
@indented(g_indent_tab)
def _try_composite(a, d, n, s):
    print_verbose("")

    print_verbose("Calculate "+str(a)+"^"+str(d)+" mod "+str(n))
    x = exp_mod(a, d, n)
    print_verbose(str(a)+"^"+str(d)+" mod "+str(n)+" = "+str(x))
    if (x == 1) or (x == n-1):
        print_verbose(str(n) + " is pseudoprime to "+str(a))
        return False
    for i in xrange(s):
        x = (x*x) % n
        print_verbose(str(a) + "^(2^"+str(i)+")*"+str(d)+" mod "+str(n)+" = "+str(x))
        if x == n - 1:
            print_verbose(str(n) + " is pseudoprime to "+str(a))
            return False
    print_verbose(str(n) + " is composite")
    return True

@indented(g_indent_tab)
def is_prime(n, _precision_for_huge_n=16):
    print_verbose("Miller-rabin:")
    if n in _known_primes or n in (0, 1):
        print_verbose(str(n)+" is a small prime, no test needed");
        return True
    if any((n % p) == 0 for p in _known_primes):
        print_verbose(str(n)+" is divisible by small primes, no test needed");
        return False
    d, s = n - 1, 0
    while not d % 2:
        d, s = d >> 1, s + 1
    print_verbose(str(n)+" = 2^"+str(s)+" * "+str(d))
    # Returns exact according to http://primes.utm.edu/prove/prove2_3.html
    if n < 1373653:
        return not any(_try_composite(a, d, n, s) for a in (2, 3))
    if n < 25326001:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5))
    if n < 118670087467:
        if n == 3215031751:
            return False
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7))
    if n < 2152302898747:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11))
    if n < 3474749660383:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13))
    if n < 341550071728321:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13, 17))
    # otherwise
    return not any(_try_composite(a, d, n, s)
                   for a in _known_primes[:_precision_for_huge_n])

_known_primes = [2, 3]
_known_primes += [x for x in range(5, 1000, 2) if is_prime(x)]

@indented(g_indent_tab)
def is_prime2(n, _precision_for_huge_n=16):
    if (is_prime(n, _precision_for_huge_n)):
        print_verbose("With a very high probability "+str(n)+" is prime")
        return True
    print_verbose(str(n)+" is composite")
    return False

@indented(g_indent_tab)
def rand_prime2(a, b):
    print_verbose("Generate random prime between "+str(a)+" and "+str(b))
    p = random.randrange(a, b)
    print_verbose("Random number = " + str(p))
    while True:
        print_verbose("Test primality of "+str(p))
        if (is_prime(p)):
            print_verbose(str(p) + " is prime, return it")
            return p
        p = random.randrange(a, b)
        print_verbose("Another random number = " + str(p))

def rand_prime(b):
    return rand_prime2(0, b)

@indented(g_indent_tab)
def rand_coprime(lo, hi, cop):
    print_verbose("Generate coprime with "+str(cop)+" between "+str(lo)+" and "+str(hi))
    r = random.randrange(lo, hi)
    print_verbose("Random number = " + str(r))
    while True:
        print_verbose("Test gcd("+str(r)+", "+str(cop)+")")
        if gcd(r, cop) == 1:
            print_verbose(str(r) + " is coprime with "+str(cop))
            return r
        print_verbose(str(r) + " is not coprime with "+str(cop))
        r = random.randrange(lo, hi)
        print_verbose("Another random number = " + str(r))

@indented(g_indent_tab)
def rsa_generate_key(lo = 2**500, hi = 2**1000):
    print_verbose("Generate key for RSA with primes between "+
            str(lo) +" and "+str(hi))
    p, q = rand_prime2(lo, hi), rand_prime2(lo, hi)
    n = p*q
    print_verbose(str(n)+" = "+str(p)+"*"+str(q))
    phin = (p-1)*(q-1)
    print_verbose("phi("+str(n)+") = ("+str(p)+" - 1) * ("+str(q)+" - 1)")
    print_verbose("phi("+str(n)+") = "+str(phin))
    print_verbose("Generate random coprime to "+str(phin)+" between 2 and "+str(phin))
    e = rand_coprime(2, phin, phin)
    print_verbose("Compute the modular inverse between "+str(e)+" and "+
            str(phin))
    d = inv_mod(e, phin)

    print_verbose("Encryption key: ("+str(n)+", "+str(e)+")")
    print_verbose("Decryption key: ("+str(n)+", "+str(d)+")")
    return (n, e, d)

def generate_rsa_key_files(filename, lo = 2**500, hi = 2**1000):
    n, e, d = rsa_generate_key(lo, hi)
    with open(filename+"_publicKey", "w") as fpublic, open(filename+"_privateKey", "w") as fprivate:
        json.dump({'zn':n, 'exponent': e}, fpublic)
        json.dump({'zn':n, 'exponent': d}, fprivate)

@indented(g_indent_tab)
def numerical_equivalent(text, alphabet):
    print_verbose("Numerical equivalent of \""+text+"\" in the alphabet: "+alphabet)
    lit_text = ""
    num_text = ""
    old_text = text

    text = text[::-1]
    exp = 1
    putere = 0
    value = 0
    for c in text:
        lit_text += c+"*"+str(len(alphabet))+"^"+str(putere)
        num_text += str(alphabet.find(c))+"*"+str(len(alphabet))+"^"+str(putere)
        if putere + 1 < len(text):
            lit_text += " + "
            num_text += " + "
        value += exp * alphabet.find(c)
        exp *= len(alphabet)
        putere += 1

    print_verbose(text + " = " +lit_text + " = ")
    print_verbose(num_text + " = " + str(value))
    return value

@indented(g_indent_tab)
def literal_equivalent(value, alphabet):
    old_value = value
    print_verbose("Literal equivalent of "+str(value)+" in the alphabet: "+alphabet)
    text = ''
    while value > 0:
        print_verbose(str(value) + " mod "+ str(len(alphabet))+" = " + str(value %len(alphabet)) + " = \"" + str(alphabet[value % len(alphabet)])+"\"")
        text += alphabet[value % len(alphabet)]
        value //= len(alphabet)

    print_verbose(str(old_value) + " = "+text[::-1])
    return text[::-1]

def pad_left(c, length, text):
    if len(text) >= length:
        return text

    return c*(length - len(text))+text

@indented(g_indent_tab)
def encrypt(key, k, l, text, alphabet = " abcdefghijklmnopqrstuvwxyz"):
    n = key['zn']
    e = key['exponent']

    print_verbose("RSA encryption")
    print_verbose("")
    print_verbose("Key: "+str(n))
    print_verbose("Exponent: "+str(e))
    print_verbose("k = "+str(k))
    print_verbose("l = "+str(l))
    print_verbose("text = \""+text+"\"")
    print_verbose("alphabet = \""+alphabet+"\"")

    if not(len(alphabet)**k < n < len(alphabet)**l or
            len(alphabet)**l < n < len(alphabet)**k):
        raise ValueError("k and l are not good")

    while len(text) % k != 0:
        text += " "
    chunks = len(text) // k # k is the chunk size
    chunked =[ text[i: i + k] for i in range(0, len(text), k) ]
    print_verbose("Text by blocks: " +str(chunked))

    print_verbose("Now for each block compute it's numerical equivalent")
    chunked = map(lambda x:numerical_equivalent(x, alphabet), chunked)
    print_verbose("Numerical equivalents: "+str(chunked))

    print_verbose("For each block value v, compute v^"+str(e)+" mod "+str(n))
    chunked = map(lambda x:exp_mod(x, e, n), chunked)
    print_verbose("Encrypted blocks: "+str(chunked))

    print_verbose("Compute the literal equivalents for each chunk and pad them to length "+str(l))
    chunked = map(lambda x:literal_equivalent(x, alphabet), chunked)
    chunked = map(lambda x:pad_left(alphabet[0], l, x), chunked)
    print_verbose("Encrypted literal blocks: "+str(chunked))

    print_verbose("Encrypted value: \""+''.join(chunked)+"\"")
    return ''.join(chunked)

def encrypt_from_file(keyfilename, k, l, text, alphabet = " abcdefghijklmnopqrstuvwyz"):
    with open(keyfilename, "r") as f:
        key = json.load(f)
        return encrypt(key, k, l, text, alphabet)

def main():
    global g_verbose
    global g_indent_tab

    parser = argparse.ArgumentParser(description="RSA key generation and encryption")
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
            dest='verbose', help='Makes output verbose')
    parser.add_argument('-i', '--indent', action='store', default=4, type=int,
            dest='indent', help='Indentation of verbosity in function call')
    subparsers = parser.add_subparsers()

    parser_gen_key = subparsers.add_parser('generate-key', description="Generates a RSA key and stores it in 2 text files")
    parser_gen_key.set_defaults(func=generate_rsa_key_files)
    parser_gen_key.add_argument('filename', help='Filename for key generation,\
    it\'ll generate the files: filename_publicKey respectively\
    filename_privateKey')
    parser_gen_key.add_argument('lo', type=int, nargs='?', default=100, help='Lower bound for prime generation for RSA key')
    parser_gen_key.add_argument('hi', type=int, nargs='?', default=300, help='Upper bound for prime generation for RSA key')

    parser_encrypt = subparsers.add_parser('encrypt', description="Encrypts/decrypts a text given a key")
    parser_encrypt.set_defaults(func=encrypt_from_file)
    parser_encrypt.add_argument('keyfilename');
    parser_encrypt.add_argument('k', type=int, help='Text block length')
    parser_encrypt.add_argument('l', type=int, help='Text block length after encryption')
    parser_encrypt.add_argument('text', help='Text to be encrypted/decrypted')
    parser_encrypt.add_argument('alphabet', nargs='?', default=' abcdefghijklmnopqrstuvwxyz', help='Encryption alphabet')

    args = parser.parse_args()
    func = args.func;
    g_verbose = args.verbose;
    g_indent_tab[0] = args.indent;

    arguments = dict(vars(args))
    del arguments['func']
    del arguments['verbose']
    del arguments['indent']

    try:
        value = func(**arguments)
        if value:
            print "\""+str(value)+"\""
    except ValueError as e:
        print e

if __name__ == "__main__":
    main()
