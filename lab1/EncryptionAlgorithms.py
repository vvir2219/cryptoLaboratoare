from Exceptions import ValidationException

def _gcd(a, b):
    if b == 0:
        return a
    return _gcd(b, a % b)

def gcd(a, b):
    return _gcd(abs(a), abs(b))

def _egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    d, x0, y0 = _egcd(b, a % b)
    return (d, y0, x0 - (a//b)*y0)

def egcd(a, b):
    return _egcd(abs(a), abs(b));

class EncryptionAlgorithm:
    def __init__(self, alphabet):
        self._validateAlphabet(alphabet)
        self.alphabet = alphabet

    def _validateAlphabet(self, alphabet):
        if len(set(alphabet)) != len(alphabet):
            raise ValidationException("Alfabetul trebuie sa fie un string cu proprietati de multime",
                    alphabet)

    # validates the key
    # throws ValidationException
    def _validateKey(self, key):
        pass

    # validates the plain text
    # throws ValidationException
    def _validatePlainText(self, text):
        pass

    # validates the cipher text
    # throws ValidationException
    def _validateCipherText(self, text):
        pass

    def _encrypt(self, key, text):
        pass

    def _decrypt(self, key, text):
        pass

    def encrypt(self, key, text):
        self._validateKey(key)
        self._validatePlainText(text)
        return self._encrypt(key, text)

    def decrypt(self, key, text):
        self._validateKey(key)
        self._validateCipherText(text)
        return self._decrypt(key, text)


class CaesarCipher(EncryptionAlgorithm):
    # validates the key
    # throws ValidationException
    def _validateKey(self, key):
        if not isinstance(key, (int, long)):
            raise ValidationException('Key is not integer', key)
        if not (0 <= key < len(self.alphabet)):
            raise ValidationException('Key is not in the alphabet\'s bounds', key)

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
        return ''.join([self.alphabet[(self.alphabet.find(c) + key) % len(self.alphabet)] for
                c in text]).upper()

    def _decrypt(self, key, text):
        return self._encrypt(-key, text.lower()).lower()


class SubstitutionCipher(EncryptionAlgorithm):
    # validates the key
    # throws ValidationException
    def _validateKey(self, key):
        if not isinstance(key, str):
            raise ValidationException('Key is not string', key)
        if not len(key) == len(self.alphabet):
            raise ValidationException('Key length has to be equal to alphabet length', key)
        if not len(key) == len(set(key)):
            raise ValidationException('Key has to be a set', key)

    # validates the plain text
    # throws ValidationException
    def _validatePlainText(self, text):
        if len(set(text).difference(set(self.alphabet))) > 0:
            raise ValidationException('Plaintext contains characters which are not in the alphabet', text)

    # validates the cipher text
    # throws ValidationException
    def _validateCipherText(self, key, text):
        if len(set(text).difference(set(key))) > 0:
            raise ValidationException('Ciphertext contains characters which are not in the cipher key', text)

    def _encrypt(self, key, text):
        return ''.join([key[self.alphabet.find(c)] for c in text])

    def _decrypt(self, key, text):
        return ''.join([self.alphabet[key.find(c)] for c in text])

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
class HillCipher(EncryptionAlgorithm):
    def _validateKey(self, key):
        if not (isinstance(key, list) and
                is_square(len(key)) and
                all(map(lambda x: isinstance(x, (int, long)), key))):
            raise ValidationException('Key is not valid', key)
        n = int(np.sqrt(len(key)))
        det = int(round(np.linalg.det(np.array(key).reshape([n, n]))))
        if det == 0 or gcd(det, len(self.alphabet)) != 1:
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
        n = int(np.sqrt(len(key)))
        key = np.array(key).reshape([n, n])

        if len(text) % n != 0:
            text = text + (n - len(text) % n)*self.alphabet[0]
        textlen = len(text)
        text = np.array(map(lambda x : self.alphabet.find(x), text)).reshape(len(text) // n, n)

        text = (np.matmul(text, key) % len(self.alphabet)).reshape(textlen)
        return ''.join(map(lambda x : self.alphabet[x], text)).upper()

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


