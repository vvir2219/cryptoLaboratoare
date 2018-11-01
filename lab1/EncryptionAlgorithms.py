from Exceptions import ValidationException

##
# @brief Greatest common divisor between two positive integers
#
# @param a integer
# @param b integer
#
# @return gcd between a and b
def _gcd(a, b):
    if b == 0:
        return a
    return _gcd(b, a % b)

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
def _egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    d, x0, y0 = _egcd(b, a % b)
    return (d, y0, x0 - (a//b)*y0)

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
# @brief Base encryption algorigm class, defines the API
class EncryptionAlgorithm:
    ##
    # @brief Constructor
    #
    # @param alphabet string - List of symbols for plaintext and ciphertext
    #
    # @return The object
    def __init__(self, alphabet):
        self.setAlphabet(alphabet)

    ##
    # @brief internal method for validating the alphabet
    #
    # @param alphabet
    #
    # @return 
    def _validateAlphabet(self, alphabet):
        if len(set(alphabet)) != len(alphabet):
            raise ValidationException("Alfabetul trebuie sa fie un string cu proprietati de multime",
                    alphabet)
        if len(alphabet) == 0:
            raise ValidationException("Alfabetul nu poate fi vid");
        if alphabet.lower() != alphabet:
            raise ValidationException("Alfabetul nu poate contine litere mari.");

    ##
    # @brief Sets the new alphabet, validates it
    #
    # @param alphabet - string
    #
    # @return None
    def setAlphabet(self, alphabet):
        self._validateAlphabet(alphabet)
        self.alphabet = alphabet

    ##
    # @brief Validates the key.
    # Throws ValidationException
    #
    # @param key
    #
    # @return None
    def _validateKey(self, key):
        pass

    ##
    # @brief validates the plain text.
    # Throws ValidationException
    #
    # @param text
    #
    # @return 
    def _validatePlainText(self, text):
        pass

    ##
    # @brief validates the cipher text.
    # Throws ValidationException
    #
    # @param text
    #
    # @return 
    def _validateCipherText(self, text):
        pass

    ##
    # @brief internal encryption function, called by encrypt
    #
    # @param key
    # @param text
    #
    # @return encrypted text
    def _encrypt(self, key, text):
        pass

    ##
    # @brief internal decryption function, called by decrypt
    #
    # @param key
    # @param text
    #
    # @return decrypted text
    def _decrypt(self, key, text):
        pass

    ##
    # @brief Encryption function, validates key and plaintext.
    # Throws ValidationException
    #
    # @param key
    # @param text
    #
    # @return Encrypted text
    def encrypt(self, key, text):
        self._validateKey(key)
        self._validatePlainText(text)
        return self._encrypt(key, text)

    ##
    # @brief Decryption function, validates key and ciphertext.
    #
    # @param key
    # @param text
    #
    # @return Decrypted text
    def decrypt(self, key, text):
        self._validateKey(key)
        self._validateCipherText(text)
        return self._decrypt(key, text)


##
# @brief Implements the Caesar cipher, has all methods from EncryptionAlgorithm
class CaesarCipher(EncryptionAlgorithm):
    ##
    # @brief validates the key.
    # Throws ValidationException.
    # Key has to be an integer between 0 and alphabet length.
    #
    # @param key
    #
    # @return 
    def _validateKey(self, key):
        if not isinstance(key, (int, long)):
            raise ValidationException('Key is not integer', key)
        if not (0 <= key < len(self.alphabet)):
            raise ValidationException('Key is not in the alphabet\'s bounds', key)

    ##
    # @brief validates the plain text.
    # Throws ValidationException.
    # Plaintext has to contain only characters from the alphabet.
    #
    # @param text
    #
    # @return 
    def _validatePlainText(self, text):
        if len(set(text).difference(set(self.alphabet))) > 0:
            raise ValidationException('Plaintext contains characters which are not in the alphabet', text)

    ##
    # @brief validates the cipher text.
    # Throws ValidationException.
    # Ciphertext has to contain only characters from the uppercase(alphabet).
    #
    # @param text
    #
    # @return 
    def _validateCipherText(self, text):
        if len(set(text).difference(set(self.alphabet.upper()))) > 0:
            raise ValidationException('Ciphertext contains characters which are not in the cipher alphabet', text)

    ##
    # @brief Internal encryption function.
    # Shifts each character from the plaintext by 'key' ammount of characters in
    # the alphabet.
    #
    # @param key
    # @param text
    #
    # @return 
    def _encrypt(self, key, text):
        return ''.join([self.alphabet[(self.alphabet.find(c) + key) % len(self.alphabet)] for
                c in text]).upper()

    ##
    # @brief Internal decryption function.
    # Encrypth with -key
    #
    # @param key
    # @param text
    #
    # @return 
    def _decrypt(self, key, text):
        return self._encrypt(-key, text.lower()).lower()


##
# @brief Extends EncryptionAlgorithm
class SubstitutionCipher(EncryptionAlgorithm):
    ##
    # @brief validates the key.
    # Throws ValidationException.
    # Key has to be a string with set properties and equal of length with the
    # alphabet.
    #
    # @param key
    #
    # @return 
    def _validateKey(self, key):
        if not isinstance(key, str):
            raise ValidationException('Key is not string', key)
        if not len(key) == len(self.alphabet):
            raise ValidationException('Key length has to be equal to alphabet length', key)
        if not len(key) == len(set(key)):
            raise ValidationException('Key has to be a set', key)

    ##
    # @brief validates the plain text.
    # Throws ValidationException.
    # Plaintext has to contain only characters from the alphabet.
    #
    # @param text
    #
    # @return 
    def _validatePlainText(self, text):
        if len(set(text).difference(set(self.alphabet))) > 0:
            raise ValidationException('Plaintext contains characters which are not in the alphabet', text)

    ##
    # @brief validates the cipher text.
    # Throws ValidationException.
    # Ciphertext has to contain only characters from the uppercase(alphabet).
    #
    # @param text
    #
    # @return 
    def _validateCipherText(self, key, text):
        if len(set(text).difference(set(key))) > 0:
            raise ValidationException('Ciphertext contains characters which are not in the cipher key', text)

    ##
    # @brief Internal encryption function.
    # Substitutes each character in the plaintext with the corresponding
    # character in the ciphertext.
    #
    # @param key
    # @param text
    #
    # @return Encrypted text
    def _encrypt(self, key, text):
        return ''.join([key[self.alphabet.find(c)] for c in text])

    ##
    # @brief Internal decryption function.
    # Substitutes each character in the ciphertext with the corresponding
    # character in the plaintext.
    #
    # @param key
    # @param text
    #
    # @return Decrypted text
    def _decrypt(self, key, text):
        return ''.join([self.alphabet[key.find(c)] for c in text])

    ##
    # @brief Overload on decrypth method.
    # Overload needed because ciphertext validation has to include the key.
    #
    # @param key
    # @param text
    #
    # @return Decrypted text
    def decrypt(self, key, text):
        self._validateKey(key)
        self._validateCipherText(key, text)
        return self._decrypt(key, text)


class AffineCipher(EncryptionAlgorithm):
    # validates the key
    # throws ValidationException
    def _validateKey(self, key):
        if not (isinstance(key[0], (int, long)) and
                isinstance(key[1], (int, long)) and
                0 <= key[0] < len(self.alphabet) and 
                0 <= key[1] < len(self.alphabet) and 
                gcd(key[0], len(self.alphabet)) == 1):
            raise ValidationException('Key is not valid', key)

    # validates the plain text
    # throws ValidationException
    def _validatePlainText(self, text):
        if len(set(text).difference(set(self.alphabet))) > 0:
            raise ValidationException('Plaintext contains characters which are not in the alphabet', text)

    # validates the cipher text
    # throws ValidationException
    def _validateCipherText(self, text):
        if len(set(text).difference(set(self.alphabet.upper()))) > 0:
            raise ValidationException('Ciphertext contains characters which are not in the cipher alphabet', text)

    def _encrypt(self, key, text):
        affineEncryption = lambda c : self.alphabet[(key[0] * self.alphabet.find(c) + key[1]) % len(self.alphabet)]
        return ''.join([affineEncryption(c) for c in text]).upper()

    def _decrypt(self, key, text):
        _, _, a_reversed = egcd(len(self.alphabet), key[0])
        affineDecryption = lambda c :self.alphabet[((self.alphabet.find(c) - key[1]) * a_reversed) % len(self.alphabet)]
        return ''.join([affineDecryption(c) for c in text.lower()])


class BelasoCipher(EncryptionAlgorithm):
    def _validateKey(self, key):
        if not (isinstance(key, str) and
                len(key) > 0 and
                len(set(key).difference(set(self.alphabet))) == 0):
            raise ValidationException('Key is not valid', key)

    # validates the plain text
    # throws ValidationException
    def _validatePlainText(self, text):
        if len(set(text).difference(set(self.alphabet))) > 0:
            raise ValidationException('Plaintext contains characters which are not in the alphabet', text)

    # validates the cipher text
    # throws ValidationException
    def _validateCipherText(self, text):
        if len(set(text).difference(set(self.alphabet.upper()))) > 0:
            raise ValidationException('Ciphertext contains characters which are not in the cipher alphabet', text)

    def _encrypt(self, key, text):
        encrypted = []
        for i in xrange(len(text)):
            encrypted.append(self.alphabet[(self.alphabet.find(text[i]) + self.alphabet.find(key[i % len(key)])) % len(self.alphabet)]);
        return ''.join(encrypted).upper()

    def _decrypt(self, key, text):
        ciphertext = text.lower();
        decrypted = []
        for i in xrange(len(ciphertext)):
            decrypted.append(self.alphabet[(self.alphabet.find(ciphertext[i]) - self.alphabet.find(key[i % len(key)])) % len(self.alphabet)]);
        return ''.join(decrypted)


from gmpy import is_square
import numpy as np
from sympy import Matrix
##
# @brief Extends EncryptionAlgorithm
class HillCipher(EncryptionAlgorithm):
    ##
    # @brief Validates the key.
    # Throws ValidationException.
    # Key is a square matrix of integers given as a list of nxn elements.
    # Key has to be invertible and gcd(det(key), len(alphabet)) has to be 1.
    # @param key
    #
    # @return 
    def _validateKey(self, key):
        if not (isinstance(key, list) and
                is_square(len(key)) and
                all(map(lambda x: isinstance(x, (int, long)), key))):
            raise ValidationException('Key is not valid', key)
        n = int(np.sqrt(len(key)))
        det = int(round(np.linalg.det(np.array(key).reshape([n, n]))))
        if det == 0 or gcd(det, len(self.alphabet)) != 1:
            raise ValidationException('Key is not valid', key)

    ##
    # @brief validates the plain text.
    # Throws ValidationException.
    # Plaintext has to contain only characters from the alphabet.
    #
    # @param text
    #
    # @return 
    def _validatePlainText(self, text):
        if len(set(text).difference(set(self.alphabet))) > 0:
            raise ValidationException('Plaintext contains characters which are not in the alphabet', text)

    ##
    # @brief validates the cipher text.
    # Throws ValidationException.
    # Ciphertext has to contain only characters from the uppercase(alphabet).
    #
    # @param text
    #
    # @return 
    def _validateCipherText(self, text):
        if len(set(text).difference(set(self.alphabet.upper()))) > 0:
            raise ValidationException('Ciphertext contains characters which are not in the cipher alphabet', text)

    ##
    # @brief Internal encryption function.
    # Splits the plaintext in blocks of length N(key is a matrix of NxN).
    # and concatenates dot products between key and each block.
    #
    # @param key
    # @param text
    #
    # @return 
    def _encrypt(self, key, text):
        n = int(np.sqrt(len(key)))
        key = np.array(key).reshape([n, n])

        if len(text) % n != 0:
            text = text + (n - len(text) % n)*self.alphabet[0]
        textlen = len(text)
        text = np.array(map(lambda x : self.alphabet.find(x), text)).reshape(len(text) // n, n)

        text = (np.matmul(text, key) % len(self.alphabet)).reshape(textlen)
        return ''.join(map(lambda x : self.alphabet[x], text)).upper()

    ##
    # @brief Internal decryption function.
    # Splits the plaintext in blocks of length N(key is a matrix of NxN).
    # and concatenates dot products between the modular inverse of the key and
    # each block.
    #
    # @param key
    # @param text
    #
    # @return 
    def _decrypt(self, key, text):
        n = int(np.sqrt(len(key)))
        if len(text) % n != 0:
            raise ValidationException('Ciphertext has wrong length', text)

        key = Matrix(np.array(key).reshape([n, n])).inv_mod(len(self.alphabet))
        key = np.array(key).astype(long)

        textlen = len(text)
        text = text.lower()
        text = np.array(map(lambda x : self.alphabet.find(x), text)).reshape(len(text) // n, n)
        text = (np.matmul(text, key) % len(self.alphabet)).reshape(textlen)
        return ''.join(map(lambda x : self.alphabet[x], text))


class PermutationCipher(EncryptionAlgorithm):
    def _validateKey(self, key):
        if not (isinstance(key, list) and
                list(sorted(key)) == list(range(len(key)))):
            raise ValidationException('Key is not valid', key)

    # validates the plain text
    # throws ValidationException
    def _validatePlainText(self, text):
        if len(set(text).difference(set(self.alphabet))) > 0:
            raise ValidationException('Plaintext contains characters which are not in the alphabet', text)

    # validates the cipher text
    # throws ValidationException
    def _validateCipherText(self, text):
        if len(set(text).difference(set(self.alphabet.upper()))) > 0:
            raise ValidationException('Ciphertext contains characters which are not in the cipher alphabet', text)

    def _encrypt(self, key, text):
        if len(text) % len(key) != 0:
            text = text + (len(key) - len(text) % len(key))*self.alphabet[0]
        no_blocks = len(text) // len(key)

        cipher = []
        for i in xrange(no_blocks):
            for j in xrange(len(key)):
                cipher.append(text[i*len(key) + key[j]])

        return ''.join(cipher).upper()


    def _decrypt(self, key, text):
        if len(text) % len(key) != 0:
            raise ValidationException('Ciphertext has wrong length', text)
        decriptionKey = [0]*len(key)
        for i in range(len(key)):
            decriptionKey[key[i]] = i

        return self._encrypt(decriptionKey, text.lower()).lower()


